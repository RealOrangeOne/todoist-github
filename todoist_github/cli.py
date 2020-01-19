#!/usr/bin/env python3

import argparse
import time

from .tasks import ALL_TASKS


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=int, default=0)
    return parser.parse_args()


def run_tasks():
    for task in ALL_TASKS:
        print("Executing", task.__name__)
        task()


def main():
    args = get_args()
    run_tasks()
    if args.interval:
        while True:
            run_tasks()
            time.sleep(args.interval)


if __name__ == "__main__":
    main()
