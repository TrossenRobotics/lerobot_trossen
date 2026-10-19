from lerobot_robot_trossen.bi_widowx_follower import BiWidowXFollowerRobot
from lerobot_robot_trossen.config_bi_widowxai_follower import BiWidowXAIFollowerRobotConfig
from lerobot_robot_trossen.widowxai_follower import WidowXAIFollower


class BiWidowXAIFollowerRobot(BiWidowXFollowerRobot):
    """
    [Bimanual WidowX AI Follower Arms](https://www.trossenrobotics.com/widowx-ai) by Trossen
    Robotics
    """

    config_class = BiWidowXAIFollowerRobotConfig
    name = "bi_widowxai_follower_robot"
    arm_class = WidowXAIFollower
