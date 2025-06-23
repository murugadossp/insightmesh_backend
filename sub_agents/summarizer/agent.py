from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
import pandas as pd
from utils.llm_client import summarize_with_llm
from .prompt import SUMMARIZER_PROMPT

class SummarizerAgent(LlmAgent):
    def __init__(self):
        def summarizer_tool(numeric_summary: dict, cleaned: dict) -> dict:
            stats_text = pd.DataFrame(numeric_summary).to_string()
            summary = summarize_with_llm(stats_text)
            return {"summary_text": summary}

        super().__init__(
            name="summarizer",
            model="gemini-2.5-flash",
            description="Summarizes dataset statistics in natural language.",
            instruction=SUMMARIZER_PROMPT,
            tools=[
                FunctionTool(func=summarizer_tool)
            ]
        )

summarizer_agent = SummarizerAgent()
