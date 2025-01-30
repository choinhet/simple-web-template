from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
import uuid


class Message(BaseModel):
    text: str
    timestamp: datetime = datetime.now()
    id: uuid.UUID = uuid.uuid4()

class Conversation(BaseModel):
    users: List[str]
    messages: List[Message] = Field(default_factory=list)
    created_at: datetime = datetime.now()
    id: uuid.UUID = uuid.uuid4()

class SendDTO(BaseModel):
    conversation_id: uuid.UUID
    message: Message

