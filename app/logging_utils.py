def save_run_log(task, mode, agent_messages, final_answer, metadata, outdir="runs"):

"""
Logging utilities for saving run artifacts.
"""
import os
import json
from datetime import datetime
from typing import List, Dict, Any

def save_run_log(
    task: str,
    mode: str,
    agent_messages: List[Dict[str, Any]],
    final_answer: str,
    metadata: Dict[str, Any],
    outdir: str = "runs"
) -> str:
    """
    Saves a JSON artifact with timestamp, mode, task, agent messages, final answer, and metadata.

    Args:
        task (str): The user task prompt.
        mode (str): Run mode ("single" or "multi").
        agent_messages (list): List of agent message dicts.
        final_answer (str): Final answer string.
        metadata (dict): Metadata for the run.
        outdir (str): Output directory for logs.
    Returns:
        str: Path to the saved JSON file.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"{timestamp}_{mode}.json"
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, fname)
    data = {
        "timestamp": timestamp,
        "mode": mode,
        "task": task,
        "agent_messages": agent_messages,
        "final_answer": final_answer,
        "metadata": metadata,
    }
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return outpath
