from adk.agent import Agent
from utils.llm_client import summarize_with_llm
import pandas as pd

class SummarizerAgent(Agent):
    def run(self, context):
        df = context.get("dataframe")
        if df is None:
            raise ValueError("No dataframe available for summarization.")

        # Generate statistical summary
        stats_text = df.describe(include="all").to_string()
        summary = summarize_with_llm(stats_text)
        context["summary_text"] = summary

        print(f"[SummarizerAgent] Summary generated.")
        return context