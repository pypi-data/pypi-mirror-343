import argparse
import itertools
import json
import urllib.request
from pathlib import Path


def make_parser():
    parser = argparse.ArgumentParser(description='Fetch, maintain and query historical download information')
    parser.add_argument('package', nargs="?")
    parser.add_argument('--path', action='store_true', default=False, help="Return path to stats")
    parser.add_argument('--major', action='store_true', default=False)

    type_mx = parser.add_mutually_exclusive_group()
    type_mx.add_argument('--version', action='store_true', default=False, help="Only output data for versions")
    type_mx.add_argument('--system', action='store_true', default=False, help="Only output data for versions")

    mx = parser.add_mutually_exclusive_group()
    mx.add_argument('--total', '-T', action='store_true', default=False, help="Print total number of downloads")
    mx.add_argument('--total-system', action='store_true', default=False, help="Print total calculated based on system stats")
    parser.add_argument('--no-fetch', '-n', action='store_false', default=True, help="Print total", dest="fetch")
    return parser


STATS_DIR = Path.home() / ".local" / "state" / "pypi-stats-timeline"

def stats_path(package):
    return STATS_DIR / (package + ".json")

def read_stats(package):
    path = stats_path(package)

    if not path.exists():
        return []

    data = []

    with open(path) as stream:
        for line in stream:
            data.append(json.loads(line))

    return data

class StatsAdder:
    def __init__(self, package):
        self.package = package

    def __enter__(self):
       self.stream = open(stats_path(self.package), 'a')
       return self

    def add(self, x):
        self.stream.write(json.dumps(x) + "\n")

    def __exit__(self, *_):
        self.stream.close()


SYSTEM_URL = "https://pypistats.org/api/packages/{package}/system"
VERSIONS_URL = "https://pypistats.org/api/packages/{package}/python_minor"


def key(x):
    return (x.get("system") or "", x.get("version") or "", x["date"])

def main():
    args = make_parser().parse_args()

    if args.path:
        if args.package:
            print(stats_path(args.package))
        else:
            print(STATS_DIR)
        return

    if args.package is None:
        make_parser().print_help()
        return


    STATS_DIR.mkdir(exist_ok=True)

    if args.fetch:
        fetch(args.package)

    total = 0
    system_total = 0
    points = sort_points(read_stats(args.package))

    if args.major:
        points = group_minors(points)

    for x in points:
        if x.get("version", "") == "null":
            continue
        if x.get("system", "") == "null":
            continue

        if x.get("version"):
            total += x["downloads"]

        if x.get("system"):
            system_total += x["downloads"]

        if not (args.total or args.total_system):
            show = (args.system and x.get("system")) or (args.version and x.get("version")) or (not args.system and not args.version)
            if show:
                print(json.dumps(x))

    if args.total:
        print(total)
    if args.total_system:
        print(system_total)


def sort_points(points):
    return sorted(points, key=lambda x: (x["date"], x.get("version", ""), x.get("system", "")))



def group_minors(points):
    group_key = lambda x: (x["date"], "version" in x, x.get("version", ".").split(".")[0])
    for (_date, version_point, major), group_points in itertools.groupby(points, group_key):
        if not version_point:
            for p in group_points:
                yield p
        else:
            group_points = list(group_points)
            point = group_points[0]
            point["downloads"] = sum(p["downloads"] for p in group_points)
            point["version"] = major
            yield point

def fetch(package):
    stats = read_stats(package)
    existing_keys = set(key(d) for d in stats)

    response = urllib.request.urlopen(VERSIONS_URL.format(package=package))
    raw = response.read()
    minor_data = json.loads(raw)["data"]

    with StatsAdder(package) as stats:
        for x in sort_points(minor_data):
            x["version"] = x.pop("category")
            if key(x) not in existing_keys:
                stats.add(x)

    response = urllib.request.urlopen(SYSTEM_URL.format(package=package))
    raw = response.read()

    system_data = json.loads(raw)["data"]
    for x in system_data:
        x["system"] = x.pop("category")

    with StatsAdder(package) as stats:
        for x in sort_points(system_data):
            if key(x) not in existing_keys:
                stats.add(x)
