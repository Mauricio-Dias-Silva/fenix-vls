
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Fenix VLS UI")

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open(os.path.join(_BASE_DIR, "dashboard.html"), "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
