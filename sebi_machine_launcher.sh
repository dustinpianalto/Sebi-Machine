#!/bin/bash

# 20th June 2018
# Esp: added a trap here, as it otherwise attempts to restart when given
# the interrupt signal. This is really annoying over SSH when I have
# a 1-second lag anyway.
trap "echo 'Received interrupt. Exiting.'; exit 0" SIGINT SIGTERM

# Also loads the venv if it is present.
[ -d .venv/bin ] && source .venv/bin/activate && echo "Entered venv." || echo "No venv detected."

function git-try-pull() {
    git pull --all
}

FAIL_COUNTER=0

while true; do
    if [ ${FAIL_COUNTER} -eq 4 ]; then
        echo -e "\e[0;31mFailed four times in a row. Trying to repull.\e[0m"
        git-try-pull
        let FAIL_COUNTER=0
    fi

    # Just respawn repeatedly until sigint.
    python3.6 -m src
    EXIT_STATUS=${?}
    if [ ${EXIT_STATUS} -ne 0 ]; then
        let FAIL_COUNTER=${FAIL_COUNTER}+1
    else
        let FAIL_COUNTER=0
    fi

    # Added colouring to ensure the date of shutdown and the exit code stands
    # out from the other clutter in the traceback that might have been output.
    echo -e "\e[0;31m[$(date --utc)]\e[0m Sebi-Machine shutdown with error \e[0;31m${EXIT_STATUS}\e[0m. Restarting..." >&2

    sleep 1
done

