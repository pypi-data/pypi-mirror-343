#! /usr/bin/env bash

function test_bluer_journal_add() {
    local options=$1

    bluer_journal_add \
        ~push,$options \
        "this is a test" \
        --title test
}
