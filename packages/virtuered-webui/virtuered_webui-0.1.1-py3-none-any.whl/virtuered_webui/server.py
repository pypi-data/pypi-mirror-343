from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import os

app = FastAPI()

FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "frontend")

# Static files serving (JS, CSS, images)
app.mount("/_next", StaticFiles(directory=os.path.join(FRONTEND_PATH, "_next")), name="_next")
app.mount("/images", StaticFiles(directory=os.path.join(FRONTEND_PATH, "images")), name="images")

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    file_path = os.path.join(FRONTEND_PATH, full_path)

    if os.path.isfile(file_path):
        return FileResponse(file_path)

    # Fallback for any path: serve index.html with injected API_URL
    index_path = os.path.join(FRONTEND_PATH, "index.html")
    api_url = os.environ.get("API_URL", "http://localhost:4401")
    
    with open(index_path, "r") as file:
        html = file.read().replace(
            "<head>",
            f"<head><script>window.__NEXT_PUBLIC_API_URL__ = '{api_url}';</script>",
        )
    return HTMLResponse(html)
