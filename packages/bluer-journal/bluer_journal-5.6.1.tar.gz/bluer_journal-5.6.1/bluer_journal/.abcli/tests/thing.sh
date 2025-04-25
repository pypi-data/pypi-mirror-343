#! /usr/bin/env bash

function test_bluer_journal_thing() {
    local options=$1

    local test_options=$2

    bluer_ai_eval ,$options \
        "echo 📜 bluer-journal: test: thing: $test_options: ${@:3}."
}

