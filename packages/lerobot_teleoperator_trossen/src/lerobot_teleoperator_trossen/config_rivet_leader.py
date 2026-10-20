from dataclasses import dataclass

from lerobot.teleoperators.config import TeleoperatorConfig

from lerobot_teleoperator_trossen.config_bi_glide_leader import (
    BiGlideLeaderRobotConfig,
)


@TeleoperatorConfig.register_subclass("bi_rivet_glide_leader_teleop")
@dataclass
class RivetGlideLeaderTeleopConfig(BiGlideLeaderRobotConfig):

    # Maximum linear velocity that can be commanded (meters/second).
    max_linear_velocity: float = 0.8

    # Maximum angular velocity that can be commanded (radians/second).
    max_angular_velocity: float = 1.0

    # Maximum lift velocity that can be commanded (meters/second).
    max_lift_velocity: float = 0.2

    # Linear Velocities set to 0 if input is less then this value (meters/second).
    linear_deadzone: float = 0.01

    # Angular Velocities set to 0 if input is less then this value (radians/second).
    angular_deadzone: float = 0.05