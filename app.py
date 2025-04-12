import json

from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from datetime import datetime

from embedding_generator import NewsPostVectorDB
from fetch_news import lambda_handler

app = Flask(__name__)

vector_db = NewsPostVectorDB()


@app.route("/search")
def search():
    query = request.args.get("query")
    limit = request.args.get("limit", default=5, type=int)

    if not query:
        return jsonify({"error": "Query parameter is required."}), 400

    try:
        results = vector_db.search_news(query=query, limit=limit)
        return jsonify({
            "query": query,
            "results_count": len(results),
            "results": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- SCHEDULED TASK ---
def fetch_news():
    print(f"[{datetime.now()}] Running fetch_news scheduled job...")
    try:
        with open("utils/fetch_news_config.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        for value in data.values():
            lambda_handler(value)
        print(f"[{datetime.now()}] fetch_news completed successfully.")
    except Exception as e:
        print(f"[{datetime.now()}] Error in fetch_news: {e}")

# --- SCHEDULER SETUP ---
scheduler = BackgroundScheduler()

# Run fetch_news at 10:00 AM and 6:00 PM daily
scheduler.add_job(func=fetch_news, trigger="cron", hour=10, minute=0)
scheduler.add_job(func=fetch_news, trigger="cron", hour=18, minute=0)

scheduler.start()

# Ensure scheduler shuts down properly on exit
atexit.register(lambda: scheduler.shutdown())

# --- RUN FETCH ON STARTUP ---
#fetch_news()

if __name__ == "__main__":
    app.run(debug=False)
