# Copyright 2024 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass, field

from lerobot.cameras import CameraConfig
from lerobot.robots.config import RobotConfig


@RobotConfig.register_subclass("bi_widowxai_follower")
@dataclass
class BiWidowXAIFollowerConfig(RobotConfig):
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

    # cameras (shared between both arms)
    cameras: dict[str, CameraConfig] = field(default_factory=dict)
