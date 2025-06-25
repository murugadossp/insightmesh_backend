#!/bin/bash

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
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Navigate to the frontend directory
cd "$(dirname "$0")"

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

# Check if Streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo -e "${YELLOW}Streamlit is not installed. Installing required packages...${NC}"
    pip install -r requirements.txt
    
    # Check if installation was successful
    if ! command -v streamlit &> /dev/null; then
        echo -e "${RED}Error: Failed to install Streamlit. Please install it manually:${NC}"
        echo -e "${YELLOW}pip install streamlit==1.31.0${NC}"
        exit 1
    fi
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

# Run the Streamlit app
echo -e "${GREEN}Starting InsightMesh frontend...${NC}"
streamlit run streamlit_app.py

# Check if Streamlit started successfully
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to start Streamlit app.${NC}"
    echo -e "${YELLOW}Try running it manually:${NC}"
    echo -e "${YELLOW}cd $(pwd) && streamlit run streamlit_app.py${NC}"
    exit 1
fi
