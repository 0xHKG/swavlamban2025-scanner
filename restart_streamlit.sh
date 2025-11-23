#!/bin/bash
# Kill ALL streamlit processes
killall -9 streamlit 2>/dev/null
sleep 2

# Clear Python cache
find /home/gogi/Desktop/swav-registration -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find /home/gogi/Desktop/swav-registration -name "*.pyc" -delete 2>/dev/null

# Start ONE instance
cd /home/gogi/Desktop/swav-registration/frontend
streamlit run app.py --server.port 8501 --server.headless true
