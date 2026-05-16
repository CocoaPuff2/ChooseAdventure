import uuid
from typing import Optional 
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.story import Story, StoryNode
from models.job import StoryJob
from schemas.story import (
    CompleteStoryNodeResponse, CompleteStoryResponse, CreateStoryRequest
)
from schemas.job import StoryJobResponse
from core.story_generator import StoryGenerator


# backend URL/api/stories/endpoint 
#endpoint is the specific url, like create_story

router = APIRouter(
    prefix="/stories",
    tags=["stories"]
)

# session identifies the browser when interacting with a website 
# sessions can expire, meaning that  data is cleared 
def get_session_id(session_id: Optional[str] = Cookie(None)):
    if not session_id: 
        session_id = str(uuid.uuid4())
    return session_id

@router.post("/create", response_model=StoryJobResponse)
def create_story(
    request: CreateStoryRequest,
    background_tasks: BackgroundTasks, 
    response: Response, 
    session_id: str = Depends(get_session_id), 
    db: Session = Depends(get_db)

):
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    
    # call LLM to create the story for us 
    job_id = str(uuid.uuid4())

    # create a job 
    job = StoryJob(
        job_id=job_id, 
        session_id=session_id, 
        theme=request.theme, 
        status="pending"
    )

    # add job to database 
    db.add(job)
    db.commit()

    # TODO: add background tasks, generate story 
    background_tasks.add_task(
        generate_story_task, 
        job_id=job_id, 
        theme=request.theme, 
        session_id=session_id
    )


    return job 

def generate_story_task(job_id: str, theme: str, session_id: str):
    db = SessionLocal() # important line to not clog up background tasks 

    try:
        # look for job 
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()

        if not job:
            return
        
        try: 
            job.status = "processing"
            db.commit()

            story = StoryGenerator.generate_story(db, session_id, theme)

            job.story_id = story.id # update story id
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()
            
        except Exception as e: 
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()

    finally:
        db.close()

# retrieve finished story 
@router.get("/{story_id}/complete", response_model=CompleteStoryResponse)

def get_complete_story(story_id: int, db: Session = Depends(get_db)):
    # looks for story 
    # TODO STORY NOT BEING FOUND 
    story = db.query(Story).filter(Story.id == story_id).first()
    
    if not story:
        raise HTTPException(status_code=404, detail="Story not found!!")
    
    complete_story = build_complete_story_tree(db, story)
    return complete_story 



def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    # return the complete story tree
    # looks at all nodes that we created in the database of the story generator
    # gets all the ones that ref this story 
    nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all()

    node_dict = {}
    for node in nodes:
        node_response = CompleteStoryNodeResponse(
            id=node.id, 
            content=node.content,
            is_ending=node.is_ending, 
            is_winning_ending=node.is_winning_ending, 
            options=node.options
        )
        node_dict[node.id] = node_response

    # looks at all nodes, search for root node 
    root_node = next((node for node in nodes if node.is_root), None)
    if not root_node:
        raise HTTPException(status_code=500, detail="Story root node not found")
    
    return CompleteStoryResponse (
        id=story.id, 
        title=story.title, 
        session_id=story.session_id, 
        created_at=story.created_at, 
        root_node=node_dict[root_node.id], 
        all_nodes=node_dict
    )