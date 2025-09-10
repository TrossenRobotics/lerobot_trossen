import logging
import time
from functools import cached_property
from typing import Any

import trossen_arm
from lerobot.cameras.utils import make_cameras_from_configs
from lerobot.errors import DeviceAlreadyConnectedError, DeviceNotConnectedError
from lerobot.robots.robot import Robot
from lerobot.robots.utils import ensure_safe_goal_position

from .config_widowxai_follower import WidowXAIFollowerConfig

logger = logging.getLogger(__name__)


class WidowXAIFollower(Robot):
    """
    [WidowX AI](https://www.trossenrobotics.com/widowx-ai) by Trossen Robotics
    """

    config_class = WidowXAIFollowerConfig
    name = "widowxai_follower"

    def __init__(self, config: WidowXAIFollowerConfig):
        super().__init__(config)
        self.config = config

        self.driver = trossen_arm.TrossenArmDriver()
        self.cameras = make_cameras_from_configs(config.cameras)
        self.min_time_to_move = config.min_time_to_move_multiplier / self.config.loop_rate

    @property
    def _joint_ft(self) -> dict[str, type]:
        return {f"{joint_name}.pos": float for joint_name in self.config.joint_names}

    @property
    def _cameras_ft(self) -> dict[str, tuple]:
        return {
            cam: (self.config.cameras[cam].height, self.config.cameras[cam].width, 3)
            for cam in self.cameras
        }

    @cached_property
    def observation_features(self) -> dict[str, type | tuple]:
        return {**self._joint_ft, **self._cameras_ft}

    @cached_property
    def action_features(self) -> dict[str, type]:
        return self._joint_ft

    @property
    def is_connected(self) -> bool:
        return self.driver.get_is_configured() and all(
            cam.is_connected for cam in self.cameras.values()
        )

    def connect(self, calibrate: bool = True) -> None:
        if self.is_connected:
            raise DeviceAlreadyConnectedError(f"{self} already connected")

        self.driver.configure(
            model=trossen_arm.Model.wxai_v0,
            end_effector=trossen_arm.StandardEndEffector.wxai_v0_follower,
            serv_ip=self.config.ip_address,
            clear_error=True,
        )
        if not self.is_calibrated and calibrate:
            self.calibrate()

        for cam in self.cameras.values():
            cam.connect()

        self.configure()
        logger.info(f"{self} connected.")

    @property
    def is_calibrated(self) -> bool:
        # Trossen Arm robots do not require calibration
        return True

    def calibrate(self) -> None:
        # Trossen Arm robots do not require calibration
        pass

    def configure(self) -> None:
        # Set the arm to position control mode
        self.driver.set_all_modes(trossen_arm.Mode.position)
        self.driver.set_all_positions(
            self.config.staged_positions,
            goal_time=2.0,
            blocking=True,
        )

    def get_observation(self) -> dict[str, Any]:
        if not self.is_connected:
            raise DeviceNotConnectedError(f"{self} is not connected.")

        # Create observation dictionary with joint positions, velocities, and efforts
        start = time.perf_counter()

        robot_all_joint_outputs = self.driver.get_robot_output().joint.all
        obs_dict = {}
        obs_dict.update(
            {
                f"{joint_name}.pos": pos
                for joint_name, pos in zip(
                    self.config.joint_names,
                    robot_all_joint_outputs.positions,
                    strict=True,
                )
            }
        )
        obs_dict.update(
            {
                f"{joint_name}.vel": vel
                for joint_name, vel in zip(
                    self.config.joint_names,
                    robot_all_joint_outputs.velocities,
                    strict=True,
                )
            }
        )
        obs_dict.update(
            {
                f"{joint_name}.eff": eff
                for joint_name, eff in zip(
                    self.config.joint_names,
                    robot_all_joint_outputs.efforts,
                    strict=True,
                )
            }
        )

        dt_ms = (time.perf_counter() - start) * 1e3
        logger.debug(f"{self} read state: {dt_ms:.1f}ms")

        # Capture images from cameras
        for cam_key, cam in self.cameras.items():
            start = time.perf_counter()
            obs_dict[cam_key] = cam.async_read()
            dt_ms = (time.perf_counter() - start) * 1e3
            logger.debug(f"{self} read {cam_key}: {dt_ms:.1f}ms")

        return obs_dict

    def send_action(self, action: dict[str, Any]) -> dict[str, Any]:
        """Command arm to move to a target joint configuration.

        The relative action magnitude may be clipped depending on the configuration parameter
        `max_relative_target`. In this case, the action sent differs from original action.
        Thus, this function always returns the action actually sent.

        Raises:
            RobotDeviceNotConnectedError: if robot is not connected.

        Returns:
            the action sent to the motors, potentially clipped.
        """
        if not self.is_connected:
            raise DeviceNotConnectedError(f"{self} is not connected.")

        goal_pos = {
            key.removesuffix(".pos"): val for key, val in action.items() if key.endswith(".pos")
        }

        # Cap goal position when too far away from present position.
        # /!\ Slower fps expected due to reading from the follower.
        if self.config.max_relative_target is not None:
            present_pos = dict(
                zip(self.config.joint_names, self.driver.get_all_positions(), strict=False)
            )
            goal_present_pos = {key: (g_pos, present_pos[key]) for key, g_pos in goal_pos.items()}
            goal_pos = ensure_safe_goal_position(goal_present_pos, self.config.max_relative_target)

        # Send goal position to the arm
        self.driver.set_all_positions(
            goal_positions=[goal_pos[joint_name] for joint_name in self.config.joint_names],
            goal_time=self.min_time_to_move,
            blocking=False,
        )
        return {f"{motor}.pos": val for motor, val in goal_pos.items()}

    def disconnect(self):
        if not self.is_connected:
            raise DeviceNotConnectedError(f"{self} is not connected.")

        # Move the arm to the staged positions before disconnecting
        self.driver.set_all_positions(
            self.config.staged_positions,
            goal_time=2.0,
            blocking=True,
        )
        # Move the arm to the sleep position (all positions to 0.0)
        self.driver.set_all_positions(
            [0.0] * len(self.config.joint_names),
            goal_time=2.0,
            blocking=True,
        )

        self.driver.cleanup()
        for cam in self.cameras.values():
            cam.disconnect()

        logger.info(f"{self} disconnected.")
