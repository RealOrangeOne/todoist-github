#!/usr/bin/env python3

import argparse
import logging
import time

import coloredlogs

from .tasks import ALL_TASKS


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=int, default=0)
    return parser.parse_args()


def run_tasks():
    for task in ALL_TASKS:
        logging.info("Executing %s", task.__name__)
        task()


def main():
    coloredlogs.install(
        level=logging.INFO,
        fmt="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    )
    args = get_args()
    run_tasks()
    if args.interval:
        while True:
            run_tasks()
            time.sleep(args.interval)


if __name__ == "__main__":
    main()
