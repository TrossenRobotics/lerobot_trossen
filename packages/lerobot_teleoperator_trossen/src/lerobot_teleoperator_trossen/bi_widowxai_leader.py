from lerobot_teleoperator_trossen.bi_widowx_leader import BiWidowXLeaderRobot
from lerobot_teleoperator_trossen.config_bi_widowxai_leader import BiWidowXAILeaderRobotConfig
from lerobot_teleoperator_trossen.widowxai_leader import WidowXAILeaderTeleop


class BiWidowXAILeaderRobot(BiWidowXLeaderRobot):
    """
    [Bimanual WidowX AI Leader Arms](https://www.trossenrobotics.com/widowx-ai) by Trossen Robotics
    """

    config_class = BiWidowXAILeaderRobotConfig
    name = "bi_widowxai_leader_teleop"
    left_arm_class = WidowXAILeaderTeleop
    right_arm_class = WidowXAILeaderTeleop
