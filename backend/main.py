from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Project import router as project_router  # ✅ we're importing the router now

app = FastAPI()

# CORS middleware for local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include the project router with a prefix
app.include_router(project_router, prefix="/project")

@app.get("/")
def root():
    return {"message": "Main FastAPI app is live!"}

# Optional, only needed if you want to run with `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
