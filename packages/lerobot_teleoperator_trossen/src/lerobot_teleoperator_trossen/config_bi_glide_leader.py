from dataclasses import dataclass, field

from lerobot.teleoperators.config import TeleoperatorConfig


@TeleoperatorConfig.register_subclass("bi_glide_leader_teleop")
@dataclass
class BiGlideLeaderRobotConfig(TeleoperatorConfig):
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

    # The effort (N) that each Glide trigger maintains against the finger.
    left_arm_glide_trigger_effort: float = 6.5
    right_arm_glide_trigger_effort: float = 6.5
