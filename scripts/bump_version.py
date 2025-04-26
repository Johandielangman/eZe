# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: April 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# =============== // STANDARD IMPORT // ===============

import argparse
from pathlib import Path


# =============== // FILE PATH PROCESSING // ===============

REPOSITORY_ROOT: Path = Path(__file__).resolve(strict=True).parent.parent
VERSION_PATH: Path = REPOSITORY_ROOT / "version.txt"


if __name__ == "__main__":
    # =============== // ARGPARSE // ===============

    parser = argparse.ArgumentParser(
        prog=__file__,
        description='Bump the version'
    )
    parser.add_argument(
        "--major",
        action="store_true",
        help="Bump the major version"
    )
    parser.add_argument(
        "--minor",
        action="store_true",
        help="Bump the minor version"
    )
    parser.add_argument(
        "--patch",
        action="store_true",
        help="Bump the patch version"
    )
    args = parser.parse_args()

    if not any([args.major, args.minor, args.patch]):
        parser.error("No version bump type provided")

    if sum([args.major, args.minor, args.patch]) > 1:
        parser.error("Only one version bump type can be provided")

    # =============== // VERSION BUMP // ===============

    old_version = VERSION_PATH.read_text(encoding="utf-8").strip()
    major, minor, patch = [int(v) for v in old_version.split(".")]
    if args.major:
        major += 1
        minor = 0
        patch = 0
    elif args.minor:
        minor += 1
        patch = 0
    elif args.patch:
        patch += 1

    new_version = f"{major}.{minor}.{patch}"

    # =============== // FILE WRITE // ===============

    print(f"Bumping version from {old_version} to {new_version}")
    VERSION_PATH.write_text(f'{new_version}\n')
    print("Version bumped!")
