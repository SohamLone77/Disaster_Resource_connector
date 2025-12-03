import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from main_agent import run_agent

if __name__ == "__main__":
    print("=== Disaster Resource Connector Demo ===")
    test_inputs = [
        "I need shelter and food after the hurricane",
        "Where can I find medical help?",
        "How do I apply for government assistance?",
        "Emergency shelter needed now!"
    ]
    
    for i, input_msg in enumerate(test_inputs, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Input: {input_msg}")
        print(f"Output: {run_agent(input_msg)}")
        print("-" * 50)
