from adk.agent import Agent
import pandas as pd

class AnalysisAgent(Agent):
    def run(self, context):
        df = context.get("dataframe")
        if df is None:
            raise ValueError("No dataframe found in context.")

        numeric_cols = df.select_dtypes(include=["number"]).columns
        summary = {
            col: {
                "mean": round(df[col].mean(), 2),
                "sum": round(df[col].sum(), 2),
                "min": round(df[col].min(), 2),
                "max": round(df[col].max(), 2),
            }
            for col in numeric_cols
        }

        context["numeric_summary"] = summary
        context["analysis_notes"] = "Basic summary generated for all numeric columns."

        print(f"[AnalysisAgent] Summary for numeric columns: {summary}")
        return context