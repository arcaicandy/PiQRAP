#!/bin/bash
if [[ $(tty) == "/dev/tty1" ]]; then
    echo "Starting PiQRAP"
    sudo chmod uga+rwx /tmp
    cd /home/pi/PiQRAP
    python3 piqrap.py
fi
