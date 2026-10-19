import logging

from lerobot.teleoperators.teleoperator import Teleoperator

from lerobot_teleoperator_trossen.config_bi_widowx_leader import (
    BiWidowXCoreLeaderRobotConfig,
    BiWidowXLeaderRobotConfig,
)
from lerobot_teleoperator_trossen.widowx_leader import WidowXCoreLeaderTeleop

logger = logging.getLogger(__name__)


class BiWidowXLeaderRobot(Teleoperator):
    """
    [Bimanual WidowX Leader Arms](https://www.trossenrobotics.com/widowx) Abstract class by Trossen
    Robotics
    """

    def __init__(self, config: BiWidowXLeaderRobotConfig):
        super().__init__(config)
        self.config = config

        left_arm_config = self.left_arm_class.config_class(
            id=f"{config.id}_left" if config.id else None,
            ip_address=config.left_arm_ip_address,
            joint_names=config.left_arm_joint_names,
            staged_positions=config.left_arm_staged_positions,
        )

        right_arm_config = self.right_arm_class.config_class(
            id=f"{config.id}_right" if config.id else None,
            ip_address=config.right_arm_ip_address,
            joint_names=config.right_arm_joint_names,
            staged_positions=config.right_arm_staged_positions,
        )

        self.left_arm = self.left_arm_class(left_arm_config)
        self.right_arm = self.right_arm_class(right_arm_config)

    @property
    def action_features(self) -> dict[str, type]:
        return {**self.left_arm.action_features, **self.right_arm.action_features}

    @property
    def feedback_features(self) -> dict[str, type]:
        # TODO(lukeschmitt-tr): Implement force feedback
        # Note that feedback is currently not implemented upstream huggingface/lerobot.
        return {}

    @property
    def is_connected(self) -> bool:
        return self.left_arm.is_connected and self.right_arm.is_connected

    def connect(self, calibrate: bool = True) -> None:
        self.left_arm.connect(calibrate)
        self.right_arm.connect(calibrate)

    @property
    def is_calibrated(self) -> bool:
        # Trossen Arm robots do not require calibration but we check both arms for consistency
        return self.left_arm.is_calibrated and self.right_arm.is_calibrated

    def calibrate(self) -> None:
        # Trossen Arm robots do not require calibration but we call calibrate on both arms for
        # consistency
        self.left_arm.calibrate()
        self.right_arm.calibrate()

    def configure(self) -> None:
        self.left_arm.configure()
        self.right_arm.configure()

    def get_action(self) -> dict[str, float]:
        return {**self.left_arm.get_action(), **self.right_arm.get_action()}

    def send_feedback(self, feedback: dict[str, float]) -> None:
        # Note that feedback is currently not implemented upstream huggingface/lerobot.
        left_feedback = {
            key: value for key, value in feedback.items() if key.startswith("left_")
        }
        right_feedback = {
            key: value for key, value in feedback.items() if key.startswith("right_")
        }

        if left_feedback:
            self.left_arm.send_feedback(left_feedback)
        if right_feedback:
            self.right_arm.send_feedback(right_feedback)

    def disconnect(self) -> None:
        self.left_arm.disconnect()
        self.right_arm.disconnect()


class BiWidowXCoreLeaderRobot(BiWidowXLeaderRobot):
    """
    [Bimanual WidowX Core Leader Arms](https://www.trossenrobotics.com/workbench) by Trossen
    Robotics
    """

    config_class = BiWidowXCoreLeaderRobotConfig
    name = "bi_widowxcore_leader_teleop"
    left_arm_class = WidowXCoreLeaderTeleop
    right_arm_class = WidowXCoreLeaderTeleop
