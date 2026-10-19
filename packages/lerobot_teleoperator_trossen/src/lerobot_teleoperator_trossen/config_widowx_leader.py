from dataclasses import dataclass, field

from lerobot.teleoperators.config import TeleoperatorConfig


@dataclass
class WidowXLeaderTeleopConfig(TeleoperatorConfig):
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

    # "Staged" positions in rad for the arm and m for the gripper.
    #
    # The robot will move to these positions when first started and before the arm is sent to the
    # sleep position.
    staged_positions: list[float] = field(
        default_factory=lambda: [0, 0, 0, 0, 0, 0, 0]
    )


@TeleoperatorConfig.register_subclass("widowxcore_leader_teleop")
@dataclass
class WidowXCoreLeaderTeleopConfig(WidowXLeaderTeleopConfig):
    # All other configuration is in WidowXLeaderTeleopConfig
    pass

