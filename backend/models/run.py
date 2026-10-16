from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class TestRun(Base):
    __tablename__ = "test_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("test_cases.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(50), nullable=False, index=True)  # PENDING, RUNNING, PASSED, FAILED, TIMEOUT, ERROR
    duration_ms = Column(Integer)
    error_message = Column(Text)
    browser_version = Column(String(100))
    playwright_version = Column(String(50))
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime)
    
    test = relationship("TestCase", back_populates="runs")
    artifacts = relationship("Artifact", back_populates="run", cascade="all, delete-orphan")
