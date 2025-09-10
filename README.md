# trossen_lerobot

## Overview

This package contains LeRobot integrations for the Trossen AI series of robots.

## Installation

We use `uv` to manage our dependencies.
Follow the instructions [here](https://docs.astral.sh/uv/getting-started/installation/) to install `uv`.

Run the following command to install this package and its dependencies:

```bash
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

```bash
uv run trossen_lerobot.teleoperate \
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

```bash
uv run trossen_lerobot.record \
  --robot.type=widowxai_follower \
  --robot.ip_address=192.168.1.4 \
  --robot.cameras="{cam_high: {type: opencv, camera_index: 0, width: 640, height: 480}}" \
  --robot.id=black \
  --dataset.repo_id=${HF_USER}/record-test \
  --dataset.num_episodes=2 \
  --dataset.single_task="Grab the cube" \
  --teleop.type=widowxai_leader \
  --teleop.ip_address=192.168.1.2 \
  --teleop.id=blue
```

### Replay Script

To replay an episode from a dataset on, say, a WidowX AI follower arm, run:

```bash
uv run -m trossen_lerobot.replay \
    --robot.type=widowxai_follower \
    --robot.ip_address=192.168.1.4 \
    --robot.id=follower \
    --dataset.repo_id=${HF_USER}/widowxai-cube-pickup \
    --dataset.episode=2
```
