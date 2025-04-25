import os

from bluer_objects import file
from bluer_objects.env import abcli_path_git

from bluer_journal.env import BLUER_JOURNAL_REPO
from bluer_journal.logger import logger


class JournalPage:
    def __init__(
        self,
        title: str,
        verbose: bool = False,
    ):
        self.title = title
        self.load(verbose)

    @property
    def filename(self) -> str:
        return os.path.join(
            abcli_path_git,
            f"{BLUER_JOURNAL_REPO}.wiki",
            f"{self.title}.md",
        )

    def load(
        self,
        verbose: bool = False,
    ):
        _, self.content = file.load_text(
            self.filename,
            ignore_error=True,
            log=verbose,
        )

    def save(
        self,
        verbose: bool = False,
    ) -> bool:
        return file.save_text(
            self.filename,
            self.content,
            log=verbose,
        )
