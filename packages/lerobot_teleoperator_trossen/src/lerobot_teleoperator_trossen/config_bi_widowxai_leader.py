from dataclasses import dataclass, field

import numpy as np
from lerobot.teleoperators.config import TeleoperatorConfig

from lerobot_teleoperator_trossen.config_bi_widowx_leader import BiWidowXLeaderRobotConfig


@TeleoperatorConfig.register_subclass("bi_widowxai_leader_teleop")
@dataclass
class BiWidowXAILeaderRobotConfig(BiWidowXLeaderRobotConfig):
    # All other configuration is in BiWidowXLeaderRobotConfig

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
