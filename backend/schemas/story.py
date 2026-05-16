from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel

# anything Base = used as a parent class
# response is the response from API (returned to front end)
# reqiest is coming from front to backend 

class StoryOptionsScheme(BaseModel):
    text: str
    node_id: Optional[int] = None


class StoryNodeBase(BaseModel):
    content: str
    is_ending: bool = False
    is_winning_ending: bool = False

class CompleteStoryNodeResponse(StoryNodeBase):
    id: int
    options: List[StoryOptionsScheme] = []

    class Config:
        from_attribute = True

class StoryBase(BaseModel):
    title: str
    session_id: Optional[str] = None
    
    class Config:
        from_attribute = True

class CreateStoryRequest(BaseModel):
    theme: str


class CompleteStoryResponse(StoryBase):
    id: int 
    created_at: datetime
    root_node: CompleteStoryNodeResponse
    all_nodes: Dict[int, CompleteStoryNodeResponse]

    class Config:
        from_attribute = True