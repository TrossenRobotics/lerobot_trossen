from dataclasses import dataclass, field

from lerobot.cameras import CameraConfig
from lerobot.robots.config import RobotConfig


# Shared configuration for all WidowX followers.
@dataclass
class WidowXFollowerConfig(RobotConfig):
    # IP address of the arm
    ip_address: str

    # `max_relative_target` limits the magnitude of the relative positional target vector for
    # safety purposes. Set this to a positive scalar to have the same value for all motors
    max_relative_target: float | None = 0.2

    # Multiplier for computing minimum time (in seconds) for the arm to reach a target position.
    # The final goal time is computed as: min_time_to_move = multiplier / fps.
    # A smaller multiplier results in faster (but potentially jerky) motion.
    # A larger multiplier results in smoother motion but with increased lag.
    # A recommended starting value is 3.0.
    min_time_to_move_multiplier: float = 3.0

    # Control loop rate in Hz
    loop_rate: int = 30

    # Include per-joint velocity (`.vel`) in observations.
    include_velocity: bool = False

    # Include per-joint effort (`.eff`) in observations. This is the total motor effort, combining
    # gravity, friction, and any external load. Measured in Nm for the arm joints and N for the
    # gripper carriage. Nonzero even when the arm is holding still against gravity.
    include_effort: bool = False

    # Include per-joint external effort (`.ext_eff`) in observations. This is the estimated
    # externally applied effort, after gravity and friction compensation. Measured in Nm for the
    # arm joints and N for the gripper carriage. Useful for contact and force sensing; an unloaded
    # arm reports values near zero.
    include_external_effort: bool = False

    # cameras
    cameras: dict[str, CameraConfig] = field(default_factory=dict)
    # Troubleshooting: If one of your IntelRealSense cameras freeze during
    # data recording due to bandwidth limit, you might need to plug the camera
    # on another USB hub or PCIe card.

    # Joint names for the WidowX follower arm
    joint_names: list[str] = field(
        default_factory=lambda: [
            "joint_0",
            "joint_1",
            "joint_2",
            "joint_3",
            "joint_4",
            "joint_5",
            "left_carriage_joint",
        ]
    )

    # "Staged" positions in rad for the arm and m for the gripper
    #
    # The robot will move to these positions when first started and before the arm is sent to the
    # sleep position.
    staged_positions: list[float] = field(default_factory=lambda: [0, 0, 0, 0, 0, 0, 0])


@RobotConfig.register_subclass("widowxcore_follower_robot")
@dataclass
class WidowXCoreFollowerConfig(WidowXFollowerConfig):
    pass


@RobotConfig.register_subclass("widowxpro_follower_robot")
@dataclass
class WidowXProFollowerConfig(WidowXFollowerConfig):
    pass


@RobotConfig.register_subclass("widowxheavy_follower_robot")
@dataclass
class WidowXHeavyFollowerConfig(WidowXFollowerConfig):
    pass
