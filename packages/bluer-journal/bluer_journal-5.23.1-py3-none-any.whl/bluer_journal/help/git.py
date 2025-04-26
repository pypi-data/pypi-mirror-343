from typing import List

from bluer_options.terminal import show_usage, xtra


def help_pull(
    tokens: List[str],
    mono: bool,
) -> str:
    options = xtra("~pull", mono=mono)

    return show_usage(
        [
            "@journal",
            "git",
            "pull",
            f"[{options}]",
            "[.|<object-name>]",
        ],
        "git -> journal.",
        mono=mono,
    )


def push_options(mono: bool):
    return xtra("~calendar,~push,~sync", mono=mono)


def help_push(
    tokens: List[str],
    mono: bool,
) -> str:

    return show_usage(
        [
            "@journal",
            "git",
            "push",
            f"[{push_options(mono=mono)}]",
        ],
        "journal -> git.",
        mono=mono,
    )


help_functions = {
    "pull": help_pull,
    "push": help_push,
}
