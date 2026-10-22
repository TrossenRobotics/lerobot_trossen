from dataclasses import dataclass, field

from lerobot.teleoperators.config import TeleoperatorConfig

from lerobot_teleoperator_trossen.config_trossen_leader import TrossenLeaderTeleopConfig


@dataclass
class WidowXLeaderTeleopConfig(TrossenLeaderTeleopConfig):
    # IP address and joint names are in TrossenLeaderTeleopConfig

    # "Staged" positions in rad for the arm and m for the gripper.
    #
    # The robot will move to these positions when first started and before the arm is sent to the
    # sleep position.
    staged_positions: list[float] = field(default_factory=lambda: [0, 0, 0, 0, 0, 0, 0])


@TeleoperatorConfig.register_subclass("widowxcore_leader_teleop")
@dataclass
class WidowXCoreLeaderTeleopConfig(WidowXLeaderTeleopConfig):
    # All other configuration is in WidowXLeaderTeleopConfig
    pass
