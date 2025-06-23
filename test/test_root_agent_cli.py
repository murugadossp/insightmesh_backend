# test/test_root_agent_cli.py

import sys
import os
from root_agent.root_agent import root_agent

DEFAULT_CSV_PATH = "sample_data/sample_sales_data.csv"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        csv_path = DEFAULT_CSV_PATH
        print(f"[INFO] No CSV path provided. Using default: {csv_path}")
    else:
        csv_path = sys.argv[1]

    if not os.path.exists(csv_path):
        print(f"[ERROR] File not found: {csv_path}")
        sys.exit(1)

    result = root_agent.invoke({"uploaded_file": csv_path})

    print("\n=== ✅ Final Output (from final_summary) ===")
    print(result.get("final_summary", "No summary generated."))
