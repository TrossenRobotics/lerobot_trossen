from dataclasses import dataclass

from lerobot_robot_trossen.config_bi_widowxai_follower import (
    BiWidowXAIFollowerRobotConfig,
)

from lerobot.robots.config import RobotConfig


@RobotConfig.register_subclass("mobileai_robot")
@dataclass
class MobileAIRobotConfig(BiWidowXAIFollowerRobotConfig):
    # Mobile AI uses the same configuration as BiWidowXAIFollowerRobotConfig.
    # The base of the kit does not require any configuration parameters.
    enable_base_motor_torque: bool = False
