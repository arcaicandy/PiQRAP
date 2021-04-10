#!/bin/bash
if [[ $(tty) == "/dev/tty1" ]]; then
    echo "Starting PiQRAP"
    cd /home/pi/PiQRAP
    python3 piqrap.py
fi