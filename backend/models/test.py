from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class TestCase(Base):
    __tablename__ = "test_cases"
    
    id = Column(Integer, primary_key=True, index=True)
    suite_id = Column(Integer, ForeignKey("test_suites.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    code = Column(Text, nullable=False)
    tags = Column(Text)  # JSON array
    status = Column(String(50), default="draft", index=True)  # draft, approved
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    suite = relationship("TestSuite", back_populates="tests")
    runs = relationship("TestRun", back_populates="test", cascade="all, delete-orphan")
