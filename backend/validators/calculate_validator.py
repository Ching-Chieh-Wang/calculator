from functools import wraps
from flask import request, jsonify

def calculate_validator():
    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            data = request.get_json(silent=True) or {}
            if "num1" not in data or "num2" not in data:
                return jsonify({"error": "num1 and num2 are required"}), 400
            try:
                num1 = float(data["num1"])
                num2 = float(data["num2"])
            except (TypeError, ValueError):
                return jsonify({"error": "num1 and num2 must be numbers"}), 400
            return fn(num1=num1, num2=num2, *args, **kwargs)
        return wrapper
    return deco