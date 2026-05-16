# when story request submitted, first creates a job 
# (job = intent to make a story, tells stat7us of story creation)

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from db.database import Base

class StoryJob(Base):
    __tablename__ = "story_jobs"
    id = Column(Integer, primary_key=True, index=True) 
    job_id = Column(String, index=True, unique=True)
    session_id = Column(String, index=True)
    theme = Column(String)
    status = Column(String)
    story_id = Column(Integer, nullable=True)
    error = Column(String, nullable=True) #  nullable=True means it can have no value aka be null 
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 
    completed_at = Column(DateTime(timezone=True), nullable=True) 


