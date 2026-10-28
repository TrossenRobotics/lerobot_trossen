from dataclasses import dataclass, field

import numpy as np
from lerobot.cameras import CameraConfig
from lerobot.robots.config import RobotConfig


# Shared configuration for all bimanual WidowX followers.
@dataclass
class BiWidowXFollowerRobotConfig(RobotConfig):
    # IP address of the arms
    left_arm_ip_address: str
    right_arm_ip_address: str

    # `max_relative_target` limits the magnitude of the relative positional target vector for
    # safety purposes. Set this to a positive scalar to have the same value for all motors
    left_arm_max_relative_target: float | None = None
    right_arm_max_relative_target: float | None = None

    # Multiplier for computing minimum time (in seconds) for the arm to reach a target position.
    # The final goal time is computed as: min_time_to_move = multiplier / fps.
    # A smaller multiplier results in faster (but potentially jerky) motion.
    # A larger multiplier results in smoother motion but with increased lag.
    # A recommended starting value is 3.0.
    # This value is shared between both arms.
    min_time_to_move_multiplier: float = 3.0

    # Expected control loop rate in Hz (shared between both arms).
    loop_rate: int = 30

    # Include per-joint velocity (`.vel`) in observations (shared between both arms).
    include_velocity: bool = False

    # Include per-joint effort (`.eff`) in observations. This is the total motor effort, combining
    # gravity, friction, and any external load. Measured in Nm for the arm joints and N for the
    # gripper carriage. Nonzero even when the arm is holding still against gravity. Shared between
    # both arms.
    include_effort: bool = False

    # Include per-joint external effort (`.ext_eff`) in observations. This is the estimated
    # externally applied effort, after gravity and friction compensation. Measured in Nm for the
    # arm joints and N for the gripper carriage. Useful for contact and force sensing; an unloaded
    # arm reports values near zero. Shared between both arms.
    include_external_effort: bool = False

    # cameras (shared between both arms)
    cameras: dict[str, CameraConfig] = field(default_factory=dict)
    # Troubleshooting: If one of your RealSense cameras freeze during
    # data recording due to bandwidth limit, you might need to plug the camera
    # on another USB hub or PCIe card.

    # Joint names for each arm.
    left_arm_joint_names: list[str] = field(
        default_factory=lambda: [
            "left_joint_0",
            "left_joint_1",
            "left_joint_2",
            "left_joint_3",
            "left_joint_4",
            "left_joint_5",
            "left_left_carriage_joint",
        ]
    )
    right_arm_joint_names: list[str] = field(
        default_factory=lambda: [
            "right_joint_0",
            "right_joint_1",
            "right_joint_2",
            "right_joint_3",
            "right_joint_4",
            "right_joint_5",
            "right_left_carriage_joint",
        ]
    )

    # "Staged" positions in rad for the arm and m for the gripper
    #
    # The arms will move to these positions when first started and before they are sent to the
    # sleep position.
    left_arm_staged_positions: list[float] = field(
        default_factory=lambda: [0, 0, 0, 0, 0, -np.pi / 4, 0]
    )
    right_arm_staged_positions: list[float] = field(
        default_factory=lambda: [0, 0, 0, 0, 0, np.pi / 4, 0]
    )


@RobotConfig.register_subclass("bi_widowxcore_follower_robot")
@dataclass
class BiWidowXCoreFollowerRobotConfig(BiWidowXFollowerRobotConfig):
    # All other configuration is in BiWidowXFollowerRobotConfig
    pass


@RobotConfig.register_subclass("bi_widowxpro_follower_robot")
@dataclass
class BiWidowXProFollowerRobotConfig(BiWidowXFollowerRobotConfig):
    # All other configuration is in BiWidowXFollowerRobotConfig
    pass


@RobotConfig.register_subclass("bi_widowxheavy_follower_robot")
@dataclass
class BiWidowXHeavyFollowerRobotConfig(BiWidowXFollowerRobotConfig):
    # All other configuration is in BiWidowXFollowerRobotConfig
    pass
