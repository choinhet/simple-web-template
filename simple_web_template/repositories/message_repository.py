from simple_web_template.model.data_structures import Conversation
from typing import List


class MessageRepository:
    def __init__(self):
        self.conversations: List[Conversation] = []
