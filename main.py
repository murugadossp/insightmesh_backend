from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import tempfile
import os
import logging
import glob
from datetime import datetime

# Google ADK imports
from google.adk.runners import InMemoryRunner
from root_agent.root_agent import root_agent
from sub_agents.ingestor.agent import ingestor_agent
from sub_agents.cleaner.agent import cleaner_agent
from sub_agents.analyzer.agent import analyzer_agent
from sub_agents.summarizer.agent import summarizer_agent

# Schema imports
from schemas.base import AppInfoResponse

# HTML Report Generator
from utils.html_report_generator import generate_html_report, save_html_report

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="InsightMesh API - Google ADK Data Insights",
    description="AI-powered data insights using Google Agentic ADK framework",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response models
class AnalysisResponse(BaseModel):
    success: bool
    message: str
    insights: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    processing_steps: Optional[list] = None

class AgentStatusResponse(BaseModel):
    agent_name: str
    status: str
    description: str

class PipelineStatusResponse(BaseModel):
    agents: list[AgentStatusResponse]
    total_agents: int

# Agent registry for the ADK framework
AGENT_REGISTRY = {
    "ingestor": ingestor_agent,
    "cleaner": cleaner_agent,
    "analyzer": analyzer_agent,
    "summarizer": summarizer_agent,
}

@app.get("/", response_model=AppInfoResponse, tags=["Root"])
def read_root():
    return AppInfoResponse(
        message="Welcome to InsightMesh API - Powered by Google Agentic ADK Framework"
    )

@app.get("/agents/status", response_model=PipelineStatusResponse, tags=["Agents"])
def get_agents_status():
    """Get status of all Google ADK agents in the pipeline"""
    agents_status = []
    
    for key, agent in AGENT_REGISTRY.items():
        agents_status.append(AgentStatusResponse(
            agent_name=agent.name,
            status="ready",
            description=agent.description or f"{key.title()} agent for data processing"
        ))
    
    return PipelineStatusResponse(
        agents=agents_status,
        total_agents=len(agents_status)
    )

@app.post("/analyze", response_model=AnalysisResponse, tags=["Data Insights"])
async def analyze_csv_data(file: UploadFile = File(...)):
    """
    Upload CSV file and get comprehensive data insights using Google ADK agents
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        logger.info(f"Processing file: {file.filename}")
        
        # Execute Google ADK agents step by step to get actual outputs
        logger.info("Running Google ADK Agents Pipeline")
        
        try:
            # Initialize shared state for the pipeline
            shared_state = {"uploaded_file": temp_file_path}
            processing_steps = []
            
            # Step 1: Run Ingestor Agent
            logger.info("Running Ingestor Agent")
            try:
                # Directly call the agent's tool function
                ingest_result = ingestor_agent.tools[0].func(temp_file_path)
                shared_state.update(ingest_result)
                processing_steps.append({
                    "step": "ingestor",
                    "agent": ingestor_agent.name,
                    "description": "Load and parse the uploaded CSV file",
                    "status": "completed",
                    "output": {
                        "filename": ingest_result.get("filename"),
                        "num_rows": ingest_result.get("num_rows"),
                        "num_columns": ingest_result.get("num_columns"),
                        "column_names": ingest_result.get("column_names")
                    }
                })
                logger.info(f"✅ Ingestor completed: {ingest_result.get('num_rows')} rows, {ingest_result.get('num_columns')} columns")
            except Exception as e:
                logger.error(f"Ingestor failed: {e}")
                processing_steps.append({
                    "step": "ingestor",
                    "agent": ingestor_agent.name,
                    "description": "Load and parse the uploaded CSV file",
                    "status": "failed",
                    "error": str(e)
                })
                raise HTTPException(status_code=500, detail=f"Data ingestion failed: {e}")
            
            # Step 2: Run Cleaner Agent
            logger.info("Running Cleaner Agent")
            try:
                dataframe = shared_state.get("dataframe")
                if dataframe is not None:
                    clean_result = cleaner_agent.tools[0].func(dataframe)
                    shared_state.update(clean_result)
                    processing_steps.append({
                        "step": "cleaner",
                        "agent": cleaner_agent.name,
                        "description": "Clean and validate the dataset",
                        "status": "completed",
                        "output": {
                            "null_summary": clean_result.get("null_summary"),
                            "suggestions": clean_result.get("suggestions")
                        }
                    })
                    logger.info(f"✅ Cleaner completed: {len(clean_result.get('suggestions', []))} cleaning suggestions")
                else:
                    raise Exception("No dataframe available from ingestor")
            except Exception as e:
                logger.error(f"Cleaner failed: {e}")
                processing_steps.append({
                    "step": "cleaner",
                    "agent": cleaner_agent.name,
                    "description": "Clean and validate the dataset",
                    "status": "failed",
                    "error": str(e)
                })
            
            # Step 3: Run Analyzer Agent
            logger.info("Running Analyzer Agent")
            try:
                dataframe = shared_state.get("dataframe")
                if dataframe is not None:
                    analysis_result = analyzer_agent.tools[0].func(dataframe)
                    shared_state.update(analysis_result)
                    processing_steps.append({
                        "step": "analyzer",
                        "agent": analyzer_agent.name,
                        "description": "Perform basic descriptive statistics",
                        "status": "completed",
                        "output": {
                            "numeric_summary": analysis_result.get("numeric_summary")
                        }
                    })
                    logger.info(f"✅ Analyzer completed: Statistical analysis generated")
                else:
                    raise Exception("No dataframe available for analysis")
            except Exception as e:
                logger.error(f"Analyzer failed: {e}")
                processing_steps.append({
                    "step": "analyzer",
                    "agent": analyzer_agent.name,
                    "description": "Perform basic descriptive statistics",
                    "status": "failed",
                    "error": str(e)
                })
            
            # Step 4: Run Summarizer Agent
            logger.info("Running Summarizer Agent")
            try:
                numeric_summary = shared_state.get("numeric_summary", {})
                cleaned = shared_state.get("null_summary", {})
                if numeric_summary:
                    summary_result = summarizer_agent.tools[0].func(numeric_summary, cleaned)
                    shared_state.update(summary_result)
                    processing_steps.append({
                        "step": "summarizer",
                        "agent": summarizer_agent.name,
                        "description": "Generate LLM-based summary of insights",
                        "status": "completed",
                        "output": {
                            "summary_text": summary_result.get("summary_text")
                        }
                    })
                    logger.info(f"✅ Summarizer completed: LLM summary generated")
                else:
                    raise Exception("No analysis results available for summarization")
            except Exception as e:
                logger.error(f"Summarizer failed: {e}")
                processing_steps.append({
                    "step": "summarizer",
                    "agent": summarizer_agent.name,
                    "description": "Generate LLM-based summary of insights",
                    "status": "failed",
                    "error": str(e)
                })
            
            # Extract final insights from the pipeline execution
            final_summary = shared_state.get("summary_text", "Analysis completed using Google ADK agents")
            
            # Compile comprehensive insights
            insights = {
                "framework": "Google Agentic ADK",
                "pipeline_execution": "completed",
                "data_info": {
                    "filename": shared_state.get("filename"),
                    "rows": shared_state.get("num_rows"),
                    "columns": shared_state.get("num_columns"),
                    "column_names": shared_state.get("column_names")
                },
                "cleaning_info": {
                    "null_summary": shared_state.get("null_summary"),
                    "suggestions": shared_state.get("suggestions")
                },
                "analysis_results": shared_state.get("numeric_summary"),
                "file_processed": temp_file_path
            }
            
        except Exception as e:
            logger.error(f"ADK Pipeline failed: {e}")
            raise HTTPException(status_code=500, detail=f"Google ADK pipeline failed: {e}")
        
        # Generate HTML Report
        analysis_data = {
            "insights": insights,
            "summary": final_summary,
            "processing_steps": processing_steps
        }
        
        try:
            html_content, report_id = generate_html_report(analysis_data, file.filename)
            report_path = save_html_report(html_content, report_id)
            logger.info(f"📄 HTML report generated: {report_path}")
            
            # Add report info to insights
            insights["html_report"] = {
                "report_id": report_id,
                "report_path": report_path,
                "report_url": f"/reports/{report_id}"
            }
        except Exception as e:
            logger.warning(f"Failed to generate HTML report: {e}")
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        return AnalysisResponse(
            success=True,
            message=f"Successfully analyzed {file.filename} using Google ADK agents. HTML report available at /reports/{report_id}",
            insights=insights,
            summary=final_summary,
            processing_steps=processing_steps
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during analysis: {e}")
        # Clean up temporary file if it exists
        if 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/agents/run-pipeline", response_model=AnalysisResponse, tags=["Agents"])
async def run_adk_pipeline(file: UploadFile = File(...)):
    """
    Run the complete Google ADK agent pipeline programmatically
    """
    return await analyze_csv_data(file)

@app.get("/agents/{agent_name}/info", tags=["Agents"])
def get_agent_info(agent_name: str):
    """Get detailed information about a specific ADK agent"""
    if agent_name not in AGENT_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
    
    agent = AGENT_REGISTRY[agent_name]
    return {
        "name": agent.name,
        "description": agent.description,
        "model": getattr(agent, 'model', 'Not specified'),
        "tools": [tool.__class__.__name__ for tool in getattr(agent, 'tools', [])],
        "status": "ready"
    }

@app.get("/reports", tags=["Reports"])
def list_reports():
    """List all available HTML reports"""
    try:
        output_dir = "output"
        if not os.path.exists(output_dir):
            return {"reports": [], "total": 0}
        
        report_files = glob.glob(os.path.join(output_dir, "*.html"))
        reports = []
        
        for file_path in sorted(report_files, key=os.path.getmtime, reverse=True):
            filename = os.path.basename(file_path)
            report_id = filename.replace('.html', '')
            file_stats = os.stat(file_path)
            
            reports.append({
                "report_id": report_id,
                "filename": filename,
                "created_at": datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
                "size_bytes": file_stats.st_size,
                "view_url": f"/reports/{report_id}"
            })
        
        return {
            "reports": reports,
            "total": len(reports),
            "message": f"Found {len(reports)} analysis reports"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list reports: {e}")

@app.get("/reports/{report_id}", response_class=HTMLResponse, tags=["Reports"])
def view_report(report_id: str):
    """View a specific HTML report"""
    try:
        output_dir = "output"
        report_path = os.path.join(output_dir, f"{report_id}.html")
        
        if not os.path.exists(report_path):
            raise HTTPException(status_code=404, detail=f"Report '{report_id}' not found")
        
        with open(report_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        return HTMLResponse(content=html_content)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load report: {e}")

@app.get("/reports/{report_id}/download", response_class=FileResponse, tags=["Reports"])
def download_report(report_id: str):
    """Download a specific HTML report"""
    try:
        output_dir = "output"
        report_path = os.path.join(output_dir, f"{report_id}.html")
        
        if not os.path.exists(report_path):
            raise HTTPException(status_code=404, detail=f"Report '{report_id}' not found")
        
        return FileResponse(
            path=report_path,
            filename=f"insightmesh_report_{report_id}.html",
            media_type="text/html"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download report: {e}")

@app.delete("/reports/{report_id}", tags=["Reports"])
def delete_report(report_id: str):
    """Delete a specific HTML report"""
    try:
        output_dir = "output"
        report_path = os.path.join(output_dir, f"{report_id}.html")
        
        if not os.path.exists(report_path):
            raise HTTPException(status_code=404, detail=f"Report '{report_id}' not found")
        
        os.remove(report_path)
        return {"message": f"Report '{report_id}' deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete report: {e}")

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint for the ADK-powered API"""
    return {
        "status": "healthy",
        "framework": "Google Agentic ADK",
        "agents_count": len(AGENT_REGISTRY),
        "agents": list(AGENT_REGISTRY.keys())
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
