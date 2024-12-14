
import os
from google import genai
from google.genai import types
from uagents import Agent, Context, Model

# Ensure required API key is set
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

# Configure the Gemini client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Define message structure
class Message(Model):
    message: str

# Create the Assessing Agent
assessing_agent = Agent(
    name="assessing_agent",
    port=8001,
    seed="assessing_agent_seed",
    endpoint=["http://127.0.0.1:8001/submit"],  # Localhost for testing
)

# Gemini evaluation logic
@assessing_agent.on_message(model=Message)
async def evaluate_answer(ctx: Context, sender: str, msg: Message):
    """
    Evaluates the user input and sends back the evaluation result.
    """
    try:
        grounding_information = "What is machine learning and how does it differ from traditional programming?"
        user_answer = msg.message

        # Combine grounding and user input for evaluation
        contents = (
            f"Grounding Information: {grounding_information}\n\n"
            f"User Answer: {user_answer}\n\n"
            "You are an AI evaluator scoring answers related to AI knowledge. "
            "Evaluate the given answer based on the following criteria:\n\n"
            "1. *Accuracy:* Is the information correct? (3 points)\n"
            "2. *Depth:* Does the answer explain the concept well? (3 points)\n"
            "3. *Relevance:* Is the answer related to the question? (2 points)\n"
            "4. *Clarity:* Is the answer clear and easy to understand? (2 points)\n\n"
            "Provide a score between 1 and 10, where 1 is the worst and 10 is the best. "
            "Additionally, classify the question's level as one of the following: "
            "\"beginner,\" \"intermediate,\" or \"expert.\"\n\n"
            "**Output only in the following format:**\n{\"score\": 5, \"level\": \"beginner\"}\n"
        )

        # Generate response
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction='Evaluate the answer based on the grounding information provided.',
                temperature=0.3,
            ),
        )

        # Send back the evaluation result
        await ctx.send(sender, Message(message=response.text))

    except Exception as e:
        await ctx.send(sender, Message(message=f"Error during evaluation: {e}"))

# Periodic message for debugging
@assessing_agent.on_interval(period=5)
async def periodic_hello(ctx: Context):
    """
    Periodically logs a message to verify agent's activity.
    """
    ctx.logger.info("Assessing Agent is active and ready.")

if __name__ == "__main__":
    # Print the agent's address for reference
    print(f"Assessing Agent Address: {assessing_agent.address}")
    assessing_agent.run()
