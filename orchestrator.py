from uagents import Agent, Context, Model, Bureau
from QuestionGenerator import QuestionGenerator
from ChatBot import ChatBot
from models.qaPair import qaPair
from models.chatBotMessage import ChatbotMessage
from models.question import Question
from skillEvaluator import SkillEvaluator
from models.score import Score
import asyncio
import logging

# Set the log level to INFO
logging.basicConfig(level=logging.ERROR)
# Create the agents
interface_agent = Agent(
    name="interface_agent",
    seed="Interface Agent Recovery Phrase",
    port=8000,
    endpoint=["http://localhost:8000/interface"]
)

question_generator_agent = Agent(
    name="question_generator_agent",
    seed="Question Generator Agent Recovery Phrase",
    port=8000,
    endpoint=["http://localhost:8000/qga"]
)

# Initialize the components
interface = ChatBot()
question_generator = QuestionGenerator()
skill_evaluator = SkillEvaluator()

scores = []
conversation_history = []

@interface_agent.on_event("startup")
async def startup(ctx: Context):
    """Initialize conversation on startup"""
    # ctx.logger.info("Interface is starting")
    qa_pair = interface.get_last_qa()
    await ctx.send(question_generator_agent.address, qa_pair)

@interface_agent.on_message(Question)
async def handle_interface_message(ctx: Context, sender: str, msg: Question):
    """Handle messages received by interface agent"""
    # ctx.logger.info(f"Received message from {sender}")
    await interface.ask_question(msg.question)
    qa_pair = interface.get_last_qa()
    conversation_history.append(interface.get_conversation_history)
    await ctx.send(question_generator_agent.address, qa_pair)

@question_generator_agent.on_message(qaPair)
async def handle_generator_message(ctx: Context, sender: str, msg: qaPair):
    """Handle messages received by question generator"""
    try:
        score = await skill_evaluator.evaluate_response(msg)
        scores.append(score)
        response = await question_generator.generate_next_question(
            msg,
            conversation_history,
            score
        )
        response_message = Question(question=response)#change this
        await ctx.send(sender, response_message)
        
    except Exception as e:
        # ctx.logger.error(f"Error in question generator: {e}")
        error_message = Question(question="Could you tell me more about that?")
        await ctx.send(sender, error_message)

def run():
    """Run the bureau"""
    bureau = Bureau()
    bureau.add(question_generator_agent)
    bureau.add(interface_agent)

    
    # Run the bureau directly
    bureau.run()

if __name__ == "__main__":
    # Run without explicit asyncio.run()
    run()