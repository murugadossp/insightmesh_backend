# This module defines the agent execution plan for the InsightMesh pipeline.
# Since AgentPlan and AgentStep are not available in the current Google ADK version,
# we'll use a simple dictionary-based approach for the pipeline steps.

def get_insightmesh_plan(user_goal: str) -> dict:
    """
    Returns a simple plan structure for the InsightMesh pipeline.
    This replaces the previous AgentPlan approach.
    """
    return {
        "name": "InsightMesh Full Pipeline",
        "user_goal": user_goal or "Analyze uploaded CSV and summarize",
        "steps": [
            {"key": "ingestor", "description": "Load and parse the uploaded CSV file."},
            {"key": "cleaner", "description": "Clean and validate the dataset."},
            {"key": "analyzer", "description": "Perform basic descriptive statistics."},
            {"key": "summarizer", "description": "Generate LLM-based summary of insights."}
        ]
    }
