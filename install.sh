#!/bin/bash
echo "Starting Install..."

# Check if the sudo command is available
if ! command -v sudo &>/dev/null; then
    echo "Error: 'sudo' command is not available. Please install it or run this script as a superuser."
    exit 1
fi

# Install dependencies
echo "Installing dependencies python3, pip, venv, npm"
sudo apt-get update
sudo apt-get install -y python3 npm python3-pip python3-venv
cd api
python3 -m venv env && source .venv/bin/activate
pip3 install -r requirements.txt
echo "Dependencies installed successfully."

# Configure app
echo "Performing install and configuration."

cp .env.example .env

# Use nano to edit the .env file
nano .env

cd ..
cd webapp
npm install  # Uncomment this line if you want to install npm dependencies

echo "Installation and configuration completed. Run start.sh to begin."
