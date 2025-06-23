from fastapi import FastAPI
from agents import ingestion_agent, cleaning_agent, analysis_agent, summarizer_agent

app = FastAPI(title="InsightMesh API")

app.include_router(ingestion_agent.router)
app.include_router(cleaning_agent.router)
app.include_router(analysis_agent.router)
app.include_router(summarizer_agent.router)