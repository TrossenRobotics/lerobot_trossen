from dataclasses import dataclass, field

from lerobot.cameras import CameraConfig
from lerobot.robots.config import RobotConfig

from lerobot_robot_trossen.config_bi_widowx_follower import (
    BiWidowXFollowerRobotConfig,
)


# Configuration for a Rivet base without arms.
@RobotConfig.register_subclass("rivet_robot")
@dataclass
class RivetRobotConfig(RobotConfig):
    # cameras
    cameras: dict[str, CameraConfig] = field(default_factory=dict)

    # Lift position to move to on connect (m above the bottom soft bound).
    lift_staged_position: float = 0.5

    # Cruise velocity used when moving the lift to a commanded position (m/s).
    lift_velocity: float = 0.2


# Shared configuration for all Rivet robots with WidowX arms.
@dataclass
class RivetWidowXRobotConfig(RivetRobotConfig, BiWidowXFollowerRobotConfig):
    # All other configuration is in RivetRobotConfig and BiWidowXFollowerRobotConfig
    pass


@RobotConfig.register_subclass("rivet_widowxcore_robot")
@dataclass
class RivetWidowXCoreRobotConfig(RivetWidowXRobotConfig):
    # All other configuration is in RivetWidowXRobotConfig
    pass


@RobotConfig.register_subclass("rivet_widowxpro_robot")
@dataclass
class RivetWidowXProRobotConfig(RivetWidowXRobotConfig):
    # All other configuration is in RivetWidowXRobotConfig
    pass
