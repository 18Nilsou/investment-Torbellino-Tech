import os
import sys
import pytest

def run_tests():
    """Run all blockchain integration tests."""
    print("Running blockchain integration tests...")
    
    # Run all tests
    result = pytest.main([
        "market_sim/tests/unit/blockchain/",
        "market_sim/tests/integration/test_blockchain_market_sim.py",
        "-v"
    ])
    
    # Run performance tests separately (they take longer)
    if result == 0:
        print("\nRunning performance tests...")
        perf_result = pytest.main([
            "market_sim/tests/performance/test_blockchain_performance.py",
            "-v"
        ])
        
        if perf_result == 0:
            print("\n✅ All tests passed!")
            return 0
        else:
            print("\n⚠️ Performance tests failed.")
            return perf_result
    
    print("\n❌ Some tests failed.")
    return result

if __name__ == "__main__":
    sys.exit(run_tests())