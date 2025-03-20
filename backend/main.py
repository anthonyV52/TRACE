from fastapi import FastAPI
import uvicorn

# Import full FastAPI apps
from Project import app as project_app
from Credentials import app as credentials_app

# Create the main FastAPI app
app = FastAPI()

#  Mount Project and Credentials APIs
app.mount("/project", project_app)
app.mount("/credentials", credentials_app)

# Run the server
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
