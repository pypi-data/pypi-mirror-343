#! /usr/bin/env bash

function bluer_journal_add() {
    local options=$1
    local to_todo=$(bluer_ai_option_int "$options" todo 0)
    local do_pull=$(bluer_ai_option_int "$options" pull 1)
    local do_push=$(bluer_ai_option_int "$options" push 1)

    bluer_journal_check
    [[ $? -ne 0 ]] && return 1

    if [[ "$do_pull" == 1 ]]; then
        bluer_ai_git \
            $BLUER_JOURNAL_REPO.wiki \
            pull \
            ~all
        [[ $? -ne 0 ]] && return 1
    fi

    local message=$2
    if [[ -z "$message" ]]; then
        bluer_ai_log_error "@journal: add: message is empty."
        return 1
    fi

    python3 -m bluer_journal.add \
        --todo $to_todo \
        --message "$2" \
        "${@:3}"
    [[ $? -ne 0 ]] && return 1

    if [[ "$do_push" == 1 ]]; then
        bluer_ai_git \
            $BLUER_JOURNAL_REPO.wiki \
            push \
            "@journal add" \
            ~increment_version
    fi
}
