import lerobot.robots.utils
from lerobot.robots import Robot, RobotConfig


def make_robot_from_config(config: RobotConfig) -> Robot:
    try:
        return lerobot.robots.utils.make_robot_from_config(config)
    except ValueError:
        if config.type == "widowxai_follower":
            from .widowxai_follower import WidowXAIFollower

            return WidowXAIFollower(config)
        elif config.type == "bi_widowxai_follower":
            from .bi_widowxai_follower import BiWidowXAIFollower

            return BiWidowXAIFollower(config)
        else:
            raise ValueError(config.type) from None
