"""lerobot-record that also zeroes the Rivet odometry at the start of every episode.

Takes the same arguments as lerobot-record, e.g.
`uv run lerobot-rivet-record --robot.type=rivet_robot ...`
"""

import time

from lerobot.scripts import lerobot_record
from lerobot.utils.import_utils import register_third_party_plugins

from lerobot_robot_trossen.rivet import RivetRobot

_record_loop = lerobot_record.record_loop

# Odometry is considered zeroed within this tolerance (m, rad)
ODOMETRY_RESET_TOLERANCE = 0.001
# Max time to wait for the odometry to report the reset
ODOMETRY_RESET_TIMEOUT_S = 1.0


def wait_for_odometry_reset(robot: RivetRobot) -> None:
    # The reset takes effect asynchronously, so wait until the odometry reports it to keep the
    # previous episode's pose out of the first frame
    deadline = time.perf_counter() + ODOMETRY_RESET_TIMEOUT_S
    while True:
        robot.base.heartbeat()
        position = robot.base.get_odometry().position
        if all(abs(p) <= ODOMETRY_RESET_TOLERANCE for p in position):
            return
        if time.perf_counter() > deadline:
            raise RuntimeError(
                f"{robot} odometry did not reset within {ODOMETRY_RESET_TIMEOUT_S}s "
                f"(x, y, theta = {tuple(position)})"
            )
        time.sleep(0.01)


def record_loop(robot, *args, dataset=None, **kwargs):
    # record() runs this loop once per episode with a dataset, then again without one while the
    # environment is reset, so only zero the odometry when an episode starts
    if dataset is not None and isinstance(robot, RivetRobot):
        robot.reset_odometry()
        wait_for_odometry_reset(robot)
    return _record_loop(robot, *args, dataset=dataset, **kwargs)


def main():
    # record() looks up record_loop from its module when called, so this swaps in the wrapper
    lerobot_record.record_loop = record_loop
    register_third_party_plugins()
    lerobot_record.record()


if __name__ == "__main__":
    main()
