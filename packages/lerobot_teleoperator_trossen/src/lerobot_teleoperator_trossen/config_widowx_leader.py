from dataclasses import dataclass, field
from enum import Enum

import numpy as np
from lerobot.teleoperators.config import TeleoperatorConfig


class WidowXLeaderModel(str, Enum):
    CORE = "core"
    GLIDE_LEFT = "glide_left"
    GLIDE_RIGHT = "glide_right"
    WXAI = "wxai"

@TeleoperatorConfig.register_subclass("widowx_leader_teleop")
@dataclass
class WidowXLeaderTeleopConfig(TeleoperatorConfig):
    # IP address of the arm
    ip_address: str

    # Model of the WidowX arm.
    model: WidowXLeaderModel

    # Joint names for the WidowX leader arm
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

    # "Staged" positions in rad for the arm and m for the gripper. This does nothing for
    #  the GLIDEs.
    #
    # The robot will move to these positions when first started and before the arm is sent to the
    # sleep position.
    staged_positions: list[float] = field(
        default_factory=lambda: [0, 0, 0, 0, 0, 0, 0]
    )


    # [ONLY GLIDE] The effort that the GLIDE trigger maintains against the finger.
    glide_trigger_effort: float = 6.5
