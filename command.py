from map import build_map

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument(
    "command", metavar="command", type=str, 
)
args = parser.parse_args()
command = args.command

if command == "build":
	build_map()

# if command == "insert":
# 	name = input("Name")