from lerobot_teleoperator_trossen.bi_trossen_leader import BiTrossenLeaderRobot
from lerobot_teleoperator_trossen.config_bi_widowx_leader import (
    BiWidowXCoreLeaderRobotConfig,
    BiWidowXLeaderRobotConfig,
)
from lerobot_teleoperator_trossen.widowx_leader import WidowXCoreLeaderTeleop


class BiWidowXLeaderRobot(BiTrossenLeaderRobot):
    """
    [Bimanual WidowX Leader Arms](https://www.trossenrobotics.com/widowx) Abstract class by Trossen
    Robotics
    """

    def __init__(self, config: BiWidowXLeaderRobotConfig):
        super().__init__(config)

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


class BiWidowXCoreLeaderRobot(BiWidowXLeaderRobot):
    """
    [Bimanual WidowX Core Leader Arms](https://www.trossenrobotics.com/workbench) by Trossen
    Robotics
    """

    config_class = BiWidowXCoreLeaderRobotConfig
    name = "bi_widowxcore_leader_teleop"
    left_arm_class = WidowXCoreLeaderTeleop
    right_arm_class = WidowXCoreLeaderTeleop
