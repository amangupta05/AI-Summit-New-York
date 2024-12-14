import os
from dotenv import load_dotenv
from uagents import Agent, Context, Model
from typing import Dict
import logging
import openai

# Load environment variables from a .env file
load_dotenv()

# Retrieve the OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configure OpenAI client
openai.api_key = OPENAI_API_KEY

# Define message models
class EmotionalWrapperInput(Model):
    """
    Input model for Emotional Wrapper.
    """
    question: str
    emotional_state: str
    user_level: str  # e.g., beginner, intermediate, advanced

class EmotionalWrapperResponse(Model):
    """
    Response model for Emotional Wrapper.
    """
    toned_question: str
    learning_path: str

class EmotionalWrapperAgent:
    def __init__(self):
        """
        Initialize the Emotional Wrapper Agent.
        """
        self.agent = Agent(
            name="emotional_wrapper_agent",
            port=8002,
            seed="emotional_wrapper_seed",
            endpoint=["http://127.0.0.1:8002/submit"],  # Localhost endpoint
        )
        self._register_handlers()

    def _generate_toned_response(self, question: str, emotional_state: str) -> str:
        """
        Generate a toned question using OpenAI API.

        Args:
            question (str): The raw question to tone.
            emotional_state (str): The emotional state of the user.

        Returns:
            str: A toned question.
        """
        try:
            prompt = f"""
            You are an empathetic AI assistant that adjusts the tone of questions based on the user's emotional state.
            
            ### Input:
            Question: {question}
            Emotional State: {emotional_state}

            ### Task:
            Rewrite the question to match the user's emotional state:
            - If anxious: Make it calm and reassuring.
            - If excited: Reflect the energy and curiosity.
            - If confused: Simplify and clarify the question.
            - If neutral: Keep the tone balanced and engaging.

            ### Output:
            Return only the rewritten question.
            """
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=100,
                temperature=0.7,
            )
            return response.choices[0].text.strip()
        except Exception as e:
            logging.error(f"Error generating toned response: {e}")
            return "Sorry, I couldn't adjust the question's tone. Could you provide more details?"

    def _generate_learning_path(self, user_level: str) -> str:
        """
        Generate a recommended learning path based on the user's level.

        Args:
            user_level (str): The skill level of the user (beginner, intermediate, advanced).

        Returns:
            str: A suggested learning path.
        """
        learning_paths = {
            "beginner": (
                "1. Start with an introduction to AI concepts.\n"
                "2. Learn about machine learning basics (e.g., supervised and unsupervised learning).\n"
                "3. Explore beginner-friendly tools like Teachable Machine or Scratch for AI.\n"
                "4. Practice with simple datasets (e.g., Iris dataset) using Python."
            ),
            "intermediate": (
                "1. Deepen your understanding of machine learning algorithms (e.g., decision trees, SVMs).\n"
                "2. Learn about neural networks and basic deep learning frameworks like TensorFlow or PyTorch.\n"
                "3. Work on intermediate-level projects, such as building a sentiment analysis tool.\n"
                "4. Explore computer vision or natural language processing (NLP)."
            ),
            "advanced": (
                "1. Master advanced topics like reinforcement learning and GANs.\n"
                "2. Optimize machine learning pipelines for real-world deployment.\n"
                "3. Explore state-of-the-art models like transformers (e.g., BERT, GPT).\n"
                "4. Contribute to open-source AI projects or research papers."
            ),
        }
        return learning_paths.get(user_level.lower(), "No specific learning path available.")

    def _register_handlers(self):
        """
        Register message handlers for the agent.
        """
        @self.agent.on_message(model=EmotionalWrapperInput)
        async def handle_emotional_wrapper(ctx: Context, sender: str, msg: EmotionalWrapperInput):
            """
            Handle incoming messages to adjust tone and provide a learning path.

            Args:
                ctx (Context): The communication context.
                sender (str): The sender of the message.
                msg (EmotionalWrapperInput): Input message containing question, emotional state, and user level.
            """
            # Generate toned question
            toned_question = self._generate_toned_response(msg.question, msg.emotional_state)
            
            # Generate learning path
            learning_path = self._generate_learning_path(msg.user_level)
            
            # Create response
            response = EmotionalWrapperResponse(
                toned_question=toned_question,
                learning_path=learning_path,
            )
            # Send response back
            await ctx.send(sender, response)

        @self.agent.on_interval(period=10)
        async def log_status(ctx: Context):
            """
            Periodically log agent's activity.
            """
            ctx.logger.info("Emotional Wrapper Agent is running.")

    def run(self):
        """
        Run the Emotional Wrapper Agent.
        """
        self.agent.run()

# Run the agent
if __name__ == "__main__":
    emotional_wrapper = EmotionalWrapperAgent()
    print(f"Assessing Agent Address: {emotional_wrapper.agent.address}")
    emotional_wrapper.run()
