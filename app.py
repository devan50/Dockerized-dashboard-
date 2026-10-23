
from flask import Flask, render_template
import os
import redis

app = Flask(__name__)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    decode_responses=True
)

@app.route("/")
def home():
    try:
        visits = redis_client.incr("visits")
        redis_status = "Connected"
    except redis.RedisError:
        visits = "Unavailable"
        redis_status = "Disconnected"

    return render_template(
        "index.html",
        visits=visits,
        redis_status=redis_status
    )

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

