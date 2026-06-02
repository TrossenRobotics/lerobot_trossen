from dataclasses import dataclass, field

from lerobot.cameras import CameraConfig
from lerobot.robots.config import RobotConfig


@RobotConfig.register_subclass("bi_widowxai_follower_robot")
@dataclass
class BiWidowXAIFollowerRobotConfig(RobotConfig):
    # IP address of the arms
    left_arm_ip_address: str
    right_arm_ip_address: str

    # `max_relative_target` limits the magnitude of the relative positional target vector for
    # safety purposes. Set this to a positive scalar to have the same value for all motors, or a
    # list that is the same length as the number of motors in your follower arms.
    left_arm_max_relative_target: float | None = None
    right_arm_max_relative_target: float | None = None

    # Multiplier for computing minimum time (in seconds) for the arm to reach a target position.
    # The final goal time is computed as: min_time_to_move = multiplier / fps.
    # A smaller multiplier results in faster (but potentially jerky) motion.
    # A larger multiplier results in smoother motion but with increased lag.
    # A recommended starting value is 3.0.
    # This value is shared between both arms.
    min_time_to_move_multiplier: float = 3.0

    # Expected control loop rate in Hz (shared between both arms).
    loop_rate: int = 30

    # Include per-joint velocity (`.vel`) in observations (shared between both arms).
    include_velocity: bool = False

    # Include per-joint effort (`.eff`) in observations. This is the total motor effort, combining
    # gravity, friction, and any external load. Measured in Nm for the arm joints and N for the
    # gripper carriage. Nonzero even when the arm is holding still against gravity. Shared between
    # both arms.
    include_effort: bool = False

    # Include per-joint external effort (`.ext_eff`) in observations. This is the estimated
    # externally applied effort, after gravity and friction compensation. Measured in Nm for the
    # arm joints and N for the gripper carriage. Useful for contact and force sensing; an unloaded
    # arm reports values near zero. Shared between both arms.
    include_external_effort: bool = False

    # cameras (shared between both arms)
    cameras: dict[str, CameraConfig] = field(default_factory=dict)
