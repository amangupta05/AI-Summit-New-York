from uagents import Model
from typing import Optional, Dict, List


class ChatbotMessage(Model):
    content: str
    conversation_history: Optional[List[Dict[str, str]]] = []