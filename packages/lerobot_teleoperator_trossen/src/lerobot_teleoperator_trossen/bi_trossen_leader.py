from lerobot.teleoperators.teleoperator import Teleoperator

from lerobot_teleoperator_trossen.config_bi_trossen_leader import (
    BiTrossenLeaderRobotConfig,
)


class BiTrossenLeaderRobot(Teleoperator):
    """
    Abstract base for bimanual Trossen Robotics leaders (WidowX and Glide)
    """

    def __init__(self, config: BiTrossenLeaderRobotConfig):
        super().__init__(config)
        self.config = config

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
