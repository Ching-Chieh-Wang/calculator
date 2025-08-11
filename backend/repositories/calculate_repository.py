from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from extensions import db

class Calculation(db.Model):
    __tablename__ = "calculations"

    id = db.Column(db.String(64), primary_key=True)
    expression = db.Column(db.String(256), nullable=False)
    result = db.Column(db.Float, nullable=True)
    error = db.Column(db.String(256), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "expression": self.expression,
            "result": self.result,
            "error": self.error,
            "timestamp": int(self.timestamp.timestamp() * 1000),
        }

class CalculateRepository:
    def save(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        calc = Calculation(
            id=entry["id"],
            expression=entry["expression"],
            result=entry.get("result"),
            error=entry.get("error"),
            timestamp=datetime.fromtimestamp(entry["timestamp"] / 1000, tz=timezone.utc)
        )
        db.session.add(calc)
        db.session.commit()
        return calc.to_dict()

    def list_newest_first(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        query = Calculation.query.order_by(Calculation.timestamp.desc())
        if limit:
            query = query.limit(limit)
        return [c.to_dict() for c in query.all()]
