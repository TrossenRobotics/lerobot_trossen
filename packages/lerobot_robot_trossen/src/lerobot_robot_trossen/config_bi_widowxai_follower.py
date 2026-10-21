from dataclasses import dataclass, field

import numpy as np
from lerobot.robots.config import RobotConfig

from lerobot_robot_trossen.config_bi_widowx_follower import BiWidowXFollowerRobotConfig


@RobotConfig.register_subclass("bi_widowxai_follower_robot")
@dataclass
class BiWidowXAIFollowerRobotConfig(BiWidowXFollowerRobotConfig):
    # All other configuration is in BiWidowXFollowerRobotConfig

    # `max_relative_target` limits the magnitude of the relative positional target vector for
    # safety purposes. Set this to a positive scalar to have the same value for all motors
    left_arm_max_relative_target: float | None = None
    right_arm_max_relative_target: float | None = None

    # "Staged" positions in rad for the arm and m for the gripper
    #
    # The arms will move to these positions when first started and before they are sent to the
    # sleep position.
    left_arm_staged_positions: list[float] = field(
        default_factory=lambda: [0, np.pi / 3, np.pi / 6, np.pi / 5, 0, 0, 0]
    )
    right_arm_staged_positions: list[float] = field(
        default_factory=lambda: [0, np.pi / 3, np.pi / 6, np.pi / 5, 0, 0, 0]
    )
