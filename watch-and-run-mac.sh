#!/bin/bash

readonly PROGNAME=$(basename $0)
readonly ARGS="$@"

usage() {
    cat <<-EOF
    Usage: $PROGNAME <file/folder to watch> <command to run>

    Run command whenever specified file or folder is changed.

    OPTIONS:
        -c      Don't clear console before run.
        -h      Show this help.

    EXAMPLE:
        $PROGNAME -c . ./run_tests.sh
EOF
}

while getopts "hc" OPTION
do
    case $OPTION in
        h)
            usage
            exit 0
            ;;
        c)
            CLEAR_CONSOLE=1
            ;;
        ?)
            usage
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

if [[ -z "$1" ]]; then
    >&2 echo "Requires file or directory."
    usage
    exit 1
fi
if [[ ! -a $1 ]]; then
    >&2 echo "Directory does not exist."
    usage
    exit 1
fi
if [[ -z "$2" ]]; then
    >&2 echo "Requires command."
    usage
    exit 1
fi

watch_and_run() {
    TO_WATCH=$1
    shift 1
    if [[ -z "$CLEAR_CONSOLE" ]]; then
        clear
    fi
    "$@"
    if [[ -z "$CLEAR_CONSOLE" ]]; then
        fswatch -1 -o -e '\.git|\.ropeproject' "$TO_WATCH" | (while read; do clear; "$@"; done)
    else
        fswatch -1 -o -e '\.git|\.ropeproject' "$TO_WATCH" | (while read; do "$@"; done)
    fi
}

watch_and_run "$@"
