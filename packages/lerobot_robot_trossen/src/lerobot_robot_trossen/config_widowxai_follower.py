from dataclasses import dataclass, field

import numpy as np
from lerobot.robots.config import RobotConfig

from lerobot_robot_trossen.config_widowx_follower import WidowXFollowerConfig

@RobotConfig.register_subclass("widowxai_follower_robot")
@dataclass
class WidowXAIFollowerConfig(WidowXFollowerConfig):
    # All other configuration is in WidowXFollowerConfig

    # "Staged" positions in rad for the arm and m for the gripper
    #
    # The robot will move to these positions when first started and before the arm is sent to the
    # sleep position.
    staged_positions: list[float] = field(
        default_factory=lambda: [0, np.pi / 3, np.pi / 6, np.pi / 5, 0, 0, 0]
    )
