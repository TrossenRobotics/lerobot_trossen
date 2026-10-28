import logging
import time
from functools import cached_property

from lerobot_teleoperator_trossen.config_rivet_leader import (
    RivetGlideLeaderTeleopConfig,
)
from lerobot_teleoperator_trossen.bi_glide_leader import BiGlideLeaderRobot

MIN_JOYSTICK = 0  # Joystick min value
MAX_JOYSTICK = 4095  # Joystick max value

logger = logging.getLogger(__name__)


def scale(value, val_min, val_max, scaled_min, scaled_max, scaled_deadzone=None):
    """Scale a value linearly from val_min..val_max onto scaled_min..scaled_max.

    The deadzone is applied to the scaled value, so it is expressed in output units.
    """

    scaled_val = (value - val_min) / (val_max - val_min) * (
        scaled_max - scaled_min
    ) + scaled_min

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

        # The Glide has no absolute lift input, so the buttons move this goal position
        self._lift_position = config.lift_staged_position
        self._last_lift_t = None

    @cached_property
    def action_features(self) -> dict[str, type]:
        features = super().action_features
        features["x.vel"] = float
        features["y.vel"] = float
        features["theta.vel"] = float
        features["lift.pos"] = float
        return features

    def get_action(self) -> dict[str, float]:
        action = super().get_action()

        left_input = self.left_arm.driver.get_input_report()
        right_input = self.right_arm.driver.get_input_report()
        right_up_btn = bool(right_input.buttons & (1 << 0))
        right_down_btn = bool(right_input.buttons & (1 << 2))

        action_base_x_vel = -scale(
            left_input.joystick_y,
            MIN_JOYSTICK,
            MAX_JOYSTICK,
            -self.config.max_linear_velocity,
            self.config.max_linear_velocity,
            self.config.linear_deadzone,
        )
        action_base_y_vel = -scale(
            left_input.joystick_x,
            MIN_JOYSTICK,
            MAX_JOYSTICK,
            -self.config.max_linear_velocity,
            self.config.max_linear_velocity,
            self.config.linear_deadzone,
        )
        action_base_theta_vel = scale(
            right_input.joystick_x,
            MIN_JOYSTICK,
            MAX_JOYSTICK,
            -self.config.max_angular_velocity,
            self.config.max_angular_velocity,
            self.config.angular_deadzone,
        )
        # Move the lift goal while a button is held, clamped to the configured range
        now = time.perf_counter()
        dt = 0.0 if self._last_lift_t is None else now - self._last_lift_t
        self._last_lift_t = now
        self._lift_position = min(
            max(
                self._lift_position
                + (right_up_btn - right_down_btn) * self.config.max_lift_velocity * dt,
                self.config.min_lift_position,
            ),
            self.config.max_lift_position,
        )

        action.update(
            {
                "x.vel": action_base_x_vel,
                "y.vel": action_base_y_vel,
                "theta.vel": action_base_theta_vel,
                "lift.pos": self._lift_position,
            }
        )
        return action
