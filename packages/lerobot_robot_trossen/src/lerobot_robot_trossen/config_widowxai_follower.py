from dataclasses import dataclass, field

import numpy as np
from lerobot.cameras import CameraConfig
from lerobot.robots.config import RobotConfig


@RobotConfig.register_subclass("widowxai_follower_robot")
@dataclass
class WidowXAIFollowerRobotConfig(RobotConfig):
    # IP address of the arm
    ip_address: str

    # `max_relative_target` limits the magnitude of the relative positional target vector for
    # safety purposes. Set this to a positive scalar to have the same value for all motors, or a
    # list that is the same length as the number of motors in your follower arms.
    max_relative_target: float | None = 5.0

    # Multiplier for computing minimum time (in seconds) for the arm to reach a target position.
    # The final goal time is computed as: min_time_to_move = multiplier / fps.
    # A smaller multiplier results in faster (but potentially jerky) motion.
    # A larger multiplier results in smoother motion but with increased lag.
    # A recommended starting value is 3.0.
    min_time_to_move_multiplier: float = 3.0

    # Control loop rate in Hz
    loop_rate: int = 30

    # cameras
    cameras: dict[str, CameraConfig] = field(default_factory=dict)
    # Troubleshooting: If one of your IntelRealSense cameras freeze during
    # data recording due to bandwidth limit, you might need to plug the camera
    # on another USB hub or PCIe card.

    # Joint names for the WidowX AI follower arm
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
    staged_positions: list[float] = field(
        default_factory=lambda: [0, np.pi / 3, np.pi / 6, np.pi / 5, 0, 0, 0]
    )
