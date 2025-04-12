from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from datetime import datetime

app = Flask(__name__)

# Endpoint
@app.route("/get_embedding")
def get_embedding():
    return jsonify(message="Hello from Flask!")

# Cron Job Task
def scheduled_task():
    print(f"[{datetime.now()}] Cron job executed!")

# Scheduler setup
scheduler = BackgroundScheduler()
# Run every minute
scheduler.add_job(func=scheduled_task, trigger="cron", minute="*")
scheduler.start()

# Ensure scheduler shuts down when app exits
atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    app.run(debug=True)
