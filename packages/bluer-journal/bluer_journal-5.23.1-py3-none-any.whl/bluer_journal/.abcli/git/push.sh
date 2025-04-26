#! /usr/bin/env bash

function bluer_journal_git_push() {
    local options=$1
    local update_calendar=$(bluer_ai_option_int "$options" calendar 1)
    local do_push=$(bluer_ai_option_int "$options" push 1)
    local do_sync=$(bluer_ai_option_int "$options" sync 1)

    :

    [[ "$do_push" == 0 ]] &&
        return 0
    bluer_ai_git \
        $BLUER_JOURNAL_REPO.wiki \
        push \
        "@journal add" \
        ~increment_version
}
