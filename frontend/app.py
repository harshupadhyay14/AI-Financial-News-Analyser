from flask import Flask, render_template, request, jsonify, Response
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
BACKEND = os.getenv("BACKEND_API", "http://127.0.0.1:8000")


# ── page routes ────────────────────────────────────────────────────────────────
@app.route("/")
def index():      return render_template("index.html")

@app.route("/news")
def news():       return render_template("news.html")

@app.route("/dashboard")
def dashboard():  return render_template("dashboard.html")

@app.route("/companies")
def companies():  return render_template("companies.html")

@app.route("/chatbot")
def chatbot():    return render_template("chatbot.html")


# ── API proxy helper ───────────────────────────────────────────────────────────
def _proxy(path, params=None):
    """Forward a GET request to FastAPI and pass the raw JSON straight through."""
    try:
        r = requests.get(f"{BACKEND}{path}", params=params, timeout=60)
        # Pass status code + body through unchanged so the frontend gets the real data
        return Response(r.content, status=r.status_code, mimetype="application/json")
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Backend not running. Start uvicorn first."}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── API routes ─────────────────────────────────────────────────────────────────
@app.route("/api/news")
def api_news():
    return _proxy("/news")

@app.route("/api/metrics")
def api_metrics():
    return _proxy("/metrics")

@app.route("/api/companies")
def api_companies():
    return _proxy("/companies")

@app.route("/api/ask")
def api_ask():
    query = request.args.get("query", "")
    if not query:
        return jsonify({"error": "query parameter required"}), 400
    return _proxy("/ask", params={"query": query})

@app.route("/api/health")
def api_health():
    return _proxy("/")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)