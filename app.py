from flask import Flask, jsonify, render_template, request
import os
import platform
import datetime

app = Flask(__name__)

APP_VERSION = "1.0.0"


@app.route("/")
def index():
    """Serve the main HTML page."""
    return render_template("index.html", version=APP_VERSION)


@app.route("/api/health")
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })


@app.route("/api/info")
def info():
    """Return runtime information about the container."""
    return jsonify({
        "app": "python-docker-app",
        "version": APP_VERSION,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "hostname": platform.node(),
        "container": os.environ.get("HOSTNAME", "unknown"),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })


@app.route("/api/echo", methods=["POST"])
def echo():
    """Echo back the JSON body sent by the client."""
    data = request.get_json(silent=True) or {}
    return jsonify({
        "received": data,
        "method": request.method,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })


@app.route("/api/add", methods=["POST"])
def add():
    """Add two numbers sent as JSON: {"a": 1, "b": 2}."""
    data = request.get_json(silent=True) or {}
    try:
        a = float(data.get("a", 0))
        b = float(data.get("b", 0))
        return jsonify({"result": a + b})
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid numbers provided"}), 400


@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(_):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
