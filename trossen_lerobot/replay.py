"""
Replays the actions of an episode from a dataset on a robot.

Examples:

```shell
python -m lerobot.replay \
    --robot.type=widowxai_follower \
    --robot.ip_address=192.168.1.4 \
    --robot.id=black \
    --dataset.repo_id=${HF_USER}/widowxai-handover-cube \
    --dataset.episode=2
```


Example replay with bimanual WidowX AI arms:

```shell
python -m lerobot.replay \
  --robot.type=bi_widowxai_leader \
  --robot.left_arm_ip_address=192.168.1.4 \
  --robot.right_arm_ip_address=192.168.1.4 \
  --robot.id=bimanual_follower \
  --dataset.repo_id=${HF_USER}/bimanual-widowxai-handover-cube \
  --dataset.episode=0
```

"""

import logging
import time
from dataclasses import asdict
from pprint import pformat

import draccus
from lerobot.datasets.lerobot_dataset import LeRobotDataset
from lerobot.replay import ReplayConfig
from lerobot.utils.robot_utils import busy_wait
from lerobot.utils.utils import init_logging, log_say

from trossen_lerobot.robots import bi_widowxai_follower, widowxai_follower  # noqa: F401
from trossen_lerobot.robots.utils import make_robot_from_config


@draccus.wrap()
def replay(cfg: ReplayConfig):
    """Copied from lerobot.replay, modified to work with Trossen LeRobot."""
    init_logging()
    logging.info(pformat(asdict(cfg)))

    robot = make_robot_from_config(cfg.robot)
    dataset = LeRobotDataset(
        cfg.dataset.repo_id, root=cfg.dataset.root, episodes=[cfg.dataset.episode]
    )
    actions = dataset.hf_dataset.select_columns("action")
    robot.connect()

    log_say("Replaying episode", cfg.play_sounds, blocking=True)
    for idx in range(dataset.num_frames):
        start_episode_t = time.perf_counter()

        action_array = actions[idx]["action"]
        action = {}
        for i, name in enumerate(dataset.features["action"]["names"]):
            action[name] = action_array[i]

        robot.send_action(action)

        dt_s = time.perf_counter() - start_episode_t
        busy_wait(1 / dataset.fps - dt_s)

    robot.disconnect()


def main():
    replay()


if __name__ == "__main__":
    main()
