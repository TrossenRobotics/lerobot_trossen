import logging
import time
from typing import Any

from lerobot.cameras.utils import make_cameras_from_configs
from lerobot.robots.robot import Robot

from lerobot_robot_trossen.config_bi_widowx_follower import (
    BiWidowXFollowerRobotConfig, BiWidowXCoreFollowerRobotConfig, BiWidowXHeavyFollowerRobotConfig,
    BiWidowXProFollowerRobotConfig,
)
from lerobot_robot_trossen.widowx_follower import (
    WidowXFollower, WidowXCoreFollower, WidowXHeavyFollower, WidowXProFollower,
)

logger = logging.getLogger(__name__)


class BiWidowXFollowerRobot(Robot):
    """
    [Bimanual WidowX Follower Arms](https://www.trossenrobotics.com/widowx) Abstract class by
    Trossen Robotics
    """

    def __init__(self, config: BiWidowXFollowerRobotConfig):
        super().__init__(config)
        self.config = config

        left_arm_config = self.arm_class.config_class(
            id=f"{config.id}_left" if config.id else None,
            ip_address=config.left_arm_ip_address,
            max_relative_target=config.left_arm_max_relative_target,
            min_time_to_move_multiplier=config.min_time_to_move_multiplier,
            loop_rate=config.loop_rate,
            include_velocity=config.include_velocity,
            include_effort=config.include_effort,
            include_external_effort=config.include_external_effort,
            cameras={},
            joint_names=config.left_arm_joint_names,
            staged_positions=config.left_arm_staged_positions,
        )

        right_arm_config = self.arm_class.config_class(
            id=f"{config.id}_right" if config.id else None,
            ip_address=config.right_arm_ip_address,
            max_relative_target=config.right_arm_max_relative_target,
            min_time_to_move_multiplier=config.min_time_to_move_multiplier,
            loop_rate=config.loop_rate,
            include_velocity=config.include_velocity,
            include_effort=config.include_effort,
            include_external_effort=config.include_external_effort,
            cameras={},
            joint_names=config.right_arm_joint_names,
            staged_positions=config.right_arm_staged_positions,
        )

        self.left_arm = self.arm_class(left_arm_config)
        self.right_arm = self.arm_class(right_arm_config)

        self.cameras = make_cameras_from_configs(config.cameras)

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
        # Derive from each arm (sub-arms have no cameras of their own) so that the per-joint
        # velocity/effort flags are reflected automatically, then add the shared cameras.
        return {
            **self.left_arm.observation_features,
            **self.right_arm.observation_features,
            **self._cameras_ft,
        }

    @property
    def action_features(self) -> dict[str, type]:
        return {**self.left_arm.action_features, **self.right_arm.action_features}

    @property
    def is_connected(self) -> bool:
        return (
            self.left_arm.is_connected
            and self.right_arm.is_connected
            and all(cam.is_connected for cam in self.cameras.values())
        )

    def connect(self, calibrate: bool = True) -> None:
        self.left_arm.connect(calibrate)
        self.right_arm.connect(calibrate)

        for cam in self.cameras.values():
            cam.connect()

    @property
    def is_calibrated(self) -> bool:
        # Trossen Arm robots do not require calibration but we check both arms for consistency
        return self.left_arm.is_calibrated and self.right_arm.is_calibrated

    def calibrate(self) -> None:
        # Trossen Arm robots do not require calibration but we call calibrate on both arms for
        # consistency
        self.left_arm.calibrate()
        self.right_arm.calibrate()

    def configure(self) -> None:
        # Set the arm to position control mode
        self.left_arm.configure()
        self.right_arm.configure()

    def get_observation(self) -> dict[str, Any]:
        obs_dict = {
            **self.left_arm.get_observation(),
            **self.right_arm.get_observation(),
        }

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
        # Route each key to the arm whose joint names it belongs to
        left_action = {
            key: value for key, value in action.items() if key in self.left_arm.action_features
        }
        right_action = {
            key: value for key, value in action.items() if key in self.right_arm.action_features
        }

        return {
            **self.left_arm.send_action(left_action),
            **self.right_arm.send_action(right_action),
        }

    def disconnect(self):
        self.left_arm.disconnect()
        self.right_arm.disconnect()

        for cam in self.cameras.values():
            cam.disconnect()


class BiWidowXCoreFollowerRobot(BiWidowXFollowerRobot):
    """
    [Bimanual WidowX Core Follower Arms](https://www.trossenrobotics.com/workbench) by Trossen 
    Robotics
    """

    config_class = BiWidowXCoreFollowerRobotConfig
    name = "bi_widowxcore_follower_robot"
    arm_class = WidowXCoreFollower


class BiWidowXProFollowerRobot(BiWidowXFollowerRobot):
    """
    [Bimanual WidowX Pro Follower Arms](https://www.trossenrobotics.com/workbench) by Trossen 
    Robotics
    """

    config_class = BiWidowXProFollowerRobotConfig
    name = "bi_widowxpro_follower_robot"
    arm_class = WidowXProFollower


class BiWidowXHeavyFollowerRobot(BiWidowXFollowerRobot):
    """
    [Bimanual WidowX Heavy Follower Arms](https://www.trossenrobotics.com/workbench) by Trossen
    Robotics
    """

    config_class = BiWidowXHeavyFollowerRobotConfig
    name = "bi_widowxheavy_follower_robot"
    arm_class = WidowXHeavyFollower
