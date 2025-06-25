#!/bin/bash

# InsightMesh - Frontend Only Launcher
# This script starts only the Streamlit frontend without affecting the backend

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
echo "║  🔍 InsightMesh Frontend - Streamlit Dashboard               ║"
echo "║      (Frontend Only Mode - Assumes Backend is Running)       ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed. Please install Python 3 to continue.${NC}"
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo -e "${RED}Error: pip is not installed. Please install pip to continue.${NC}"
    exit 1
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

# Check if port 8501 is available
if is_port_in_use 8501; then
    echo -e "${RED}Error: Port 8501 is already in use. The Streamlit frontend requires this port.${NC}"
    echo -e "${RED}Please stop any services using port 8501 and try again.${NC}"
    exit 1
fi

# Check if backend is running
echo -e "${BLUE}Checking if backend API is available...${NC}"
if command -v curl &> /dev/null; then
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health | grep -q "200"; then
        echo -e "${GREEN}Backend API is running and healthy.${NC}"
    else
        echo -e "${YELLOW}Warning: Backend API is not responding at http://localhost:8000/health${NC}"
        echo -e "${YELLOW}Some features may not work correctly.${NC}"
        echo -e "${YELLOW}Make sure the backend server is running.${NC}"
    fi
else
    echo -e "${YELLOW}Warning: curl is not installed. Cannot check if backend API is running.${NC}"
    echo -e "${YELLOW}Make sure the backend server is running at http://localhost:8000${NC}"
fi

# Check if Streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo -e "${YELLOW}Streamlit is not installed. Installing required packages...${NC}"
    
    # Install from main requirements.txt which now includes Streamlit
    pip install -r requirements.txt
    
    # Check if installation was successful
    if ! command -v streamlit &> /dev/null; then
        echo -e "${RED}Error: Failed to install Streamlit. Please install it manually:${NC}"
        echo -e "${YELLOW}pip install streamlit==1.31.0${NC}"
        exit 1
    fi
fi

# Start the frontend
echo -e "${GREEN}Starting InsightMesh frontend...${NC}"
cd "$(dirname "$0")/frontend"
streamlit run streamlit_app.py &
FRONTEND_PID=$!

# Check if frontend started successfully
sleep 2
if ! ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${RED}Error: Failed to start frontend.${NC}"
    exit 1
fi

echo -e "${GREEN}Frontend started successfully (PID: $FRONTEND_PID).${NC}"
echo -e "${GREEN}Frontend available at: http://localhost:8501${NC}"
echo -e "${BLUE}Press Ctrl+C to stop the frontend.${NC}"

# Function to handle cleanup on exit
cleanup() {
    echo -e "${YELLOW}Shutting down InsightMesh frontend...${NC}"
    
    # Kill frontend process
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo -e "${GREEN}Frontend stopped.${NC}"
    fi
    
    echo -e "${GREEN}InsightMesh frontend shutdown complete.${NC}"
    exit 0
}

# Set up trap to catch Ctrl+C and other termination signals
trap cleanup SIGINT SIGTERM

# Keep the script running
while true; do
    sleep 1
done
