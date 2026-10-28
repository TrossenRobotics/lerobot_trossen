import logging
import time
from typing import Any

from lerobot.cameras.utils import make_cameras_from_configs
from lerobot.robots import Robot

from lerobot_robot_trossen.bi_widowx_follower import (
    BiWidowXCoreFollowerRobot,
    BiWidowXProFollowerRobot,
)
from lerobot_robot_trossen.config_rivet import (
    RivetRobotConfig,
    RivetWidowXCoreRobotConfig,
    RivetWidowXProRobotConfig,
    RivetWidowXRobotConfig,
)

logger = logging.getLogger(__name__)

# Lift is considered at its goal within this distance (m)
LIFT_POSITION_TOLERANCE = 0.005
# Odometry is considered zeroed within this tolerance (m, rad)
ODOMETRY_RESET_TOLERANCE = 0.001
# Max time to wait for the odometry to report the reset
ODOMETRY_RESET_TIMEOUT_S = 1.0


class RivetRobot(Robot):
    """
    [Rivet](https://www.trossenrobotics.com/rivet) base without arms by Trossen Robotics
    """

    config_class = RivetRobotConfig
    name = "rivet_robot"

    def __init__(self, config: RivetRobotConfig):
        super().__init__(config)
        self.config = config

        # Only require this dependency if this robot is being used
        import trossen_base

        self.base = trossen_base.TrossenBase()

        self.cameras = make_cameras_from_configs(config.cameras)

    @property
    def _base_ft(self) -> dict[str, type]:
        return {"x.vel": float, "y.vel": float, "theta.vel": float, "lift.pos": float}

    @property
    def _base_obs_ft(self) -> dict[str, type]:
        # Odometry position and lift velocity are observed but not commanded
        return {
            "x.pos": float,
            "y.pos": float,
            "theta.pos": float,
            **self._base_ft,
            "lift.vel": float,
        }

    @property
    def _cameras_ft(self) -> dict[str, tuple]:
        # Depth cameras add a separate (H, W, 1) "<cam>_depth" feature; single channel flags it as depth.
        features: dict[str, tuple] = {}
        for cam_key, cam in self.cameras.items():
            if getattr(cam, "use_rgb", True):
                features[cam_key] = (cam.height, cam.width, 3)
            if getattr(cam, "use_depth", False):
                features[f"{cam_key}_depth"] = (cam.height, cam.width, 1)
        return features

    @property
    def observation_features(self) -> dict[str, type | tuple]:
        return {**self._base_obs_ft, **self._cameras_ft}

    @property
    def action_features(self) -> dict[str, type]:
        return self._base_ft

    @property
    def is_connected(self) -> bool:
        return self.base.is_configured() and all(
            cam.is_connected for cam in self.cameras.values()
        )

    def connect(self, calibrate: bool = True) -> None:
        for cam in self.cameras.values():
            cam.connect()

        # Configure the base last so the heartbeat is not starved by slower connections
        self.base.configure(use_lidar=True)
        self.base.heartbeat()

        self.configure()

    def configure(self, reset_odometry: bool = True) -> None:
        # Move the lift to the staged position and wait for it to arrive. If reset_odometry=True,
        # resets the odometry to zero.
        if not self.base.set_lift_position(
            self.config.lift_staged_position, self.config.lift_velocity
        ):
            raise RuntimeError(f"{self} failed to command lift to staged position")
        while (
            abs(self.base.get_lift_state().position - self.config.lift_staged_position)
            > LIFT_POSITION_TOLERANCE
        ):
            self.base.heartbeat()
            time.sleep(0.01)

        # Reset odometry to zero
        if reset_odometry:
            self.reset_odometry(blocking=True)

    @property
    def is_calibrated(self) -> bool:
        # The base does not require calibration
        return True

    def calibrate(self) -> None:
        # The base does not require calibration
        pass

    def reset_odometry(self, blocking: bool = False) -> None:
        # Zero the base position and heading. If blocking=True, wait for the odometry to report
        # zeroed.
        if not self.base.reset_odometry():
            raise RuntimeError(f"{self} failed to reset odometry")

        if blocking:
            deadline = time.perf_counter() + ODOMETRY_RESET_TIMEOUT_S
            while True:
                self.base.heartbeat()
                position = self.base.get_odometry().position
                if all(abs(p) <= ODOMETRY_RESET_TOLERANCE for p in position):
                    return
                if time.perf_counter() > deadline:
                    raise RuntimeError(
                        f"{self} odometry did not reset within {ODOMETRY_RESET_TIMEOUT_S}s "
                        f"(x, y, theta = {tuple(position)})"
                    )
                time.sleep(0.01)

    def get_observation(self) -> dict[str, Any]:
        self.base.heartbeat()

        obs_dict = {}

        # Get base observations
        odometry = self.base.get_odometry()
        position = odometry.position
        velocity = odometry.velocity
        lift_state = self.base.get_lift_state()
        obs_dict.update(
            {
                "x.pos": position[0],
                "y.pos": position[1],
                "theta.pos": position[2],
                "x.vel": velocity[0],
                "y.vel": velocity[1],
                "theta.vel": velocity[2],
                "lift.pos": lift_state.position,
                "lift.vel": lift_state.velocity,
            }
        )

        # read_latest*() is a non-blocking peek of the latest frame; depth cameras also yield "<cam>_depth".
        for cam_key, cam in self.cameras.items():
            if getattr(cam, "use_rgb", True):
                start = time.perf_counter()
                obs_dict[cam_key] = cam.read_latest()
                dt_ms = (time.perf_counter() - start) * 1e3
                logger.debug(f"{self} read {cam_key}: {dt_ms:.1f}ms")

            if getattr(cam, "use_depth", False):
                start = time.perf_counter()
                obs_dict[f"{cam_key}_depth"] = cam.read_latest_depth()
                dt_ms = (time.perf_counter() - start) * 1e3
                logger.debug(f"{self} read {cam_key} depth: {dt_ms:.1f}ms")

        return obs_dict

    def send_action(self, action: dict[str, Any]) -> dict[str, Any]:
        self.base.heartbeat()
        action_base_x_vel = action.get("x.vel", 0.0)
        action_base_y_vel = action.get("y.vel", 0.0)
        action_base_theta_vel = action.get("theta.vel", 0.0)
        action_base_lift_pos = action.get("lift.pos")

        self.base.set_velocities(
            [action_base_x_vel, action_base_y_vel, action_base_theta_vel]
        )
        sent_actions = {
            "x.vel": action_base_x_vel,
            "y.vel": action_base_y_vel,
            "theta.vel": action_base_theta_vel,
        }

        if action_base_lift_pos is not None:
            self.base.set_lift_position(action_base_lift_pos, self.config.lift_velocity)
            sent_actions["lift.pos"] = action_base_lift_pos

        return sent_actions

    def disconnect(self):
        # Stop the base and cleanup the driver
        self.base.cleanup()

        for cam in self.cameras.values():
            cam.disconnect()


class RivetWidowXRobot(RivetRobot):
    """
    [Rivet with WidowX Follower Arms](https://www.trossenrobotics.com/rivet) Abstract class by
    Trossen Robotics
    """

    def __init__(self, config: RivetWidowXRobotConfig):
        super().__init__(config)

        arms_config = self.arms_class.config_class(
            left_arm_ip_address=config.left_arm_ip_address,
            right_arm_ip_address=config.right_arm_ip_address,
            left_arm_max_relative_target=config.left_arm_max_relative_target,
            right_arm_max_relative_target=config.right_arm_max_relative_target,
            min_time_to_move_multiplier=config.min_time_to_move_multiplier,
            loop_rate=config.loop_rate,
            include_velocity=config.include_velocity,
            include_effort=config.include_effort,
            include_external_effort=config.include_external_effort,
            cameras={},
            left_arm_joint_names=config.left_arm_joint_names,
            right_arm_joint_names=config.right_arm_joint_names,
            left_arm_staged_positions=config.left_arm_staged_positions,
            right_arm_staged_positions=config.right_arm_staged_positions,
        )

        self.arms = self.arms_class(arms_config)

    @property
    def observation_features(self) -> dict[str, type | tuple]:
        # Arm features (flag-aware: .pos plus optional .vel/.eff/.ext_eff) come from the bimanual
        # arms, plus the mobile base velocity and the shared cameras.
        return {**self.arms.observation_features, **super().observation_features}

    @property
    def action_features(self) -> dict[str, type]:
        return {**self.arms.action_features, **super().action_features}

    @property
    def is_connected(self) -> bool:
        return self.arms.is_connected and super().is_connected

    def connect(self, calibrate: bool = True) -> None:
        self.arms.connect(calibrate=calibrate)

        for cam in self.cameras.values():
            cam.connect()

        # Configure the base last so the heartbeat is not starved by slower connections
        self.base.configure(use_lidar=True)
        self.base.heartbeat()

        super().configure()

    @property
    def is_calibrated(self) -> bool:
        # Trossen arm robots do not require calibration but we check both arms for consistency
        return self.arms.is_calibrated

    def calibrate(self) -> None:
        # Trossen Arm robots do not require calibration but we call calibrate on both arms for
        # consistency
        self.arms.calibrate()

    def configure(self, reset_odometry: bool = True) -> None:
        super().configure(reset_odometry=reset_odometry)
        # Set the arm to position control mode
        self.arms.configure()

    def get_observation(self) -> dict[str, Any]:
        obs_dict = self.arms.get_observation()
        obs_dict.update(super().get_observation())
        return obs_dict

    def send_action(self, action: dict[str, Any]) -> dict[str, Any]:
        send_action_arms = self.arms.send_action(
            {k: v for k, v in action.items() if k in self.arms.action_features}
        )
        return {**send_action_arms, **super().send_action(action)}

    def disconnect(self):
        try:
            # Stop the base before releasing the arms
            super().disconnect()
        except Exception as e:
            # We log a warning but continue with disconnect
            logger.warning(f"Error while disconnecting Rivet and Cameras: {e}")

        try:
            self.arms.disconnect()
        except Exception as e:
            # We log a warning but continue with disconnect
            logger.warning(f"Error while disconnecting arms: {e}")


class RivetWidowXCoreRobot(RivetWidowXRobot):
    """
    [Rivet with WidowX Core Follower Arms](https://www.trossenrobotics.com/rivet) by Trossen
    Robotics
    """

    config_class = RivetWidowXCoreRobotConfig
    name = "rivet_widowxcore_robot"
    arms_class = BiWidowXCoreFollowerRobot


class RivetWidowXProRobot(RivetWidowXRobot):
    """
    [Rivet with WidowX Pro Follower Arms](https://www.trossenrobotics.com/rivet) by Trossen
    Robotics
    """

    config_class = RivetWidowXProRobotConfig
    name = "rivet_widowxpro_robot"
    arms_class = BiWidowXProFollowerRobot
