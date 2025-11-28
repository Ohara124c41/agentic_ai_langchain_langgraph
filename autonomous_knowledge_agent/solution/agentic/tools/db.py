from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@contextmanager
def session_scope(db_path: str) -> Iterator:
    """Context manager for SQLite sessions with commit/rollback safety."""
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
