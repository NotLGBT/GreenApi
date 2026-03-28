from datetime import datetime, timezone
import os

from flask import Flask, jsonify


app = Flask(__name__)


@app.get("/")
def health():
    return jsonify(
        {
            "service": "greenapi-test",
            "status": "ok",
            "build": {
                "commit": os.getenv("BUILD_COMMIT", "unknown"),
                "user": os.getenv("BUILD_USER", "unknown"),
                "time": os.getenv("BUILD_TIME", "unknown"),
            },
            "served_at": datetime.now(timezone.utc).isoformat(),
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # nosemgrep: python.flask.security.audit.app-run-param-config.avoid_app_run_with_bad_host
