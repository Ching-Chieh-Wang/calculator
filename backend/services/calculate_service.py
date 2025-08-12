import uuid
import time
from typing import Dict, Any, List, Optional
from repositories.calculate_repository import CalculateRepository


class CalculateService:
    """
    Service layer for arithmetic operations + persistence of results/history.
    Keeps controller thin and isolates business rules (e.g., div by zero).
    """

    def __init__(self, repo: Optional[CalculateRepository] = None):
        self.repo = repo or CalculateRepository()

    # -------- helpers --------
    def _now_ms(self) -> int:
        return int(time.time() * 1000)

    def _save_ok(self, expression: str, result) -> Dict[str, Any]:
        entry = {
            "id": str(uuid.uuid4()),
            "expression": expression,
            "result": result,
            "error": None,
            "timestamp": self._now_ms(),
        }
        return self.repo.save(entry)

    def _save_err(self, expression: str, error: str) -> Dict[str, Any]:
        entry = {
            "id": str(uuid.uuid4()),
            "expression": expression,
            "result": None,
            "error": error,
            "timestamp": self._now_ms(),
        }
        return self.repo.save(entry)

    # -------- operations --------
    def add(self, num1, num2) -> Dict[str, Any]:
        res = num1 + num2
        return self._save_ok(f"{num1} + {num2}", res)

    def subtract(self, num1, num2) -> Dict[str, Any]:
        res = num1 - num2
        return self._save_ok(f"{num1} - {num2}", res)

    def multiply(self, num1, num2) -> Dict[str, Any]:
        res = num1 * num2
        return self._save_ok(f"{num1} * {num2}", res)

    def divide(self, num1, num2) -> Dict[str, Any]:
        if num2 == 0:
            # Persist the failed attempt, then raise for controller to 400 it
            self._save_err(f"{num1} / {num2}", "division by zero")
            raise ZeroDivisionError("division by zero")
        res = num1 / num2
        return self._save_ok(f"{num1} / {num2}", res)

    # -------- queries --------
    def history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        return self.repo.list_newest_first(limit=limit)