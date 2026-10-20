import logging
from functools import cached_property

from lerobot_teleoperator_trossen.config_rivet_leader import (
    RivetGlideLeaderTeleopConfig,
)
from lerobot_teleoperator_trossen.bi_glide_leader import BiGlideLeaderRobot

MIN_JOYSTICK = 0        # Joystick min value
MAX_JOYSTICK = 4095     # Joystick max value

logger = logging.getLogger(__name__)

def scale(value, val_min, val_max, scaled_min, scaled_max, scaled_deadzone=None):
    """Scale a value linearly from val_min..val_max onto scaled_min..scaled_max.

    The deadzone is applied to the scaled value, so it is expressed in output units.
    """

    scaled_val = ((value - val_min) / (val_max - val_min) * (scaled_max - scaled_min) + scaled_min)

    if scaled_deadzone:
        if abs(scaled_val) < scaled_deadzone:
            return 0.0
    return scaled_val

class RivetGlideLeaderTeleop(BiGlideLeaderRobot):
    """
    [Rivet](https://www.trossenrobotics.com/rivet) and
    [Bimanual Glide](https://www.trossenrobotics.com/glide-cockpit) by Trossen Robotics
    """

    config_class = RivetGlideLeaderTeleopConfig
    name = "bi_rivet_glide_leader_teleop"

    def __init__(self, config: RivetGlideLeaderTeleopConfig):
        super().__init__(config)

    @cached_property
    def action_features(self) -> dict[str, type]:
        features = super().action_features
        features["x.vel"] = float
        features["y.vel"] = float
        features["theta.vel"] = float
        features["lift.vel"] = float
        return features


    def get_action(self) -> dict[str, float]:
        action = super().get_action()

        left_input = self.left_arm.get_input_report()
        right_input = self.right_arm.get_input_report()
        right_up_btn = bool(right_input.buttons & (1 << 0))
        right_down_btn = bool(right_input.buttons & (1 << 2))

        action_base_x_vel = -scale(left_input.joystick_y, MIN_JOYSTICK, MAX_JOYSTICK,
            -self.config.max_linear_velocity, self.config.max_linear_velocity,
            self.config.linear_deadzone)
        action_base_y_vel = -scale(left_input.joystick_x, MIN_JOYSTICK, MAX_JOYSTICK,
            -self.config.max_linear_velocity, self.config.max_linear_velocity,
            self.config.linear_deadzone)
        action_base_theta_vel = scale(right_input.joystick_x, MIN_JOYSTICK, MAX_JOYSTICK,
            -self.config.max_angular_velocity, self.config.max_angular_velocity,
            self.config.angular_deadzone)
        action_base_lift_vel = (right_up_btn - right_down_btn) * self.config.max_lift_velocity

        action.update({"x.vel": action_base_x_vel, "y.vel": action_base_y_vel,
            "theta.vel": action_base_theta_vel, "lift.vel": action_base_lift_vel,})
        return action
