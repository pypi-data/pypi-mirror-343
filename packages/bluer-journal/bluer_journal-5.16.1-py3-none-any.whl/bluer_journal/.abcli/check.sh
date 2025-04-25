#! /usr/bin/env bash

function bluer_journal_check() {
    local repo_name
    for repo_name in \
        $BLUER_JOURNAL_REPO \
        $BLUER_JOURNAL_REPO.wiki; do
        if [[ ! -d "$abcli_path_git/$repo_name" ]]; then
            if [[ "$abcli_is_github_workflow" == true ]]; then
                pushd $abcli_path_git >/dev/null
                git clone https://github.com/kamangir/$repo_name.git
                [[ $? -ne 0 ]] && return 1
                popd >/dev/null
            else
                bluer_ai_git_clone $repo_name
                [[ $? -ne 0 ]] && return 1
            fi
        fi
    done

    return 0
}
