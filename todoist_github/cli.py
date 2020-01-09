#!/usr/bin/env python3

from .tasks import ALL_TASKS


def main():
    for task in ALL_TASKS:
        print("Executing", task.__name__)
        task()


if __name__ == "__main__":
    main()
