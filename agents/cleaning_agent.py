from adk.agent import Agent
import pandas as pd

class CleaningAgent(Agent):
    def run(self, context):
        df = context.get("dataframe")
        if df is None:
            raise ValueError("No dataframe found in context.")

        nulls = df.isnull().sum().to_dict()
        suggestions = [
            f"Consider filling {count} missing values in '{col}'." 
            for col, count in nulls.items() if count > 0
        ]

        context["null_summary"] = nulls
        context["cleaning_suggestions"] = suggestions
        context["cleaning_notes"] = (
            "No missing values found. Dataset is clean." if not suggestions else "Some missing values detected."
        )

        print(f"[CleaningAgent] Null summary: {nulls}")
        return context