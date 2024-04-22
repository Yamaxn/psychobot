#!/bin/bash

# Start Rasa server
cd rasa  # Change directory to your Rasa project directory
echo "Starting Rasa server"
rasa run --port 5005 &  # Start Rasa server in the background

# Wait for Rasa server to start (adjust sleep duration if needed)
sleep 10

echo "Starting Flask application"
# Start Flask application
cd ..  # Move back to the root directory of your project
python3 app.py  # Start Flask application
