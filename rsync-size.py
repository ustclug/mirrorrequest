#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

import subprocess
import argparse


def human_readable_size(size: float) -> str:
    suffix = ["B", "KB", "MB", "GB", "TB"]
    level = 0
    while size >= 10000:
        level += 1
        size /= 1024
    return f"{size:.1f} {suffix[level]}"


def main(upstream: str) -> None:
    p = subprocess.run(
        ["rsync", "-a", "--no-motd", "-r", "--list-only", upstream],
        stdout=subprocess.PIPE,
        text=True,
    )
    if p.returncode != 0:
        print("Failed to run rsync")
        exit(1)
    total_size = 0
    for line in p.stdout.splitlines():
        line = line.strip()
        splitted = line.split(maxsplit=4)
        size = splitted[1].replace(",", "")
        total_size += int(size)
    print("Total size:", human_readable_size(total_size))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get total size from rsync upstream"
    )
    parser.add_argument(
        "upstream", type=str, help="Upstream URL, like rsync://example.com/ubuntu/"
    )
    args = parser.parse_args()

    main(args.upstream)
