"""
Google Colab Runner Script for JNTU EduAssist AI

Instructions:
1. Upload this file along with app.py, courses.json, and knowledge_base.json to Colab
2. Run each cell in order

This script handles:
- Dependency installation
- Port tunneling with ngrok
- Launching the Streamlit app
"""

def setup_environment():
    """Install required dependencies."""
    import subprocess
    import sys
    
    dependencies = [
        "streamlit",
        "pyngrok",
    ]
    
    for dep in dependencies:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", dep])
    
    print("✅ Dependencies installed!")

def run_app():
    """Run the Streamlit app with ngrok tunnel."""
    import subprocess
    import time
    from pyngrok import ngrok
    
    ngrok.kill()
    
    process = subprocess.Popen(
        ["streamlit", "run", "app.py", "--server.port", "8501", "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(5)
    
    public_url = ngrok.connect(8501)
    print(f"\n🎓 JNTU EduAssist AI is running!")
    print(f"📱 Access your app at: {public_url}")
    print(f"\n⚠️ Keep this notebook running to keep the app alive.")
    
    return process

if __name__ == "__main__":
    print("=" * 50)
    print("JNTU EduAssist AI - Google Colab Setup")
    print("=" * 50)
    print("\nStep 1: Installing dependencies...")
    setup_environment()
    print("\nStep 2: Starting application...")
    process = run_app()
