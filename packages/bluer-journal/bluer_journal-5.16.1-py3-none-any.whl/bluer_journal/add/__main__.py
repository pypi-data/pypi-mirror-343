import argparse

from blueness import module
from blueness.argparse.generic import sys_exit

from bluer_journal import NAME
from bluer_journal.add.functions import add_message
from bluer_journal.logger import logger

NAME = module.name(__file__, NAME)

parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "--message",
    type=str,
)
parser.add_argument(
    "--title",
    type=str,
    default="",
)
parser.add_argument(
    "--todo",
    type=int,
    default=0,
    help="0 |1",
)
parser.add_argument(
    "--verbose",
    type=int,
    default=0,
    help="0 |1",
)
args = parser.parse_args()

success = add_message(
    message=args.message,
    title=args.title,
    todo=args.todo,
    verbose=args.verbose == 1,
)

sys_exit(logger, NAME, "", success)
