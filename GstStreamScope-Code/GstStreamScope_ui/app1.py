from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import glob

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

LOG_DIR = "/home/vboxuser/Documents/logs/DOT"  # Change this path if needed

@app.route("/api/latest-image", methods=["GET"])
def get_latest_image():
    """Find and return the most recent PNG file from the log directory."""
    try:
        png_files = glob.glob(os.path.join(LOG_DIR, "PAUSED_PLAYING-*.png"))
        if not png_files:
            return jsonify({"error": "No PNG files found"}), 404

        latest_png = max(png_files, key=os.path.getmtime)
        latest_filename = os.path.basename(latest_png)
        return jsonify({"latest": latest_filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/logs/DOT/<filename>")
def serve_image(filename):
    """Serve the PNG file from the log directory."""
    return send_from_directory(LOG_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
