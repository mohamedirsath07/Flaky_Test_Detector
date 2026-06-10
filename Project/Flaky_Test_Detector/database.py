import datetime
from typing import List, Dict, Any
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import logging

logger = logging.getLogger(__name__)

# SQLite connection string - local database file
DATABASE_URL = "sqlite:///results.db"

# Engine setup
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Needed for SQLite in multi-threaded app
)

# Session factory setup
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class for models
Base = declarative_base()


class FlakyTestResult(Base):
    """SQLAlchemy model for storing flaky test detection results."""
    __tablename__ = "flaky_tests"

    id = Column(Integer, primary_key=True, index=True)
    test_name = Column(String, index=True, nullable=False)
    flakiness_score = Column(Float, nullable=False)
    severity = Column(String, nullable=False)
    total_runs = Column(Integer, nullable=False)
    pass_count = Column(Integer, nullable=False)
    fail_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


def get_db():
    """
    Dependency generator function to handle DB session lifecycle.
    Yields:
        SessionLocal: SQLAlchemy session instance
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def initialize_database():
    """Creates all tables defined in the metadata."""
    logger.info("Initializing database: results.db")
    Base.metadata.create_all(bind=engine)


def save_detection_results(results: List[Dict[str, Any]]):
    """
    Saves a list of detection results to the database.
    
    Args:
        results: List of dictionaries containing flaky test metrics.
    """
    db = SessionLocal()
    try:
        for result in results:
            if not result.get("flaky"):
                continue  # Only save flaky tests
                
            db_record = FlakyTestResult(
                test_name=result["test_name"],
                flakiness_score=result["flakiness_score"],
                severity=result["severity"],
                total_runs=result["total_runs"],
                pass_count=result["pass_count"],
                fail_count=result["fail_count"]
            )
            db.add(db_record)
        db.commit()
        logger.info(f"Saved {len([r for r in results if r.get('flaky')])} flaky tests to database.")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save results: {e}")
        raise
    finally:
        db.close()


def get_all_results() -> List[Dict[str, Any]]:
    """
    Retrieves all flaky test results from the database.
    
    Returns:
        List of dictionary representations of the records.
    """
    db = SessionLocal()
    try:
        records = db.query(FlakyTestResult).all()
        return [
            {
                "id": r.id,
                "test_name": r.test_name,
                "flakiness_score": r.flakiness_score,
                "severity": r.severity,
                "total_runs": r.total_runs,
                "pass_count": r.pass_count,
                "fail_count": r.fail_count,
                "created_at": r.created_at.isoformat() if r.created_at else None
            }
            for r in records
        ]
    finally:
        db.close()
