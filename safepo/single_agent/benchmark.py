import argparse
import shlex
import subprocess

navi_robots = ['Car', 'Point', 'Racecar']
navi_tasks = ['Button', 'Circle', 'Goal', 'Push']
diffculies = ['1', '2']
vel_robots = ['Ant', 'HalfCheetah', 'Hopper', 'Walker2d', 'Swimmer', 'Humanoid']
vel_tasks = ['Velocity']

navi_envs = [
    f"Safety{robot}{task}{diffculty}-v0"
    for diffculty in diffculies
    for robot in navi_robots
    for task in navi_tasks
]

vel_envs = [
    f"Safety{robot}{task}-v1"
    for robot in vel_robots
    for task in vel_tasks
]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--env-ids",
        nargs="+",
        default=navi_envs+vel_envs,
        help="the ids of the environment to benchmark",
    )
    parser.add_argument(
        "--algo",
        nargs="+",
        default=[
            "pcpo",
            "ppo_lag",
            "cup",
            "focops",
            "rcpo",
            "trpo_lag",
            "cpo",
            "cppo_pid"
        ],
        help="the ids of the algorithm to benchmark",
    )
    parser.add_argument(
        "--num-seeds", type=int, default=3, help="the number of random seeds"
    )
    parser.add_argument(
        "--start-seed", type=int, default=0, help="the number of the starting seed"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=48,
        help="the number of workers to run benchmark experimenets",
    )
    parser.add_argument(
        "--experiment", type=str, default="benchmark_single_env_8_14", help="name of the experiment"
    )
    args = parser.parse_args()

    return args


def run_experiment(command: str):
    command_list = shlex.split(command)
    print(f"running {command}")
    fd = subprocess.Popen(command_list)
    return_code = fd.wait()
    assert return_code == 0


if __name__ == "__main__":
    args = parse_args()

    commands = []

    log_dir = f"../runs"
    for seed in range(0, args.num_seeds):
        for env_id in args.env_ids:
            for algo in args.algo:
                commands += [
                    " ".join(
                        [
                            f"python {algo}.py",
                            "--env-id",
                            env_id,
                            "--seed",
                            str(args.start_seed + 1000*seed),
                            "--write-terminal",
                            "False",
                            "--log-dir",
                            log_dir,
                            "--experiment",
                            args.experiment,
                        ]
                    )
                ]

    print("======= commands to run:")
    for command in commands:
        print(command)

    if args.workers > 0:
        from concurrent.futures import ThreadPoolExecutor

        executor = ThreadPoolExecutor(
            max_workers=args.workers, thread_name_prefix="safepo-benchmark-worker-"
        )
        for command in commands:
            executor.submit(run_experiment, command)
        executor.shutdown(wait=True)
    else:
        print(
            "not running the experiments because --workers is set to 0; just printing the commands to run"
        )