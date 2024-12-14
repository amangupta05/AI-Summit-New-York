import anthropic
from uagents import Agent, Context, Model
from typing import Optional, Dict, List
import asyncio
from models.chatBotMessage import ChatbotMessage
from models.qaPair import qaPair
import os 
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
class ChatBot:
    def __init__(self, model="claude-3-haiku-20240307"):
        """
        Initialize the chatbot and start the first interaction.
        """
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.model = model
        self.conversation_history = []
        self.current_question = "What do you know about AI?"
        self.current_response = ""

        self._ask_initial_question()

    def _ask_initial_question(self):
        """
        Synchronous method to ask the first question
        """
        self.conversation_history.append({
            "role": "assistant",
            "content": self.current_question
        })
        
        print("\nQuestion:", self.current_question)
        user_response = input("Your response: ")
        self.current_response = user_response
        
        self.conversation_history.append({
            "role": "user",
            "content": self.current_response
        })

    def get_last_qa(self) -> qaPair:
        """Get the most recent user response"""
        return qaPair(question=self.current_question,answer=self.current_response)

    async def ask_question(self, question: str):
        '''
        Ask the next question
        '''
        try:
            self.conversation_history.append({
                "role":"assistant",
                "content":self.current_question
            })
            self.current_question = question
            print("\nQuestion:", question)
            user_response = input("Your response: ")
            self.current_response = user_response
            self.conversation_history.append({
                "role":"user",
                "content":self.current_response
            })
        except Exception as e:
            error_msg = f"Error while asking question: {self.current_question}{str(e)}"
            return error_msg, ""

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history"""
        return self.conversation_history

    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []
        self.last_response = ""

