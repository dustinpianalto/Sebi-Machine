#!/bin/bash

# 20th June 2018
# Esp: added a trap here, as it otherwise attempts to restart when given
# the interrupt signal. This is really annoying over SSH when I have
# a 1-second lag anyway.
trap "echo 'Received interrupt. Exiting.'; exit 0" SIGINT

# Also loads the venv if it is present.
[ -d .venv/bin ] && source .venv/bin/activate && echo "Entered venv." || echo "No venv detected."

until python -m src; do 
    # Added colouring to ensure the date of shutdown and the exit code stands
    # out from the other clutter in the traceback that might have been output.
    echo -e "\e[0;31m[$(date --utc)]\e[0m Sebi-Machine shutdown with error \e[0;31m$?\e[0m. Restarting..." >&2
    sleep 1
done
