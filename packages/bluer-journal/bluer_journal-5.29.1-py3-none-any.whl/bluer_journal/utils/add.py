from blueness import module

from bluer_journal import NAME
from bluer_journal.classes.page import JournalPage
from bluer_journal.logger import logger


NAME = module.name(__file__, NAME)


def add_message(
    message: str,
    title: str,
    todo: bool = False,
    verbose: bool = False,
) -> bool:
    logger.info(
        "{}.add_message({}{}) -> {}".format(
            NAME,
            "✔️" if todo else "",
            message,
            title,
        )
    )

    page = JournalPage(
        title=title,
        verbose=verbose,
    )

    page.content += [
        "",
        f" - [ ] {message}" if todo else message,
    ]

    return page.save(
        verbose=verbose,
    )
