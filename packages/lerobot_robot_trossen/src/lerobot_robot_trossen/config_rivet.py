from dataclasses import dataclass

from lerobot_robot_trossen.config_bi_widowx_follower import (
    BiWidowXFollowerRobotConfig,
)

from lerobot.robots.config import RobotConfig


# Shared configuration for all Rivet robots.
@dataclass
class RivetRobotConfig(BiWidowXFollowerRobotConfig):
    # All other configuration is in BiWidowXFollowerRobotConfig
    pass


@RobotConfig.register_subclass("rivetcore_robot")
@dataclass
class RivetCoreRobotConfig(RivetRobotConfig):
    # All other configuration is in RivetRobotConfig
    pass


@RobotConfig.register_subclass("rivetpro_robot")
@dataclass
class RivetProRobotConfig(RivetRobotConfig):
    # All other configuration is in RivetRobotConfig
    pass