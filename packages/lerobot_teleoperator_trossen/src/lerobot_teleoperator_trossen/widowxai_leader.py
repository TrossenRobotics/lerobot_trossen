import trossen_arm

from lerobot_teleoperator_trossen.config_widowxai_leader import (
    WidowXAILeaderTeleopConfig,
)
from lerobot_teleoperator_trossen.widowx_leader import WidowXLeaderTeleop


class WidowXAILeaderTeleop(WidowXLeaderTeleop):
    """
    [WidowX AI](https://www.trossenrobotics.com/widowx-ai) by Trossen Robotics
    """

    config_class = WidowXAILeaderTeleopConfig
    name = "widowxai_leader_teleop"

    def _configure_driver(self) -> None:
        self.driver.configure(
            model=trossen_arm.Model.wxai_v0,
            end_effector=trossen_arm.StandardEndEffector.wxai_v0_leader,
            serv_ip=self.config.ip_address,
            clear_error=True,
        )
