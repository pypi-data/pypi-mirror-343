import argparse

from blueness import module
from blueness.argparse.generic import sys_exit
from bluer_options import string

from bluer_journal import NAME
from bluer_journal.utils.add import add_message
from bluer_journal.logger import logger

NAME = module.name(__file__, NAME)

parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "task",
    type=str,
    help="add | sync",
)
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

success = False
if args.task == "add":
    success = add_message(
        message=args.message,
        title=(
            args.title
            if args.title
            else string.pretty_date(
                include_time=False,
                as_filename=True,
            )
        ),
        todo=args.todo,
        verbose=args.verbose == 1,
    )
elif args.task == "sync":
    success = True
    logger.info("🪄")
else:
    success = None

sys_exit(logger, NAME, args.task, success)
