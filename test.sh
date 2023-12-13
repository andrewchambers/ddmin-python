#!/usr/bin/env bash

set -eu

ddmin_script="./ddmin.py"
test_input="./test_input.txt"
test_script="./test_interesting.sh"


if ! test -f "$ddmin_script"
then
    echo "please run from the directory containing $ddmin_script."
    exit 1
fi

setup() {
    echo "This is a test file." > "$test_input"
    echo "It contains several lines." >> "$test_input"
    echo "One of these lines is interesting." >> "$test_input"
    echo "Others are not." >> "$test_input"
    echo '#!/bin/bash' > "$test_script"
    echo "grep -q 'interesting' \"$test_input\"" >> "$test_script"
    chmod +x "$test_script"
}

cleanup() {
    rm "$test_input" "$test_script"
}

test_line_wise() {
    setup
    python3 "$ddmin_script" --interesting "$test_script" --to-minimize "$test_input"
    if test "$(cat $test_input)" = "One of these lines is interesting."; then
        echo "Line-wise minimization test passed."
    else
        echo "Line-wise minimization test failed."
    fi
    cleanup
}

test_byte_wise() {
    setup
    python3 "$ddmin_script" -b --interesting "$test_script" --to-minimize "$test_input"
    if test "$(cat $test_input)" = "interesting"; then
        echo "Byte-wise minimization test passed."
    else
        echo "Byte-wise minimization test failed."
    fi
    cleanup
}

test_line_wise
test_byte_wise
