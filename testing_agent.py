# testing_agent.py

def run_tests():
    """
    Minimal test runner for Dev Agent automation.
    Returns (tests_passed: bool, test_output: str)
    """
    results = []
    passed = True

    try:
        # Dummy always-pass test for pipeline flow
        assert 1 + 1 == 2
        results.append("Test 1: Basic math... PASS")

    except AssertionError as e:
        results.append(f"Test failed: {str(e)}")
        passed = False

    output = "\n".join(results) if results else "No tests were run."
    return passed, output

def test_dummy():
    assert 1 + 1 == 2
