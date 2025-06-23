
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
import pandas as pd
from .prompt import INGESTOR_PROMPT

class IngestorAgent(LlmAgent):
    def __init__(self):
        def ingestion_tool(path: str) -> dict:
            df = pd.read_csv(path)
            return {
                "dataframe": df,
                "filename": path,
                "num_rows": len(df),
                "num_columns": len(df.columns),
                "column_names": df.columns.tolist(),
            }

        super().__init__(
            name="ingestor",
            description="Loads a CSV file into a DataFrame",
            instruction=INGESTOR_PROMPT,
            tools=[
                FunctionTool(func=ingestion_tool)
            ]
        )

ingestor_agent = IngestorAgent()
