# trossen_lerobot

## Overview

This package contains LeRobot integrations for the Trossen AI series of robots.
See the [LeRobot documentation](https://huggingface.co/docs/lerobot) for details on more advanced usage like using the HuggingFace Hub, model training, and using different teleoperation methods.

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

Teleoperate a WidowX AI robot with another WidowX AI robot.

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

Record 10 episodes of a cube pickup task with a single WidowX AI robot using the RealSense camera interface.
This dataset will not be pushed to the Hugging Face Hub after recording.

```shell
uv run -m trossen_lerobot.record \
  --robot.type=widowxai_follower \
  --robot.ip_address=192.168.1.4 \
  --robot.id=bimanual_follower \
  --robot.cameras="{
    wrist: {type: intelrealsense, serial_number_or_name: "0123456789", width: 640, height: 480, fps: 30}
  }" \
  --teleop.type=widowxai_leader \
  --teleop.ip_address=192.168.1.2 \
  --teleop.id=bimanual_leader \
  --display_data=true \
  --dataset.push_to_hub=false \
  --dataset.repo_id=${HF_USER}/widowxai-cube-pickup \
  --dataset.num_episodes=10 \
  --dataset.single_task="Grab the cube"
```

Record 25 episodes of a bimanual handover task with two WidowX AI robots using the OpenCV camera interface.
Datasets are pushed to the Hugging Face Hub after recording by default - make sure to set the `HF_USER` environment variable and be logged in with the `huggingface-cli login` command before running this script.

```shell
uv run -m trossen_lerobot.record \
  --robot.type=bi_widowxai_follower \
  --robot.left_arm_ip_address=192.168.1.5 \
  --robot.right_arm_ip_address=192.168.1.4 \
  --robot.id=bimanual_follower \
  --robot.cameras='{
    cam_low: {"type": "opencv", "index_or_path": "0", "width": 640, "height": 480, "fps": 30},
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

## Dataset Visualization

If you uploaded your dataset to the Hugging Face Hub using ``--control.push_to_hub=true``, you can [visualize your dataset online](https://huggingface.co/spaces/lerobot/visualize_dataset).
To do so, copy and paste your repository ID into the provided field.
Your repository ID follows the format:

```
<huggingface-username>/<dataset-id>
```

### Model Eval (Record with Policy) Script

Evaluate a trained policy by recording 2 episodes of a cube pickup task with a single WidowX AI robot using the OpenCV camera interface.

```shell
uv run -m trossen_lerobot.record \
  --robot.type=widowxai_follower \
  --robot.ip_address=192.168.1.4 \
  --robot.cameras="{cam_high: {type: opencv, index_or_path: 0, width: 640, height: 480}}" \
  --robot.id=bimanual_follower \
  --dataset.repo_id=${HF_USER}/widowxai-cube-pickup \
  --dataset.num_episodes=2 \
  --dataset.single_task="Grab the cube" \
  --policy.path=${HF_USER}/act-widowxai-cube-pickup
```

### Replay Script

Replay episode 2 of a cube pickup task with a single WidowX AI robot.

```shell
uv run -m trossen_lerobot.replay \
    --robot.type=widowxai_follower \
    --robot.ip_address=192.168.1.4 \
    --robot.id=follower \
    --dataset.repo_id=${HF_USER}/widowxai-cube-pickup \
    --dataset.episode=2
```
