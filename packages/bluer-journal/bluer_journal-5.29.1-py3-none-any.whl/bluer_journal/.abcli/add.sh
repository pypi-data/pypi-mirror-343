#! /usr/bin/env bash

function bluer_journal_add() {
    local options=$1
    local to_todo=$(bluer_ai_option_int "$options" todo 0)
    local do_pull=$(bluer_ai_option_int "$options" pull 1)

    bluer_journal_git_pull pull=$do_pull
    [[ $? -ne 0 ]] && return 1

    local message=$2
    if [[ -z "$message" ]]; then
        bluer_ai_log_error "@journal: add: message is empty."
        return 1
    fi

    local push_options=$3

    python3 -m bluer_journal.utils \
        add \
        --todo $to_todo \
        --message "$2" \
        "${@:4}"
    [[ $? -ne 0 ]] && return 1

    bluer_journal_git_push $push_options
}
