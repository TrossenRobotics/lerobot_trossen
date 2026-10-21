from dataclasses import dataclass, field

from lerobot.teleoperators.config import TeleoperatorConfig


@dataclass
class GlideLeaderTeleopConfig(TeleoperatorConfig):
    # IP address of the arm
    ip_address: str

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

    # The effort that the Glide trigger maintains against the finger.
    glide_trigger_effort: float = 6.5


@TeleoperatorConfig.register_subclass("glideleft_leader_teleop")
@dataclass
class GlideLeftLeaderTeleopConfig(GlideLeaderTeleopConfig):
    # All other configuration is in GlideLeaderTeleopConfig
    pass


@TeleoperatorConfig.register_subclass("glideright_leader_teleop")
@dataclass
class GlideRightLeaderTeleopConfig(GlideLeaderTeleopConfig):
    # All other configuration is in GlideLeaderTeleopConfig
    pass
