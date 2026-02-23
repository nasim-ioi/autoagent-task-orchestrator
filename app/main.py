
"""
CLI entrypoint for AutoAgent Task Orchestrator.
"""
import click
from .orchestrator import run_single, run_multi, run_both
from .logging_utils import save_run_log
from .eval import evaluate_output

@click.command()
@click.option('--task', required=True, help='Task prompt for the agent(s).')
@click.option('--mode', required=True, type=click.Choice(['single', 'multi', 'both']), help='Run mode.')
@click.option('--max_rounds', default=2, show_default=True, help='Max revision rounds for multi-agent.')
def main(task: str, mode: str, max_rounds: int):
    """
    CLI entry for AutoAgent Task Orchestrator.

    Args:
        task (str): The user task prompt.
        mode (str): Run mode (single, multi, both).
        max_rounds (int): Max revision rounds for multi-agent.
    """
    results = {}
    if mode == 'single':
        result = run_single(task)
        results['single'] = result
    elif mode == 'multi':
        result = run_multi(task, max_rounds)
        results['multi'] = result
    elif mode == 'both':
        results = run_both(task, max_rounds)
    # Logging and evaluation
    for m in results:
        res = results[m]
        eval_metrics = evaluate_output(res['final_answer'], res['metadata']['rounds'])
        log_path = save_run_log(
            task=task,
            mode=m,
            agent_messages=res['agent_messages'],
            final_answer=res['final_answer'],
            metadata={**res['metadata'], **eval_metrics},
        )
        print(f"\n=== {m.upper()} FINAL ANSWER ===\n{res['final_answer']}\n")
        print(f"Evaluation: {eval_metrics}")
        print(f"Log saved: {log_path}\n")
    if mode == 'both':
        print("=== COMPARISON SUMMARY ===")
        for m in ['single', 'multi']:
            res = results[m]
            eval_metrics = evaluate_output(res['final_answer'], res['metadata']['rounds'])
            print(f"{m.title()}: chars={eval_metrics['output_chars']}, rounds={eval_metrics['rounds']}, has_steps={eval_metrics['has_steps']}")

if __name__ == '__main__':
    main()
