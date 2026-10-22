from dataclasses import dataclass

from lerobot.teleoperators.config import TeleoperatorConfig

from lerobot_teleoperator_trossen.config_trossen_leader import TrossenLeaderTeleopConfig


@dataclass
class GlideLeaderTeleopConfig(TrossenLeaderTeleopConfig):
    # IP address and joint names are in TrossenLeaderTeleopConfig

    # The effort (N) that the Glide trigger maintains against the finger.
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
