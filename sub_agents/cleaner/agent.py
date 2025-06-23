from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
import pandas as pd
from .prompt import CLEANER_PROMPT

class CleanerAgent(LlmAgent):
    def __init__(self):
        def cleaning_tool(dataframe: pd.DataFrame) -> dict:
            nulls = dataframe.isnull().sum().to_dict()
            suggestions = [f"Fill missing values in {col}" for col, count in nulls.items() if count > 0]
            return {"null_summary": nulls, "suggestions": suggestions}

        super().__init__(
            name="cleaner",
            description="Detects missing values and provides cleaning suggestions.",
            instruction=CLEANER_PROMPT,
            tools=[
                FunctionTool(func=cleaning_tool)
            ]
        )

cleaner_agent = CleanerAgent()
