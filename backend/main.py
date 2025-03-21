from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Project import app as project_app  # ✅ lowercase if your file is named project.py

app = FastAPI()

# ✅ Enable CORS for the entire FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for testing only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Mount the project app at /project
app.mount("/project", project_app)

# ✅ Optional root route to confirm API is running
@app.get("/")
def root():
    return {"message": "Main FastAPI app is live!"}

# ✅ Only runs if you execute this file directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
