import sys
from pathlib import Path
import uvicorn

# Add the backend directory to sys.path so the 'app' module can be imported
backend_path = Path(__file__).parent / "backend"
sys.path.append(str(backend_path))

if __name__ == "__main__":
    # Run the FastAPI app using uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
