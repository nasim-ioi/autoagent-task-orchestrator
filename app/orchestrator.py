def run_single(task: str):

"""
Orchestration logic for single-agent, multi-agent, and comparison modes.
"""
from typing import Dict, Any
from .agents import build_agents
from .config import get_azure_openai_config
from pyautogen import AssistantAgent

def run_single(task: str) -> Dict[str, Any]:
    """
    Single-agent baseline: one LLM call to answer the task directly.

    Args:
        task (str): The user task prompt.
    Returns:
        dict: agent_messages, final_answer, metadata
    """
    config = get_azure_openai_config()
    agent = AssistantAgent(
        name="SingleAgent",
        system_message="You are a helpful assistant. Answer the user's task as best as possible.",
        llm_config=config,
    )
    messages = []
    response = agent.generate_reply(task)
    messages.append({
        "role": "assistant",
        "agent_name": "SingleAgent",
        "content": response,
    })
    return {
        "agent_messages": messages,
        "final_answer": response,
        "metadata": {
            "mode": "single",
            "model": config.get("deployment_name") or config.get("model"),
            "rounds": 1,
        },
    }



def run_multi(task: str, max_rounds: int = 2) -> Dict[str, Any]:
    """
    Multi-agent loop: Planner -> Executor -> Critic, with revision rounds.

    Args:
        task (str): The user task prompt.
        max_rounds (int): Maximum revision rounds.
    Returns:
        dict: agent_messages, final_answer, metadata
    """
    agents = build_agents()
    planner, executor, critic = agents["planner"], agents["executor"], agents["critic"]
    messages = []
    # 1. Planner creates plan
    plan = planner.generate_reply(task)
    messages.append({
        "role": "assistant",
        "agent_name": "Planner",
        "content": plan,
    })
    # 2. Executor produces solution
    exec_input = f"Task: {task}\nPlan:\n{plan}"
    exec_output = executor.generate_reply(exec_input)
    messages.append({
        "role": "assistant",
        "agent_name": "Executor",
        "content": exec_output,
    })
    rounds = 1
    while rounds <= max_rounds:
        # 3. Critic reviews
        critic_input = f"Task: {task}\nPlan:\n{plan}\nExecutor Output:\n{exec_output}"
        critic_output = critic.generate_reply(critic_input)
        messages.append({
            "role": "assistant",
            "agent_name": "Critic",
            "content": critic_output,
        })
        if "APPROVED" in critic_output.upper():
            break
        elif "REVISION REQUIRED" in critic_output.upper():
            # Executor revises
            exec_input = f"Task: {task}\nPlan:\n{plan}\nCritic Feedback:\n{critic_output}\nPrevious Output:\n{exec_output}"
            exec_output = executor.generate_reply(exec_input)
            messages.append({
                "role": "assistant",
                "agent_name": "Executor",
                "content": exec_output,
            })
            rounds += 1
        else:
            # If Critic output is unclear, stop to avoid infinite loop
            break
    return {
        "agent_messages": messages,
        "final_answer": exec_output,
        "metadata": {
            "mode": "multi",
            "model": get_azure_openai_config().get("deployment_name") or get_azure_openai_config().get("model"),
            "rounds": rounds,
        },
    }


def run_both(task: str, max_rounds: int = 2) -> Dict[str, Dict[str, Any]]:
    """
    Runs both single and multi-agent modes for comparison.

    Args:
        task (str): The user task prompt.
        max_rounds (int): Maximum revision rounds for multi-agent.
    Returns:
        dict: {'single': ..., 'multi': ...}
    """
    single = run_single(task)
    multi = run_multi(task, max_rounds)
    return {"single": single, "multi": multi}
