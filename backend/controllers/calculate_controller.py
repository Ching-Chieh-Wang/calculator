from flask import Blueprint, jsonify
from services.calculate_service import CalculateService
from repositories.calculate_repository import CalculateRepository
from validators.calculate_validator import calculate_validator
from middlewares.convert_intergers import convert_integers

bp = Blueprint("calculate", __name__)
_service = CalculateService(CalculateRepository())

@bp.post("/add")
@calculate_validator()
@convert_integers()
def add(num1, num2):
    try:
        return jsonify(_service.add(num1, num2))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.post("/subtract")
@calculate_validator()
@convert_integers()
def sub(num1, num2):
    try:
        return jsonify(_service.subtract(num1, num2))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.post("/multiply")
@calculate_validator()
@convert_integers()
def mul(num1, num2):
    try:
        return jsonify(_service.multiply(num1, num2))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.post("/divide")
@calculate_validator()
@convert_integers()
def div(num1, num2):
    try:
        return jsonify(_service.divide(num1, num2))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.get("/history")
def history():
    return jsonify(_service.history())

