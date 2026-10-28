from dataclasses import dataclass, field

from lerobot.teleoperators.config import TeleoperatorConfig

from lerobot_teleoperator_trossen.config_bi_trossen_leader import (
    BiTrossenLeaderRobotConfig,
)


# Shared configuration for all bimanual WidowX leaders.
@dataclass
class BiWidowXLeaderRobotConfig(BiTrossenLeaderRobotConfig):
    # IP addresses and joint names are in BiTrossenLeaderRobotConfig

    # "Staged" positions in rad for the arm and m for the gripper
    #
    # The arms will move to these positions when first started and before they are sent to the
    # sleep position.
    left_arm_staged_positions: list[float] = field(
        default_factory=lambda: [0, 0, 0, 0, 0, 0, 0]
    )
    right_arm_staged_positions: list[float] = field(
        default_factory=lambda: [0, 0, 0, 0, 0, 0, 0]
    )


@TeleoperatorConfig.register_subclass("bi_widowxcore_leader_teleop")
@dataclass
class BiWidowXCoreLeaderRobotConfig(BiWidowXLeaderRobotConfig):
    # All other configuration is in BiWidowXLeaderRobotConfig
    pass
