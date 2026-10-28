from dataclasses import dataclass, field

from lerobot.teleoperators.config import TeleoperatorConfig


# Shared configuration for all bimanual Trossen leaders (WidowX and Glide).
@dataclass
class BiTrossenLeaderRobotConfig(TeleoperatorConfig):
    # IP address of the arms
    left_arm_ip_address: str
    right_arm_ip_address: str

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
