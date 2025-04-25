from typing import List

from bluer_options.terminal import show_usage, xtra
from bluer_ai.help.generic import help_functions as generic_help_functions

from bluer_journal import ALIAS
from bluer_journal.help.add import help_add

help_functions = generic_help_functions(plugin_name=ALIAS)

help_functions.update(
    {
        "add": help_add,
    }
)
