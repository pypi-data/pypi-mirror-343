"""Life coach agent for personal development."""
from typing import Optional
from langchain_core.memory import BaseMemory
from me2ai.llms.base import LLMProvider
from .base import CoachingAgent

class LifeCoachAgent(CoachingAgent):
    """Life coach agent that provides advice and support."""
    
    def __init__(self, role: str, system_prompt: str, llm_provider: LLMProvider, memory: Optional[BaseMemory] = None):
        """Initialize the life coach agent.
        
        Args:
            role: The role of the agent
            system_prompt: The system prompt that defines the agent's behavior
            llm_provider: The LLM provider to use
            memory: Optional memory instance
        """
        super().__init__(
            role=role,
            system_prompt=system_prompt,
            llm_provider=llm_provider,
            memory=memory
        )
