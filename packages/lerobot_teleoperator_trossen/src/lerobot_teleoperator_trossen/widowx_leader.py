import trossen_arm
from lerobot.utils.errors import DeviceNotConnectedError

from lerobot_teleoperator_trossen.config_widowx_leader import (
    WidowXCoreLeaderTeleopConfig,
)
from lerobot_teleoperator_trossen.trossen_leader import TrossenLeaderTeleop


class WidowXLeaderTeleop(TrossenLeaderTeleop):
    """
    [WidowX](https://www.trossenrobotics.com/widowx) Abstract class by Trossen Robotics
    """

    def configure(self) -> None:
        self.driver.set_all_modes(trossen_arm.Mode.position)
        # Move the arm to the staged positions
        self.driver.set_all_positions(
            self.config.staged_positions,
            goal_time=2.0,
            blocking=True,
        )

        self.driver.set_all_modes(trossen_arm.Mode.external_effort)
        # Set all external efforts to 0.0 to enable gravity compensation
        self.driver.set_all_external_efforts(
            [0.0] * len(self.config.joint_names),
            goal_time=0.0,
            blocking=True,
        )

    def disconnect(self) -> None:
        if not self.is_connected:
            raise DeviceNotConnectedError(f"{self} is not connected.")

        self.driver.set_all_modes(trossen_arm.Mode.position)
        # Move the arm to the staged positions before disconnecting
        self.driver.set_all_positions(
            self.config.staged_positions,
            goal_time=2.0,
            blocking=True,
        )
        # Move the arm to the sleep position (all positions to 0.0)
        self.driver.set_all_positions(
            [0.0] * len(self.config.joint_names),
            goal_time=2.0,
            blocking=True,
        )

        super().disconnect()


class WidowXCoreLeaderTeleop(WidowXLeaderTeleop):
    """
    [WidowX](https://www.trossenrobotics.com/widowx) by Trossen Robotics
    """

    config_class = WidowXCoreLeaderTeleopConfig
    name = "widowxcore_leader_teleop"

    def _configure_driver(self) -> None:
        self.driver.configure(
            model=trossen_arm.Model.core,
            end_effector=trossen_arm.StandardEndEffector.core_leader,
            serv_ip=self.config.ip_address,
            clear_error=True,
        )
