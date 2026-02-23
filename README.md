# AutoAgent Task Orchestrator

A multi-agent system using AutoGen and Azure OpenAI to collaboratively solve tasks with Planner, Executor, and Critic agents. Supports iterative revision, single-agent baseline, and evaluation.

## Features
- Multi-agent (Planner, Executor, Critic) and single-agent baseline
- Azure OpenAI API (config via environment variables)
- CLI interface: run tasks in multi, single, or both modes
- Logs all agent messages and outputs to `runs/`
- Simple evaluation: output length, revision rounds, steps detection

## Setup
1. **Clone the repo**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment variables**
   - Copy `.env.example` to `.env` and fill in your Azure OpenAI details

## Example Usage
```bash
python -m app.main --task "Write a 5-step plan to deploy a FastAPI service on Azure." --mode multi --max_rounds 2
python -m app.main --task "Compare Azure RBAC vs AWS IAM in a concise table." --mode single
python -m app.main --task "Given requirements X, propose an approach and potential risks." --mode both
```

## Example Tasks
1. Write a 5-step plan to deploy a FastAPI service on Azure.
2. Compare Azure RBAC vs AWS IAM in a concise table.
3. Given requirements X, propose an approach and potential risks.

## Output
- Final answer(s) printed to console
- Evaluation summary printed
- Full run log saved to `runs/<timestamp>_<mode>.json`

## Project Structure
```
autoagent-task-orchestrator/
  app/
    __init__.py
    config.py
    agents.py
    orchestrator.py
    eval.py
    logging_utils.py
    main.py
  runs/
  tests/
  .env.example
  .gitignore
  requirements.txt
  README.md
```

## Requirements
- Python 3.11+
- AutoGen (pyautogen)
- Azure OpenAI credentials
