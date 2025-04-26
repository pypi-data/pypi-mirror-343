import re
import calendar

from blueness import module

from bluer_journal import NAME
from bluer_journal.classes.page import JournalPage
from bluer_journal.logger import logger


NAME = module.name(__file__, NAME)


def sync_calendar(
    title: str,
    verbose: bool = False,
) -> bool:
    if bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", title)):
        return True

    logger.info(f"{NAME}.sync_calendar({title})")

    title_pieces = [int(piece) for piece in title.split("-")]
    year = title_pieces[0]
    month = title_pieces[0]

    if verbose:
        logger.info(f"+= {year}...")
    year_page = JournalPage(
        title=str(year),
        verbose=verbose,
    )
    for month in range(1, 13):
        if verbose:
            logger.info(f"+= {year}-{month:02d}...")
        message_ = f"- [[{year}-{month:02d}]]"
        if message_ not in year_page.content:
            year_page.content += [message_]

        month_page = JournalPage(
            title=f"{year}-{month:02d}",
            verbose=verbose,
        )
        _, last_day = calendar.monthrange(year, month)
        for day in range(1, last_day + 1):
            message_ = f"- [[{year}-{month:02d}-{day:02d}]]"
            if message_ not in month_page.content:
                month_page.content += [message_]
        if not month_page.save(verbose=verbose):
            return False

    return year_page.save(verbose=verbose)
