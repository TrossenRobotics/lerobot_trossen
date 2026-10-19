import logging

import trossen_arm
from lerobot.utils.errors import DeviceNotConnectedError

from lerobot_teleoperator_trossen.config_glide_leader import (
    GlideLeftLeaderTeleopConfig, GlideRightLeaderTeleopConfig
)
from lerobot_teleoperator_trossen.widowx_leader import WidowXLeaderTeleop

logger = logging.getLogger(__name__)


class GlideLeaderTeleop(WidowXLeaderTeleop):
    """
    [Glide](https://www.trossenrobotics.com/glide-cockpit) Abstract class by Trossen Robotics
    """

    def configure(self) -> None:
        self.driver.set_all_modes(trossen_arm.Mode.effort)
        self.driver.set_gripper_effort(
            self.config.glide_trigger_effort,
            goal_time=0.0,
            blocking=True
        )

    def disconnect(self) -> None:
        if not self.is_connected:
            raise DeviceNotConnectedError(f"{self} is not connected.")

        self.driver.cleanup()
        logger.info(f"{self} disconnected.")

# TODO(@schromya): Add add proper end-effectors for each model when released

class GlideLeftLeaderTeleop(GlideLeaderTeleop):
    """
    [Glide](https://www.trossenrobotics.com/glide-cockpit) by Trossen Robotics
    """

    config_class = GlideLeftLeaderTeleopConfig
    name = "glideleft_leader_teleop"

    def _configure_driver(self) -> None:
        self.driver.configure(
            model=trossen_arm.Model.glide_left,
            end_effector=trossen_arm.StandardEndEffector.wxai_v0_leader,
            serv_ip=self.config.ip_address,
            clear_error=True,
        )


class GlideRightLeaderTeleop(GlideLeaderTeleop):
    """
    [Glide](https://www.trossenrobotics.com/glide-cockpit) by Trossen Robotics
    """

    config_class = GlideRightLeaderTeleopConfig
    name = "glideright_leader_teleop"

    def _configure_driver(self) -> None:
        self.driver.configure(
            model=trossen_arm.Model.glide_right,
            end_effector=trossen_arm.StandardEndEffector.wxai_v0_leader,
            serv_ip=self.config.ip_address,
            clear_error=True,
        )
