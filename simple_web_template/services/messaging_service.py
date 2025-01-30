import uuid
from typing import Optional, List
from simple_web_template.model.data_structures import Conversation
from simple_web_template.repositories.message_repository import MessageRepository


class MessagingService:
    def __init__(self, message_repository: MessageRepository):
        self.message_repository = message_repository

    def find_conversation(self, id: uuid.UUID) -> Optional[Conversation]:
        conversation = None

        for c in self.message_repository.conversations:
            if c.id == id:
                conversation = c

        return conversation

    def add_conversation(self, conversation: Conversation):
        self.message_repository.conversations.append(conversation)

    def list_conversations(self) -> List[Conversation]:
        return self.message_repository.conversations
