from typing import List

from bluer_options.terminal import show_usage, xtra

from bluer_journal.help.git import push_options


def help_add(
    tokens: List[str],
    mono: bool,
) -> str:
    options = "".join(
        [
            xtra("~pull,", mono=mono),
            "todo",
        ]
    )

    args = [
        "[--title <YYYY-MM-DD>]",
        "[--verbose 1]",
    ]

    return show_usage(
        [
            "@journal",
            "add",
            f"[{options}]",
            "<message>",
            f"[{push_options(mono=mono)}]",
        ]
        + args,
        "add to journal.",
        mono=mono,
    )
