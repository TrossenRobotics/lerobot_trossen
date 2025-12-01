import logging
from functools import cached_property

from lerobot_teleoperator_trossen.config_mobileai_leader import (
    MobileAILeaderTeleopConfig,
)
from lerobot_teleoperator_trossen.bi_widowxai_leader import BiWidowXAILeaderRobot
from lerobot_robot_trossen.mobileai import get_latest_base_velocity

logger = logging.getLogger(__name__)


class MobileAILeaderTeleop(BiWidowXAILeaderRobot):
    """
    [Mobile AI](https://www.trossenrobotics.com/mobile-ai) by Trossen Robotics
    """

    config_class = MobileAILeaderTeleopConfig
    name = "mobileai_leader_teleop"

    def __init__(self, config: MobileAILeaderTeleopConfig):
        super().__init__(config)

    @cached_property
    def action_features(self) -> dict[str, type]:
        features = super().action_features
        features["x.vel"] = float
        features["theta.vel"] = float
        return features

    def get_action(self) -> dict[str, float]:
        action = super().get_action()
        action.update(get_latest_base_velocity())
        return action
