"""
Simple script to control a robot from teleoperation.

Example:

```shell
python -m trossen_lerobot.teleoperate \
    --robot.type=widowxai_follower \
    --robot.ip_address=192.168.1.4 \
    --robot.cameras='{}' \
    --robot.id=follower \
    --teleop.type=widowxai_leader \
    --teleop.ip_address=192.168.1.2 \
    --teleop.id=leader \
    --display_data=false
```

Example teleoperation with bimanual WidowX AI arms:

```shell
python -m trossen_lerobot.teleoperate \
    --robot.type=bi_widowxai_follower \
    --robot.left_arm_ip_address=192.168.1.5 \
    --robot.right_arm_ip_address=192.168.1.4 \
    --robot.id=bimanual_follower \
    --robot.cameras='{}' \
    --teleop.type=bi_widowxai_leader \
    --teleop.left_arm_ip_address=192.168.1.3 \
    --teleop.right_arm_ip_address=192.168.1.2 \
    --teleop.id=bimanual_leader \
    --display_data=false
```
"""

import logging
from dataclasses import asdict
from pprint import pformat

import draccus
import rerun as rr
from lerobot.teleoperate import TeleoperateConfig, teleop_loop
from lerobot.utils.utils import init_logging
from lerobot.utils.visualization_utils import _init_rerun

from lerobot_robot_trossen.robots import bi_widowxai_follower, widowxai_follower  # noqa: F401
from lerobot_robot_trossen.robots.utils import make_robot_from_config
from lerobot_robot_trossen.teleoperators import bi_widowxai_leader, widowxai_leader  # noqa: F401
from lerobot_robot_trossen.teleoperators.utils import make_teleoperator_from_config


@draccus.wrap()
def teleoperate(cfg: TeleoperateConfig):
    """Copied from lerobot.teleoperate, modified to work with Trossen LeRobot."""
    init_logging()
    logging.info(pformat(asdict(cfg)))
    if cfg.display_data:
        _init_rerun(session_name="teleoperation")

    teleop = make_teleoperator_from_config(cfg.teleop)
    robot = make_robot_from_config(cfg.robot)

    teleop.connect()
    robot.connect()

    try:
        teleop_loop(
            teleop, robot, cfg.fps, display_data=cfg.display_data, duration=cfg.teleop_time_s
        )
    except KeyboardInterrupt:
        pass
    finally:
        if cfg.display_data:
            rr.rerun_shutdown()
        teleop.disconnect()
        robot.disconnect()


if __name__ == "__main__":
    teleoperate()
