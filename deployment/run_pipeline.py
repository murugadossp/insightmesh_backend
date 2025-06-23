
# deployment/run_pipeline.py

import sys
import time
import logging
from agent_plan import get_insightmesh_plan
from sub_agents.ingestor.agent import ingestor_agent
from sub_agents.cleaner.agent import cleaner_agent
from sub_agents.analyzer.agent import analyzer_agent
from sub_agents.summarizer.agent import summarizer_agent

AGENT_REGISTRY = {
    "ingestor": ingestor_agent,
    "cleaner": cleaner_agent,
    "analyzer": analyzer_agent,
    "summarizer": summarizer_agent,
}

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_intermediate_state(state, step_key):
    filename = f"intermediate_{step_key}.json"
    try:
        import json
        with open(filename, "w") as f:
            json.dump({k: str(v) for k, v in state.items()}, f, indent=2)
        logging.info(f"Intermediate output written to {filename}")
    except Exception as e:
        logging.warning(f"Could not write intermediate state: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deployment/run_pipeline.py <path_to_csv>")
        sys.exit(1)

    csv_path = sys.argv[1]
    plan = get_insightmesh_plan("Business summary from CSV")
    shared_state = {"uploaded_file": csv_path}

    for step in plan.steps:
        agent = AGENT_REGISTRY[step.key]
        print(f"\n🔹 Running agent: {agent.name}")

        start_time = time.time()
        shared_state = agent.run(shared_state)
        elapsed = time.time() - start_time

        print(f"✅ Completed in {elapsed:.2f}s")
        log_intermediate_state(shared_state, step.key)

    final_output = shared_state.get("final_summary", "No summary produced.")
    print("\n=== ✅ Final Summary ===")
    print(final_output)

    with open("summary.txt", "w") as f:
        f.write(final_output)
    print("📄 Final summary written to summary.txt")
