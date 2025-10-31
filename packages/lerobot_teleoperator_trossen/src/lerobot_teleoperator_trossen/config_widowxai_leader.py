from dataclasses import dataclass, field

import numpy as np
from lerobot.teleoperators.config import TeleoperatorConfig


@TeleoperatorConfig.register_subclass("widowxai_leader_teleop")
@dataclass
class WidowXAILeaderTeleopConfig(TeleoperatorConfig):
    # IP address of the arm
    ip_address: str

    # Joint names for the WidowX AI leader arm
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
