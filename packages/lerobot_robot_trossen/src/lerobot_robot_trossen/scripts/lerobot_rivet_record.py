"""lerobot-record that also zeroes the Rivet odometry at the start of every episode.

Takes the same arguments as lerobot-record, e.g.
`uv run lerobot-trossen-record --robot.type=rivet_robot ...`
"""

from lerobot.scripts import lerobot_record
from lerobot.utils.import_utils import register_third_party_plugins

from lerobot_robot_trossen.rivet import RivetRobot

_record_loop = lerobot_record.record_loop


def record_loop(robot, *args, dataset=None, **kwargs):
    # record() runs this loop once per episode with a dataset, then again without one while the
    # environment is reset, so only zero the odometry when an episode starts
    if dataset is not None and isinstance(robot, RivetRobot):
        robot.reset_odometry()
    return _record_loop(robot, *args, dataset=dataset, **kwargs)


def main():
    # record() looks up record_loop from its module when called, so this swaps in the wrapper
    lerobot_record.record_loop = record_loop
    register_third_party_plugins()
    lerobot_record.record()


if __name__ == "__main__":
    main()
