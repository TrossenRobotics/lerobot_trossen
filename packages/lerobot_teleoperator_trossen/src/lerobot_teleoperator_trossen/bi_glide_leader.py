from lerobot_teleoperator_trossen.bi_trossen_leader import BiTrossenLeaderRobot
from lerobot_teleoperator_trossen.config_bi_glide_leader import BiGlideLeaderRobotConfig
from lerobot_teleoperator_trossen.glide_leader import (
    GlideLeftLeaderTeleop,
    GlideRightLeaderTeleop,
)


class BiGlideLeaderRobot(BiTrossenLeaderRobot):
    """
    [Bimanual Glide Leaders](https://www.trossenrobotics.com/glide-cockpit) by Trossen Robotics
    """

    config_class = BiGlideLeaderRobotConfig
    name = "bi_glide_leader_teleop"
    left_arm_class = GlideLeftLeaderTeleop
    right_arm_class = GlideRightLeaderTeleop

    def __init__(self, config: BiGlideLeaderRobotConfig):
        super().__init__(config)

        left_arm_config = self.left_arm_class.config_class(
            id=f"{config.id}_left" if config.id else None,
            ip_address=config.left_arm_ip_address,
            joint_names=config.left_arm_joint_names,
            glide_trigger_effort=config.left_arm_glide_trigger_effort,
        )

        right_arm_config = self.right_arm_class.config_class(
            id=f"{config.id}_right" if config.id else None,
            ip_address=config.right_arm_ip_address,
            joint_names=config.right_arm_joint_names,
            glide_trigger_effort=config.right_arm_glide_trigger_effort,
        )

        self.left_arm = self.left_arm_class(left_arm_config)
        self.right_arm = self.right_arm_class(right_arm_config)
