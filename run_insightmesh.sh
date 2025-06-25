#!/bin/bash

# InsightMesh - Combined Backend and Frontend Launcher
# This script starts both the backend FastAPI server and the Streamlit frontend

# Set colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print banner
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║  🔍 InsightMesh - AI-Powered Data Analysis Platform          ║"
echo "║      Powered by Google's Agentic Development Kit (ADK)       ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed. Please install Python 3 to continue.${NC}"
    exit 1
fi

# Check if required environment variables are set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo -e "${YELLOW}Warning: GOOGLE_API_KEY environment variable is not set.${NC}"
    echo -e "${YELLOW}Some features may not work correctly.${NC}"
    echo -e "${YELLOW}Set it using: export GOOGLE_API_KEY=\"your-gemini-api-key\"${NC}"
    echo ""
fi

# Function to check if a port is in use
is_port_in_use() {
    if command -v lsof &> /dev/null; then
        lsof -i:"$1" &> /dev/null
        return $?
    elif command -v netstat &> /dev/null; then
        netstat -tuln | grep -q ":$1 "
        return $?
    else
        # If neither lsof nor netstat is available, assume port is free
        return 1
    fi
}

# Check if ports are available
if is_port_in_use 8000; then
    echo -e "${RED}Error: Port 8000 is already in use. The backend server requires this port.${NC}"
    echo -e "${RED}Please stop any services using port 8000 and try again.${NC}"
    exit 1
fi

if is_port_in_use 8501; then
    echo -e "${RED}Error: Port 8501 is already in use. The Streamlit frontend requires this port.${NC}"
    echo -e "${RED}Please stop any services using port 8501 and try again.${NC}"
    exit 1
fi

# Function to install dependencies if needed
check_and_install_dependencies() {
    local req_file=$1
    local component=$2
    
    echo -e "${BLUE}Checking $component dependencies...${NC}"
    
    if [ ! -f "$req_file" ]; then
        echo -e "${RED}Error: $req_file not found.${NC}"
        return 1
    fi
    
    # Check if pip is installed
    if ! command -v pip &> /dev/null; then
        echo -e "${RED}Error: pip is not installed. Please install pip to continue.${NC}"
        return 1
    }
    
    # Install dependencies
    echo -e "${YELLOW}Installing $component dependencies...${NC}"
    pip install -r "$req_file"
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to install $component dependencies.${NC}"
        return 1
    fi
    
    echo -e "${GREEN}$component dependencies installed successfully.${NC}"
    return 0
}

# Start backend server
start_backend() {
    echo -e "${BLUE}Starting InsightMesh backend server...${NC}"
    
    # Check and install backend dependencies
    check_and_install_dependencies "requirements.txt" "backend"
    
    # Start the backend server
    cd "$(dirname "$0")"
    python main.py &
    BACKEND_PID=$!
    
    # Check if backend started successfully
    sleep 2
    if ! ps -p $BACKEND_PID > /dev/null; then
        echo -e "${RED}Error: Failed to start backend server.${NC}"
        return 1
    fi
    
    echo -e "${GREEN}Backend server started successfully (PID: $BACKEND_PID).${NC}"
    echo -e "${GREEN}API available at: http://localhost:8000${NC}"
    echo -e "${GREEN}API documentation: http://localhost:8000/docs${NC}"
    
    return 0
}

# Start frontend
start_frontend() {
    echo -e "${BLUE}Starting InsightMesh frontend...${NC}"
    
    # Check if frontend directory exists
    if [ ! -d "frontend" ]; then
        echo -e "${RED}Error: frontend directory not found.${NC}"
        return 1
    fi
    
    # Check and install frontend dependencies
    check_and_install_dependencies "frontend/requirements.txt" "frontend"
    
    # Start the frontend
    cd "$(dirname "$0")/frontend"
    streamlit run streamlit_app.py &
    FRONTEND_PID=$!
    
    # Check if frontend started successfully
    sleep 2
    if ! ps -p $FRONTEND_PID > /dev/null; then
        echo -e "${RED}Error: Failed to start frontend.${NC}"
        return 1
    fi
    
    echo -e "${GREEN}Frontend started successfully (PID: $FRONTEND_PID).${NC}"
    echo -e "${GREEN}Frontend available at: http://localhost:8501${NC}"
    
    return 0
}

# Function to handle cleanup on exit
cleanup() {
    echo -e "${YELLOW}Shutting down InsightMesh...${NC}"
    
    # Kill backend process
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo -e "${GREEN}Backend server stopped.${NC}"
    fi
    
    # Kill frontend process
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo -e "${GREEN}Frontend stopped.${NC}"
    fi
    
    echo -e "${GREEN}InsightMesh shutdown complete.${NC}"
    exit 0
}

# Set up trap to catch Ctrl+C and other termination signals
trap cleanup SIGINT SIGTERM

# Start the backend and frontend
start_backend
if [ $? -ne 0 ]; then
    cleanup
    exit 1
fi

start_frontend
if [ $? -ne 0 ]; then
    cleanup
    exit 1
fi

echo -e "${GREEN}InsightMesh is now running!${NC}"
echo -e "${BLUE}Press Ctrl+C to stop all services.${NC}"

# Keep the script running
while true; do
    sleep 1
done
