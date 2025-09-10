# trossen_lerobot

## Overview

This package contains LeRobot integrations for the Trossen AI series of robots.

## Installation

We use `uv` to manage our dependencies.
Follow the instructions [here](https://docs.astral.sh/uv/getting-started/installation/) to install `uv`.

Run the following command to install this package and its dependencies:

```shell
uv sync
# or
uv pip install -e .
```

## Usage

We provide drop-in replacements for the main scripts in the `lerobot` package:

* teleoperate.py
* record.py
* replay.py

### Teleoperate Script

To teleoperate, say, the Trossen AI Solo Kit, run:

```shell
uv run -m trossen_lerobot.teleoperate \
    --robot.type=widowxai_follower \
    --robot.ip_address=192.168.1.4 \
    --robot.id=follower \
    --teleop.type=widowxai_leader \
    --teleop.ip_address=192.168.1.2 \
    --teleop.id=leader \
    --display_data=false
```

### Record Script

To record a dataset on, say, the Trossen AI Stationary Kit, run:

```shell
uv run -m trossen_lerobot.record \
  --robot.type=bi_widowxai_follower \
  --robot.left_arm_ip_address=192.168.1.5 \
  --robot.right_arm_ip_address=192.168.1.4 \
  --robot.id=bimanual_follower \
  --robot.cameras='{
    cam_low: {"type": "opencv", "index_or_path": 0, "width": 640, "height": 480, "fps": 30},
  }' \
  --teleop.type=bi_widowxai_leader \
  --teleop.left_arm_ip_address=192.168.1.3 \
  --teleop.right_arm_ip_address=192.168.1.2 \
  --teleop.id=bimanual_leader \
  --display_data=true \
  --dataset.repo_id=${HF_USER}/bimanual-widowxai-handover-cube \
  --dataset.num_episodes=25 \
  --dataset.single_task="Grab and handover the red cube to the other arm"
```

### Model Eval (Record with Policy) Script

```shell
python -m trossen_lerobot.record \
  --robot.type=widowxai_follower \
  --robot.ip_address=192.168.1.4 \
  --robot.cameras="{cam_high: {type: opencv, camera_index: 0, width: 640, height: 480}}" \
  --robot.id=bimanual_follower \
  --dataset.repo_id=${HF_USER}/widowxai-cube-pickup \
  --dataset.num_episodes=2 \
  --dataset.single_task="Grab the cube" \
  --policy.path=${HF_USER}/act-widowxai-cube-pickup
```

### Replay Script

To replay an episode from a dataset on, say, a WidowX AI follower arm, run:

```shell
uv run -m trossen_lerobot.replay \
    --robot.type=widowxai_follower \
    --robot.ip_address=192.168.1.4 \
    --robot.id=follower \
    --dataset.repo_id=${HF_USER}/widowxai-cube-pickup \
    --dataset.episode=2
```
