# app.py
# A simple Flask backend to demonstrate the Gorgias app workflow.
# It receives data from the Gorgias widget and stores it in memory.
# A public page can display the last submitted message.

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os

app = Flask(__name__)

# Enable Cross-Origin Resource Sharing for the Gorgias app to call this backend.
CORS(app)

# In-memory storage for simplicity. In a real app, use a database.
last_submission = {
    "ticket_id": "None",
    "message": "No message submitted yet."
}

# This is the public page that displays the last submitted message.
PUBLIC_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gorgias App Submissions</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style> body { font-family: 'Inter', sans-serif; } </style>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen">
    <div class="max-w-2xl w-full bg-white p-8 rounded-lg shadow-lg text-center">
        <h1 class="text-2xl font-bold text-gray-800 mb-4">Last Message from Gorgias App</h1>
        <div class="bg-gray-50 p-6 rounded-md border border-gray-200">
            <p class="text-sm text-gray-500">From Ticket ID: <strong class="text-gray-700">{{ ticket_id }}</strong></p>
            <p class="text-lg text-gray-900 mt-2 break-all">"{{ message }}"</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def public_page():
    """Renders the public page showing the last submission."""
    return render_template_string(PUBLIC_PAGE_TEMPLATE, **last_submission)

@app.route('/submit-from-gorgias', methods=['POST'])
def handle_gorgias_submission():
    """
    This is the endpoint your Gorgias App frontend will call.
    It receives the data and stores it.
    """
    global last_submission
    data = request.json
    
    print(f"Received data from Gorgias app: {data}")

    if not data or 'ticket_id' not in data or 'message' not in data:
        return jsonify({"status": "error", "message": "Invalid data received."}), 400

    last_submission['ticket_id'] = data.get('ticket_id', 'N/A')
    last_submission['message'] = data.get('message', 'No message content.')
    
    return jsonify({"status": "success", "message": "Data received and stored."})

if __name__ == '__main__':
    # This block is for running the app directly for local testing without Docker.
    app.run(host='0.0.0.0', port=5001, debug=True)
