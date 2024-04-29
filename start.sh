#!/bin/bash

# Start Rasa server
cd rasa  # Change directory to your Rasa project directory
echo "Starting Rasa server"
rasa run -m models/20240424-161407-plain-equity.tar.gz --enable-api --cors "*" &

# Wait for Rasa server to start (adjust sleep duration if needed)
sleep 20

echo "Starting Flask application"
# Start Flask application
cd ..  # Move back to the root directory of your project
python app.py  # Start Flask application
