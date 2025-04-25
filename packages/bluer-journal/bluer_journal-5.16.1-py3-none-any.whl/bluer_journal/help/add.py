from typing import List

from bluer_options.terminal import show_usage, xtra


def help_add(
    tokens: List[str],
    mono: bool,
) -> str:
    options = "".join(
        [
            xtra("~pull,~push,", mono=mono),
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
        ]
        + args,
        "add to journal.",
        mono=mono,
    )
