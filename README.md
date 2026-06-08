# LeRobot Trossen Integration

## Overview

This package contains LeRobot integrations for the Trossen AI series of robots.
See the [LeRobot documentation](https://huggingface.co/docs/lerobot) for details on more advanced usage like using the HuggingFace Hub, model training, and using different teleoperation methods.
See the [Trossen AI documentation](https://docs.trossenrobotics.com/trossen_arm/main/tutorials/lerobot_plugin.html) for details on configuration and usage of Trossen AI robots with LeRobot.

## Installation

We use `uv` to manage our dependencies.
Follow the instructions [here](https://docs.astral.sh/uv/getting-started/installation/) to install `uv`.

This package requires **Python ≥ 3.12** (it depends on `lerobot >= 0.5.1`, which requires 3.12).
`uv` provisions a compatible interpreter automatically.

Run the following command to install this package and its dependencies:

```shell
# Clone this repository
git clone https://github.com/TrossenRobotics/lerobot_trossen.git

# Install the trossen lerobot packages and their dependencies
uv sync

# Verify installation
uv pip list | grep trossen
# lerobot-robot-trossen
# lerobot-teleoperator-trossen
# trossen-arm
# trossen-slate
```

## Usage

### Teleoperation Script

Teleoperate a WidowX AI robot with another WidowX AI robot.

```shell
uv run lerobot-teleoperate \
  --robot.type=widowxai_follower_robot \
  --robot.ip_address=192.168.1.4 \
  --robot.id=follower \
  --teleop.type=widowxai_leader_teleop \
  --teleop.ip_address=192.168.1.2 \
  --teleop.id=leader \
  --display_data=false
```

### Record Script

Record 10 episodes with duration 45s of a cube pickup task with a single WidowX AI robot using the RealSense camera interface.
This dataset will not be pushed to the Hugging Face Hub after recording.

```shell
uv run lerobot-record \
  --robot.type=widowxai_follower_robot \
  --robot.ip_address=192.168.1.4 \
  --robot.id=follower \
  --robot.cameras="{
    wrist: {type: intelrealsense, serial_number_or_name: "0123456789", width: 640, height: 480, fps: 30}
  }" \
  --teleop.type=widowxai_leader_teleop \
  --teleop.ip_address=192.168.1.2 \
  --teleop.id=leader \
  --display_data=true \
  --dataset.push_to_hub=false \
  --dataset.repo_id=${HF_USER}/widowxai-cube-pickup \
  --dataset.episode_time_s=45 \
  --dataset.reset_time_s=15 \
  --dataset.num_episodes=10 \
  --dataset.single_task="Grab the cube"
```

Record 25 episodes with duration 60s of a bimanual handover task with two WidowX AI robots using the OpenCV camera interface.
Datasets are pushed to the Hugging Face Hub after recording by default - make sure to set the `HF_USER` environment variable and be logged in with the `huggingface-cli login` command before running this script.

```shell
uv run lerobot-record \
  --robot.type=bi_widowxai_follower_robot \
  --robot.left_arm_ip_address=192.168.1.5 \
  --robot.right_arm_ip_address=192.168.1.4 \
  --robot.id=bimanual_follower \
  --robot.cameras='{
    cam_low: {"type": "opencv", "index_or_path": "0", "width": 640, "height": 480, "fps": 30},
  }' \
  --teleop.type=bi_widowxai_leader_teleop \
  --teleop.left_arm_ip_address=192.168.1.3 \
  --teleop.right_arm_ip_address=192.168.1.2 \
  --teleop.id=bimanual_leader \
  --display_data=true \
  --dataset.repo_id=${HF_USER}/bimanual-widowxai-handover-cube \
  --dataset.num_episodes=25 \
  --dataset.episode_time_s=60 \
  --dataset.reset_time_s=15 \
  --dataset.single_task="Grab and handover the red cube to the other arm"
```

### Optional Observation Features

By default, WidowX AI followers only observe joint positions (`<joint>.pos`).
You can optionally record additional per-joint signals by enabling the following flags.
All are disabled by default.

| Flag | Observation key | Description |
| ---- | --------------- | ----------- |
| `include_velocity` | `<joint>.vel` | Joint velocity. Measured in rad/s for the arm joints and m/s for the gripper carriage. |
| `include_effort` | `<joint>.eff` | Total motor effort, combining gravity, friction, and any external load. Measured in Nm for the arm joints and N for the gripper carriage. Nonzero even when the arm is holding still against gravity. |
| `include_external_effort` | `<joint>.ext_eff` | Estimated externally applied effort, after gravity and friction compensation. Measured in Nm for the arm joints and N for the gripper carriage. Useful for contact and force sensing; an unloaded arm reports values near zero. |

Pass them as `--robot.<flag>=true` when running any command that constructs the robot (for example `lerobot-record` or `lerobot-teleoperate`). For example, to record with all three enabled on a single WidowX AI follower:

```shell
uv run lerobot-record \
  --robot.type=widowxai_follower_robot \
  --robot.ip_address=192.168.1.4 \
  --robot.id=follower \
  --robot.include_velocity=true \
  --robot.include_effort=true \
  --robot.include_external_effort=true \
  --dataset.repo_id=${HF_USER}/widowxai-cube-pickup \
  --dataset.single_task="Grab the cube" \
  --teleop.type=widowxai_leader_teleop \
  --teleop.ip_address=192.168.1.2 \
  --teleop.id=leader
```

The same flags are available on the bimanual (`bi_widowxai_follower_robot`) and Mobile AI (`mobileai_robot`) configurations, where they are shared across both arms.
The resulting observation keys are prefixed per arm, e.g. `left_<joint>.eff` and `right_<joint>.eff`.

### Dataset Visualization

If you uploaded your dataset to the Hugging Face Hub using ``--control.push_to_hub=true``, you can [visualize your dataset online](https://huggingface.co/spaces/lerobot/visualize_dataset).
To do so, copy and paste your repository ID into the provided field.
Your repository ID follows the format:

```
<huggingface-username>/<dataset-id>
```

### Model Eval (Record with Policy) Script

Evaluate a trained policy by recording 2 episodes of a cube pickup task with a single WidowX AI robot using the OpenCV camera interface.

```shell
uv run lerobot-record \
  --robot.type=widowxai_follower_robot \
  --robot.ip_address=192.168.1.4 \
  --robot.cameras="{cam_high: {type: opencv, index_or_path: 0, width: 640, height: 480}}" \
  --robot.id=follower \
  --dataset.repo_id=${HF_USER}/widowxai-cube-pickup \
  --dataset.num_episodes=2 \
  --dataset.single_task="Grab the cube" \
  --policy.path=${HF_USER}/act-widowxai-cube-pickup
```

> [!NOTE]
> The example above uses an **ACT** policy, which the lean base install runs directly.
> **VLA policies (π₀, π₀.₅, SmolVLA) need extra dependencies** (transformers/peft) that the base install omits — prefix the command with `uv run --with "lerobot[pi]>=0.5.1"` (use `[smolvla]` for SmolVLA).
> For responsive on-robot VLA evaluation, prefer the **Async Inference** flow below.

### Async Inference (Policy Server + Robot Client)

For asynchronous / distributed inference, LeRobot runs the policy in a separate **policy server** process and the robot in a **client** process, communicating over gRPC.
This is the recommended path for slow VLA policies (π₀, π₀.₅, SmolVLA): the client keeps the robot control loop responsive while the server runs inference, and overlapping action chunks are blended on the client (real-time chunking).

The server and client live in **upstream LeRobot**, and they need dependencies the lean base install omits: `async` (the `grpcio` transport) and, for π-family policies, `pi` (transformers/peft).
Layer them at run time with `uv run --with` (requires Python ≥ 3.12):

**Terminal A — policy server** (holds the policy on the GPU):

```shell
uv run --with "lerobot[async,pi]>=0.5.1" python -m lerobot.async_inference.policy_server \
  --host=127.0.0.1 \
  --port=8080 \
  --fps=30 \
  --inference_latency=0.033 \
  --obs_queue_timeout=2
```

**Terminal B — robot client** (drives the hardware):

```shell
uv run --with "lerobot[async,pi]>=0.5.1" python -m lerobot.async_inference.robot_client \
  --server_address=127.0.0.1:8080 \
  --robot.type=bi_widowxai_follower_robot \
  --robot.left_arm_ip_address=192.168.1.5 \
  --robot.right_arm_ip_address=192.168.1.4 \
  --robot.id=bimanual_follower \
  --robot.cameras='{
      cam_high: {type: intelrealsense, serial_number_or_name: "<serial>", width: 640, height: 480, fps: 30},
      cam_low: {type: intelrealsense, serial_number_or_name: "<serial>", width: 640, height: 480, fps: 30},
      cam_left_wrist: {type: intelrealsense, serial_number_or_name: "<serial>", width: 640, height: 480, fps: 30},
      cam_right_wrist: {type: intelrealsense, serial_number_or_name: "<serial>", width: 640, height: 480, fps: 30}
      }' \
  --task="Grab and handover the red cube to the other arm" \
  --policy_type=pi05 \
  --pretrained_name_or_path=${HF_USER}/pi05-block-transfer-lerobot \
  --policy_device=cuda \
  --actions_per_chunk=50 \
  --chunk_size_threshold=0.5 \
  --aggregate_fn_name=weighted_average
```

Notes:

- The Trossen robots **auto-register** — LeRobot discovers the installed `lerobot_robot_trossen` plugin, so `--robot.type=bi_widowxai_follower_robot` resolves with no manual import.
- The model loads on the **first** client connection (large VLAs take 1–2 min) before the first action.
- The `--task` prompt **must match training** (π-family policies are language-conditioned).
- `--actions_per_chunk`, `--chunk_size_threshold`, and `--aggregate_fn_name` control real-time chunking: how many predicted steps to execute per chunk, when to re-query the server, and how overlapping steps are blended (`weighted_average`).
- The client strictly only needs `lerobot[async]`; using `[async,pi]` on both is identical and simplest.
- Stop the **client** first (`Ctrl-C`), then the server.

### Replay Script

Replay episode 2 of a cube pickup task with a single WidowX AI robot.

```shell
uv run lerobot-replay \
  --robot.type=widowxai_follower_robot \
  --robot.ip_address=192.168.1.4 \
  --robot.id=follower \
  --dataset.repo_id=${HF_USER}/widowxai-cube-pickup \
  --dataset.episode=2
```
