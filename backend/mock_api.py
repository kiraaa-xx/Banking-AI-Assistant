from flask import Flask, send_from_directory, jsonify, request
import os

# Get the absolute path to the frontend/dist folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DIST_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend", "dist"))

# Configure Flask to serve static files from the build directory
# We set static_url_path to '/' so that files like /assets/main.js are served automatically
app = Flask(__name__, static_folder=DIST_DIR, static_url_path='/')

print(f"--- SERVER LOGS ---")
print(f"Base Directory: {BASE_DIR}")
print(f"Seeking Frontend at: {DIST_DIR}")
if os.path.exists(DIST_DIR):
    print("Frontend folder: FOUND")
    if os.path.exists(os.path.join(DIST_DIR, "index.html")):
        print("index.html: FOUND")
    else:
        print("index.html: MISSING (Check your 'npm run build' output)")
else:
    print("Frontend folder: MISSING")
print(f"-------------------\n")

# 1. API Endpoints (Must come before the catch-all/error handlers)
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    print(f"API Request: {user_message}")
    
    return jsonify({
        "response": f"Hello from mock backend! You said: {user_message}",
        "intent": "GENERAL",
        "category": "GENERAL",
        "confidence": 1.0
    })

# 2. Main Page Route
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# 3. Catch-all: If a file isn't found (like /stats), send index.html for React Router to handle
@app.errorhandler(404)
def not_found(e):
    # This handles both SPA routing and any missing files
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8501))
    print(f"Starting server at http://127.0.0.1:{port}")
    # Run with host 0.0.0.0 for LAN access
    app.run(host="0.0.0.0", port=port, debug=False)