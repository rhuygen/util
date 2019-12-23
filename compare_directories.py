#!/usr/bin/env python3
# coding: utf-8

import os
import shutil
import time
import logging
from pathlib import Path

os.getcwd()


def is_valid_file(file):
    if file.startswith("."):
        return False
    if file.startswith("_"):
        return False

    return True


def compare_directories(source, destination, *, copy_source=False, copy_dest=False):
    files_in_source = os.listdir(source)
    files_in_destination = os.listdir(destination)

    files_not_in_source = []
    files_not_in_destination = []

    for file in files_in_source:
        if file not in files_in_destination:
            if is_valid_file(file): files_not_in_destination.append(file)
    for file in files_in_destination:
        if file not in files_in_source:
            if is_valid_file(file): files_not_in_source.append(file)

    if not files_not_in_source:
        print(f"No files are missing in {source}")
    else:
        print(f"The following {len(files_not_in_source)} files are not found in {source}:")
        for file in files_not_in_source:
            print(f"  * {file}")
            if copy_dest:
                print(f"copying '{file}'...", end=' ', flush=True)
                with Timer() as timer:
                    from_file = Path(destination, file)
                    to = Path(source)
                    shutil.copy2(from_file, to)
                print(f"took {timer():0.2f} seconds, {from_file.stat().st_size/1024./1024./timer():0.2f} MB/s")

    if not files_not_in_destination:
        print(f"No files are missing in {destination}")
    else:
        print(f"The following {len(files_not_in_destination)} files are not found in {destination}:")
        for file in files_not_in_destination:
            print(f"  * {file}")
            if copy_source:
                print(f"copying '{file}'...", end=' ', flush=True)
                with Timer() as timer:
                    from_file = Path(source, file)
                    to = Path(destination)
                    shutil.copy2(from_file, to)
                print(f"took {timer():0.2f} seconds, {from_file.stat().st_size/1024./1024./timer():0.2f} MB/s")


class Timer(object):
    """
    Context manager to benchmark some lines of code.

    When the context exits, the elapsed time is sent to the default logger (level=INFO).

    Elapsed time can be logged with the `log_elapsed()` method and requested in fractional seconds
    by calling the class instance. When the contexts goes out of scope, the elapsed time will not
    increase anymore.

    ```python
    with Timer("Some calculation") as timer:
        # do some calculations
        timer.log_elapsed()
        # do some more calculations
        print(f"Elapsed seconds: {timer()}")
    ```

    Args:
        name (str): a name for the Timer, will be printed in the logging message
        precision (int): the precision for the presentation of the elapsed time (number of digits behind the comma ;)

    Returns:
        a context manager class that records the elapsed time.
    """
    def __init__(self, name="Timer", precision=3):
        self.name = name
        self.precision = precision

    def __enter__(self):
        # start is a value containing the start time in fractional seconds
        # end is a function which returns the time in fractional seconds
        self.start = time.perf_counter()
        self.end = time.perf_counter
        return self

    def __exit__(self, ty, val, tb):
        # The context goes out of scope here and we fix the elapsed time
        self._total_elapsed = time.perf_counter()

        # Overwrite self.end() so that it always returns the fixed end time
        self.end = self._end

        logging.info(f"{self.name}: {self.end() - self.start:0.{self.precision}f} seconds")
        return False

    def __call__(self):
        return self.end() - self.start

    def log_elapsed(self):
        """Sends the elapsed time info to the default logger."""
        logging.info(f"{self.name}: {self.end() - self.start:0.{self.precision}f} seconds elapsed")

    def _end(self):
        return self._total_elapsed


# disk1 = "/Volumes/WD 1TB/"
# disk2 = "/Volumes/WD 1TB - BACKUP/"
# disk3 = "/Volumes/Movie Disk 1TB/"

# **Comparing Movies on WD 1TB with its BACKUP drive**

# compare_directories(disk1 + "Films", disk2 + "Films")

# **Compare TV Series on WD 1TB and its BACKUP drive**

# compare_directories(disk1 + "Series", disk2 + "Series")

# **Comparing Movies on WD 1TB with the G-Drive disk @MacMini**

# compare_directories(disk1 + "Films", disk3 + "Films")

# **Compare TV Series on WD 1TB and the G-Drive disk @MacMini**

# compare_directories(disk1 + "Series", disk3 + "Series")


def main(argv):
    import argparse

    parser = argparse.ArgumentParser(description='Compare two directories by filename.')
    parser.add_argument('source', type=str,
                        help='the source directory for comparison')
    parser.add_argument('destination', type=str,
                        help='the destination directory for comparison')
    parser.add_argument('--copy_source', action='store_false',
                        help='copy missing files from the source to the destination directory')
    parser.add_argument('--copy_dest', action='store_false',
                        help='copy missing files from the destination to the source directory')

    args = parser.parse_args()

    compare_directories(args.source, args.destination, copy_src=args.copy_source, copy_dest=args.copy_dest)


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
