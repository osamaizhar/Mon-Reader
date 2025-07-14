#!/usr/bin/env python3
"""
Mon-Reader FastAPI Server Launcher
"""
import sys
import os
import uvicorn
from pathlib import Path

# Add Backend directory to Python path
backend_path = Path(__file__).parent / "Backend"
sys.path.insert(0, str(backend_path))

def main():
    """Launch the FastAPI server"""
    print("🚀 Starting Mon-Reader Server...")
    print("📁 Backend: http://localhost:8000")
    print("🌐 Frontend: Open Frontend/index.html in your browser")
    print("📚 API Docs: http://localhost:8000/docs")
    print("❌ Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Change to Backend directory
    os.chdir(backend_path)
    
    # Start the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(backend_path)]
    )

if __name__ == "__main__":
    main()