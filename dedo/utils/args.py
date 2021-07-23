#
# Command line arguments.
#
# @contactrika
#
import argparse
import logging
import sys

from .task_info import TASK_INFO


def get_args(parent=None):
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)])
    parser = argparse.ArgumentParser(description='args', add_help=False)
    # Main/demo args.
    parser.add_argument('--env', type=str,
                        default='HangBag-v0', help='Env name')
    parser.add_argument('--max_episode_len', type=int,
                        default=400, help='Number of simulation steps per task')
    parser.add_argument('--seed', type=int, default=0, help='Random seed')
    parser.add_argument('--num_runs', type=int, default=10,
                        help='Number of runs/episodes to complete')
    parser.add_argument('--viz', action='store_true', help='Whether to visualize')
    parser.add_argument('--debug', action='store_true',
                        help='Whether to print debug info')
    # Simulation args. Note: turn up frequency when deform stiffness is high.
    parser.add_argument('--sim_frequency', type=int, default=500,
                        help='Number of simulation steps per second')  # 250-1K
    parser.add_argument('--sim_gravity', type=float, default=-9.8, help='Gravity')
    # Anchor/grasping args.
    parser.add_argument('--anchor_init_pos', type=float, nargs=3,
                        default=[-0.04, 0.40, 0.70],
                        help='Initial position for an anchor')
    parser.add_argument('--other_anchor_init_pos', type=float, nargs=3,
                        default=[0.04, 0.40, 0.70],
                        help='Initial position for another anchors')
    # SoftBody args.
    parser.add_argument('--override_deform_obj', type=str, default=None,
                        help='Load custom deformable (note that you have to'
                             'fill in DEFORM_INFO entry for new items)')
    parser.add_argument('--deform_init_pos', type=float, nargs=3,
                        default=[0,0,0.42],
                        help='Initial pos for the center of the deform object')
    parser.add_argument('--deform_init_ori', type=float, nargs=3,
                        default=[0,0,0],
                        help='Initial orientation for deform (in Euler angles)')
    parser.add_argument('--deform_scale', type=float, default=1.0,
                        help='Scaling for the deform object')
    parser.add_argument('--deform_bending_stiffness', type=float, default=1.0,
                        help='deform spring elastic stiffness')  # 1.0-300.0
    parser.add_argument('--deform_damping_stiffness', type=float, default=0.1,
                        help='deform spring damping stiffness')
    parser.add_argument('--deform_elastic_stiffness', type=float, default=1.0,
                        help='deform spring elastic stiffness')  # 1.0-300.0
    parser.add_argument('--deform_friction_coeff', type=float, default=0.0,
                        help='deform friction coefficient')
    # Camera args.
    parser.add_argument('--cam_resolution', type=int, default=None,
                        help='RGB camera resolution in pixels (both with and '
                             'height). Use none to get only anchor poses.')
    # Parse args and do sanity checks.
    args, unknown = parser.parse_known_args()
    env_parts = args.env.split('-v')
    assert(len(env_parts) == 2 and env_parts[1].isdigit()), \
        '--env=[Task]-v[Version] (e.g. HangCloth-v0)'
    args.task = env_parts[0]
    args.version = int(env_parts[1])
    assert(args.task in TASK_INFO.keys()), 'TASK_INFO lists supported tasks'
    assert(args.version < len(TASK_INFO[args.task])), 'env version too high'
    return args, parser
