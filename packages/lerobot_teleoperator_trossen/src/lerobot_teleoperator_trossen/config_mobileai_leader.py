from dataclasses import dataclass

from lerobot_teleoperator_trossen.config_bi_widowxai_leader import (
    BiWidowXAILeaderRobotConfig,
)

from lerobot.teleoperators.config import TeleoperatorConfig


@TeleoperatorConfig.register_subclass("mobileai_leader_teleop")
@dataclass
class MobileAILeaderTeleopConfig(BiWidowXAILeaderRobotConfig):
    pass
