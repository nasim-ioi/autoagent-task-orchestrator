
"""
Agent definitions for AutoAgent Task Orchestrator.
"""
from typing import Dict
from pyautogen import AssistantAgent
from .config import get_azure_openai_config

PLANNER_SYSTEM_MESSAGE: str = (
    "You are Planner. Create a concise plan. Do not produce the final solution. "
    "Output: Understanding, Plan bullets, Success criteria."
)

EXECUTOR_SYSTEM_MESSAGE: str = (
    "You are Executor. Produce the final solution following the plan. "
    "If Critic feedback exists, revise accordingly. Be clear and structured."
)

CRITIC_SYSTEM_MESSAGE: str = (
    "You are Critic. Review the Executor output against the task and plan. "
    "Reply with either 'APPROVED' or 'REVISION REQUIRED' and bullet feedback. Be strict and specific."
)

def build_agents() -> Dict[str, AssistantAgent]:
    """
    Instantiates and returns the Planner, Executor, and Critic agents.

    Returns:
        dict: {"planner": PlannerAgent, "executor": ExecutorAgent, "critic": CriticAgent}
    """
    config = get_azure_openai_config()
    planner = AssistantAgent(
        name="Planner",
        system_message=PLANNER_SYSTEM_MESSAGE,
        llm_config=config,
    )
    executor = AssistantAgent(
        name="Executor",
        system_message=EXECUTOR_SYSTEM_MESSAGE,
        llm_config=config,
    )
    critic = AssistantAgent(
        name="Critic",
        system_message=CRITIC_SYSTEM_MESSAGE,
        llm_config=config,
    )
    return {"planner": planner, "executor": executor, "critic": critic}
