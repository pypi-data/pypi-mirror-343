#! /usr/bin/env bash

function test_bluer_journal_add() {
    local options=$1

    bluer_journal_add \
        ,$options \
        "remind me that Mathematics is the voice of God." \
        ~push, \
        --title test
}
