import logging
from typing import Any

from flask import Flask, jsonify, request
import pandas as pd
from werkzeug.exceptions import HTTPException
from src.manhattan import get_manhattan_distance

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


def _validate_payload(data: Any) -> None:
    if data is None:
        raise ValueError("Request body must be valid JSON.")
    if not isinstance(data, dict):
        raise ValueError("JSON body must be an object with keys 'df1' and 'df2'.")
    if "df1" not in data or "df2" not in data:
        raise ValueError("JSON body must contain 'df1' and 'df2'.")
    if not isinstance(data["df1"], list) or not isinstance(data["df2"], list):
        raise ValueError("'df1' and 'df2' must be JSON arrays.")


@app.route("/manhattan", methods=["POST"])
def calculate_distance():
    data = request.get_json(silent=True)
    _validate_payload(data)

    df1 = pd.DataFrame(data["df1"])
    df2 = pd.DataFrame(data["df2"])

    logger.info("Received /manhattan request with shapes df1=%s df2=%s", df1.shape, df2.shape)
    dist = get_manhattan_distance(df1, df2)
    logger.info("Computed Manhattan distance: %.4f", dist)

    return jsonify({"distance": dist}), 200


@app.route("/", methods=["GET"])
def home():
    return jsonify(
        {
            "message": "Manhattan Distance API is running.",
            "endpoint": "/manhattan",
            "method": "POST",
        }
    ), 200


@app.errorhandler(ValueError)
def handle_value_error(exc: ValueError):
    logger.warning("Validation error: %s", exc)
    return jsonify({"error": str(exc)}), 400


@app.errorhandler(TypeError)
def handle_type_error(exc: TypeError):
    logger.warning("Type error: %s", exc)
    return jsonify({"error": str(exc)}), 400


@app.errorhandler(Exception)
def handle_unexpected_error(exc: Exception):
    if isinstance(exc, HTTPException):
        logger.warning("HTTP error %s: %s", exc.code, exc.description)
        return jsonify({"error": exc.description}), exc.code

    logger.exception("Unexpected error while handling request")
    return jsonify({"error": "Internal server error."}), 500


if __name__ == "__main__":
    app.run(debug=True)
