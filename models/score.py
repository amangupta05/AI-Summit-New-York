from uagents import Model
from typing import Optional, Dict, List

class Score(Model):
    evaluation: dict = {
        "skill_level": str,  # One of: "Beginner", "Intermediate", "Advanced"
        "score": int  # Value between 1 and 10
    }