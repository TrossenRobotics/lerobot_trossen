from dataclasses import dataclass

from lerobot.teleoperators.config import TeleoperatorConfig


@TeleoperatorConfig.register_subclass("bi_widowxai_leader_teleop")
@dataclass
class BiWidowXAILeaderRobotConfig(TeleoperatorConfig):
    left_arm_ip_address: str
    right_arm_ip_address: str
