import anthropic
from uagents import Agent, Context, Model, Bureau
from models.qaPair import qaPair
import json
import asyncio
from models.score import Score
from typing import Optional, Dict, List
import os
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
class QuestionGenerator:
    def __init__(self, api_key=None, model="claude-3-haiku-20240307"):
        """
        Initialize the Question Generation Agent with Anthropic Claude.
        
        Args:
            api_key (str, optional): Anthropic API key
            model (str, optional): Claude model to use
        """
        self.client = anthropic.Anthropic(api_key="ANTHROPIC_API_KEY")
        self.model = model

    async def generate_next_question(self, qa_pair: qaPair, history: List[Dict[str, str]], score: Score) -> str:
        """
        Generate the next question and determine emotional state using Claude.
        
        Args:
            conversation_history (list): Full conversation history
            user_response (str): Latest user response
        
        Returns:
            dict: Contains next question and emotional state
        """
        sample_json = '''
                {
                    "question": "What specific aspects of AI interest you the most?"
                }'''
        try:
            # Construct a comprehensive prompt for Claude
            prompt = f"""You are an advanced AI interviewer specializing in adaptive questioning. Generate the next question that are related to the AI that are based on this assessment:

            CURRENT EVALUATION:
            - Latest Question: {qa_pair.question}
            - User's Answer: {qa_pair.answer}
            - Skill Level: {score.evaluation['skill_level']}
            - Score: {score.evaluation['score']}/10

            CONVERSATION HISTORY:
            {str(history)}

            INSTRUCTIONS:
            1. Analyze the user's current skill level and previous responses
            2. Generate a question that:
            - Matches their demonstrated skill level
            - Builds upon previous topics
            - Encourages deeper exploration
            3. If the user shows mastery (score 8-10), increase complexity
            4. If the user struggles (score 1-4), adjust to more foundational concepts
            5. Maintain relevance to previous discussion while introducing new aspects

            RESPONSE FORMAT:
            Return only a JSON object with a single "question" field. Example:
            {sample_json}

            Your response must be a valid, parseable JSON object."""
            
            # Send request to Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            # Parse the response
            generated_content = response.content[0].text.strip()
        
            parsed_response = json.loads(generated_content)
            
            # Validate the response has required keys
            if "question" not in parsed_response:
                raise ValueError("Response missing required keys")
            
            # Return the parsed response
            return parsed_response["question"]

            
        except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                # Try to extract information from non-JSON response
                lines = generated_content.split('\n')
                score = next((int(line.split(':')[1].strip()) 
                            for line in lines if 'score' in line.lower()), 5)
                question = next((line.split(':')[1].strip() 
                            for line in lines if 'question' in line.lower()),
                            "Could you elaborate on that?")
