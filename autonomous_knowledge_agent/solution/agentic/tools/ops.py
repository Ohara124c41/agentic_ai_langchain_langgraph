from __future__ import annotations

import uuid
from pathlib import Path
from typing import Dict, Optional

from sqlalchemy.exc import SQLAlchemyError

from data.models import cultpass, udahub
from agentic.tools.db import session_scope

BASE_DIR = Path(__file__).resolve().parents[2]
CULTPASS_DB = BASE_DIR / "data" / "external" / "cultpass.db"
UDAHUB_DB = BASE_DIR / "data" / "core" / "udahub.db"


def _path_exists(path: Path) -> bool:
    return path.exists() and path.is_file()


def account_lookup(email: str, db_path: Path = CULTPASS_DB) -> Dict:
    if not _path_exists(db_path):
        return {"error": f"db_missing:{db_path}"}
    with session_scope(str(db_path)) as session:
        user = session.query(cultpass.User).filter(cultpass.User.email == email).first()
        if not user:
            return {"error": "user_not_found"}
        subscription = session.query(cultpass.Subscription).filter(cultpass.Subscription.user_id == user.user_id).first()
        reservations = session.query(cultpass.Reservation).filter(cultpass.Reservation.user_id == user.user_id).all()
        return {
            "user": {
                "id": user.user_id,
                "name": user.full_name,
                "email": user.email,
                "blocked": user.is_blocked,
            },
            "subscription": {
                "status": subscription.status if subscription else None,
                "tier": subscription.tier if subscription else None,
                "monthly_quota": subscription.monthly_quota if subscription else None,
            },
            "reservations": [
                {
                    "reservation_id": r.reservation_id,
                    "experience_id": r.experience_id,
                    "status": r.status,
                }
                for r in reservations
            ],
        }


def plan_update_or_refund(email: str, action: str = "credit", reason: str = "", db_path: Path = CULTPASS_DB) -> Dict:
    lookup = account_lookup(email, db_path)
    if lookup.get("error"):
        return lookup
    approved = action in {"credit", "downgrade"}
    note = f"Action={action}; reason={reason or 'n/a'}; approved={approved}"
    return {"action": action, "approved": approved, "note": note, "user": lookup.get("user")}


def log_ticket_note(ticket_id: str, content: str, db_path: Path = UDAHUB_DB) -> Dict:
    if not _path_exists(db_path):
        return {"error": f"db_missing:{db_path}"}
    try:
        with session_scope(str(db_path)) as session:
            message = udahub.TicketMessage(
                message_id=str(uuid.uuid4())[:8],
                ticket_id=ticket_id,
                role=udahub.RoleEnum.ai,
                content=content,
            )
            session.add(message)
        return {"ticket_id": ticket_id, "logged": True}
    except SQLAlchemyError as e:
        return {"error": f"db_error:{e}"}


def summarize_ticket_history(user_id: str, db_path: Path = UDAHUB_DB) -> str:
    if not _path_exists(db_path):
        return ""
    with session_scope(str(db_path)) as session:
        tickets = session.query(udahub.Ticket).filter(udahub.Ticket.user_id == user_id).all()
        if not tickets:
            return ""
        snippets = []
        for t in tickets:
            msgs = (
                session.query(udahub.TicketMessage)
                .filter(udahub.TicketMessage.ticket_id == t.ticket_id)
                .order_by(udahub.TicketMessage.created_at.desc())
                .limit(3)
                .all()
            )
            for m in msgs:
                snippets.append(f"[{t.ticket_id}/{m.role.name}] {m.content}")
        return "\n".join(snippets)
