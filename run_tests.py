#!/usr/bin/env python3
"""
Simple test runner for the chatbot project.
"""
import subprocess
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def run_tests():
    """Run basic tests for the chatbot project."""
    print("Running basic tests for sweet shop chatbot...")
    print("=" * 50)

    # Set environment variables for testing
    env = os.environ.copy()
    # Use Redis URL from environment or default for testing
    test_redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    env.update({"PYTHONPATH": ".", "REDIS_URL": test_redis_url})

    try:
        # Run pytest with basic configuration
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
            env=env,
            check=True,
        )

        print("\n" + "=" * 50)
        print("[SUCCESS] All tests passed!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"\n[FAILED] Tests failed with exit code: {e.returncode}")
        return False
    except Exception as e:
        print(f"\n[ERROR] Error running tests: {e}")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
