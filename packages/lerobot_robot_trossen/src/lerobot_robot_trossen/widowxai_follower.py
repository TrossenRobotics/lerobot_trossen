import trossen_arm

from lerobot_robot_trossen.config_widowxai_follower import WidowXAIFollowerConfig
from lerobot_robot_trossen.widowx_follower import WidowXFollower


class WidowXAIFollower(WidowXFollower):
    """
    [WidowX AI](https://www.trossenrobotics.com/widowx-ai) by Trossen Robotics
    """

    config_class = WidowXAIFollowerConfig
    name = "widowxai_follower_robot"

    def _configure_driver(self) -> None:
        self.driver.configure(
            model=trossen_arm.Model.wxai_v0,
            end_effector=trossen_arm.StandardEndEffector.wxai_v0_follower,
            serv_ip=self.config.ip_address,
            clear_error=True,
        )
