from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Artifact(Base):
    __tablename__ = "artifacts"
    
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("test_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)  # screenshot, trace, console_log, network_log
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    run = relationship("TestRun", back_populates="artifacts")
