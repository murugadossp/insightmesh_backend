from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from sub_agents.ingestor.agent import ingestor_agent
from sub_agents.cleaner.agent import cleaner_agent
from sub_agents.analyzer.agent import analyzer_agent
from sub_agents.summarizer.agent import summarizer_agent
from .prompt import ROOT_AGENT_PROMPT

root_agent = LlmAgent(
    name="insightmesh_coordinator",
    model="gemini-2.5-pro",
    description=(
        "InsightMesh Coordinator orchestrates a structured analysis pipeline: "
        "it loads a CSV, cleans the data, runs descriptive analysis, and generates "
        "a final natural-language summary using an LLM."
    ),
    instruction=ROOT_AGENT_PROMPT,
    tools=[
        AgentTool(agent=ingestor_agent),
        AgentTool(agent=cleaner_agent),
        AgentTool(agent=analyzer_agent),
        AgentTool(agent=summarizer_agent),
    ],
    output_key="final_summary",
)
