#!/bin/bash
echo "Starting..."

# Check if the gnome-terminal command is available
if command -v gnome-terminal &>/dev/null; then
  # Open Terminal Windows
  gnome-terminal -- bash -c "cd webapp && npm start" &
  gnome-terminal -- bash -c "cd api && python3 -m venv env && source .venv/bin/activate && python3 server.py" &
  
  # Sleep to keep the script running and the terminal windows open
  sleep 99999
else
  echo "Error: gnome-terminal is not installed or not in your PATH. Edit start.sh"
fi

