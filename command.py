from map import build_map, fit_image

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument(
    "command", metavar="command", type=str, 
)
args = parser.parse_args()
command = args.command

if command == "build":
	build_map()
