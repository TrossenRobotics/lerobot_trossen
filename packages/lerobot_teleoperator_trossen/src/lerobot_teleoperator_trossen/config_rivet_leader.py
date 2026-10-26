from dataclasses import dataclass

from lerobot.teleoperators.config import TeleoperatorConfig

from lerobot_teleoperator_trossen.config_bi_glide_leader import (
    BiGlideLeaderRobotConfig,
)


@TeleoperatorConfig.register_subclass("bi_rivet_glide_leader_teleop")
@dataclass
class RivetGlideLeaderTeleopConfig(BiGlideLeaderRobotConfig):
    # Maximum linear velocity that can be commanded (m/s).
    max_linear_velocity: float = 0.8

    # Maximum angular velocity that can be commanded (rad/s).
    max_angular_velocity: float = 1.0

    # Velocity the lift goal moves at while a lift button is held (m/s).
    max_lift_velocity: float = 0.2

    # Range of lift positions that can be commanded (m above the bottom soft bound).
    min_lift_position: float = 0.0
    max_lift_position: float = 0.86

    # Lift position the leader starts at, should match the robot's lift_staged_position (m).
    lift_staged_position: float = 0.5

    # Linear Velocities set to 0 if input is less then this value (m/s).
    linear_deadzone: float = 0.01

    # Angular Velocities set to 0 if input is less then this value (rad/s).
    angular_deadzone: float = 0.05
