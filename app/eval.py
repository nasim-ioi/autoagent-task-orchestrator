def evaluate_output(final_answer: str, rounds: int) -> dict:

"""
Evaluation metrics for agent outputs.
"""
import re
from typing import Dict

def evaluate_output(final_answer: str, rounds: int) -> Dict[str, object]:
  """
  Computes evaluation metrics for a run.

  Args:
    final_answer (str): The final answer string.
    rounds (int): Number of revision rounds.
  Returns:
    dict: {"rounds": int, "output_chars": int, "has_steps": bool}
  """
  output_chars = len(final_answer)
  # Heuristic: contains numbered steps or bullet points
  has_steps = bool(re.search(r"(\d+\. |\n- |\n\* )", final_answer))
  return {
    "rounds": rounds,
    "output_chars": output_chars,
    "has_steps": has_steps,
  }
