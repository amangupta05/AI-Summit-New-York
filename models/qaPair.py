from uagents import Model
from typing import Optional, Dict, List


class qaPair(Model):
    question: str
    answer: str