import logging

import lerobot.teleoperators.utils
from lerobot.teleoperators import Teleoperator, TeleoperatorConfig

logger = logging.getLogger(__name__)


def make_teleoperator_from_config(config: TeleoperatorConfig) -> Teleoperator:
    logger.info(f"Creating teleoperator from config: {config}")
    try:
        return lerobot.teleoperators.utils.make_teleoperator_from_config(config)
    except ValueError:
        logger.info("Custom teleoperator type detected, creating specific teleoperator.")
        if config.type == "widowxai_leader":
            from .widowxai_leader import WidowXAILeader

            return WidowXAILeader(config)
        elif config.type == "bi_widowxai_leader":
            from .bi_widowxai_leader import BiWidowXAILeader

            return BiWidowXAILeader(config)
        else:
            raise ValueError(config.type) from None
