from dataclasses import dataclass

from lerobot.teleoperators.config import TeleoperatorConfig

from lerobot_teleoperator_trossen.config_bi_trossen_leader import (
    BiTrossenLeaderRobotConfig,
)


@TeleoperatorConfig.register_subclass("bi_glide_leader_teleop")
@dataclass
class BiGlideLeaderRobotConfig(BiTrossenLeaderRobotConfig):
    # IP addresses and joint names are in BiTrossenLeaderRobotConfig

    # The effort (N) that each Glide trigger maintains against the finger.
    left_arm_glide_trigger_effort: float = 6.5
    right_arm_glide_trigger_effort: float = 6.5
