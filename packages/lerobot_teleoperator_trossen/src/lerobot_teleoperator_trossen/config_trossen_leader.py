from dataclasses import dataclass, field

from lerobot.teleoperators.config import TeleoperatorConfig


# Shared configuration for all Trossen leader arms (WidowX and Glide).
@dataclass
class TrossenLeaderTeleopConfig(TeleoperatorConfig):
    # IP address of the arm
    ip_address: str

    # Joint names for the leader arm
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
