from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
import pandas as pd
from .prompt import ANALYZER_PROMPT

class AnalyzerAgent(LlmAgent):
    def __init__(self):
        def analysis_tool(dataframe: pd.DataFrame) -> dict:
            stats = dataframe.describe(include="all").to_dict()
            return {"numeric_summary": stats}

        super().__init__(
            name="analyzer",
            description="Performs statistical summary of numerical data.",
            instruction=ANALYZER_PROMPT,
            tools=[
                FunctionTool(func=analysis_tool)
            ]
        )

analyzer_agent = AnalyzerAgent()
