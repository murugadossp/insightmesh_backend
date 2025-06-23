from adk.agent import Agent
import pandas as pd
import os

class IngestorAgent(Agent):
    def run(self, context):
        file_path = context.get("file_path")
        if not file_path or not os.path.exists(file_path):
            raise ValueError("File path not found in context.")

        df = pd.read_csv(file_path)
        context["dataframe"] = df
        context["filename"] = os.path.basename(file_path)
        context["num_rows"] = len(df)
        context["num_columns"] = len(df.columns)
        context["column_names"] = list(df.columns)

        print(f"[IngestorAgent] Loaded {context['num_rows']} rows from {file_path}")
        return context