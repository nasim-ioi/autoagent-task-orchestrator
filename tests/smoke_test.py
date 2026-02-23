# Minimal smoke test for orchestrator
from app.orchestrator import run_single, run_multi

def test_single():
    """Test single-agent baseline."""
    result = run_single("Say hello in 3 words.")
    assert isinstance(result['final_answer'], str)
    assert result['final_answer']

def test_multi():
    """Test multi-agent loop."""
    result = run_multi("Say hello in 3 words.", max_rounds=1)
    assert isinstance(result['final_answer'], str)
    assert result['final_answer']

def run():
    """Run all smoke tests."""
    test_single()
    test_multi()
    print("Smoke tests passed.")

if __name__ == "__main__":
    run()
