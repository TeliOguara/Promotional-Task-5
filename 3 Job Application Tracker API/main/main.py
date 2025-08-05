from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from file_handler import load_applications, save_applications


app = FastAPI()

class JobApplication(BaseModel):
    name: str
    company: str
    position: str
    status: str

@app.post("/applications/")
def add_application(app_data: JobApplication):
    try:
        apps = load_applications()
        apps.append(app_data.model_dump())
        save_applications(apps)
        return {"message": "Application saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/applications/")
def get_all_applications():
    try:
        return load_applications()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/applications/search")
def search_by_status(status: str):
    try:
        apps = load_applications()
        filtered = [a for a in apps if a["status"].lower() == status.lower()]
        if not filtered:
            raise HTTPException(status_code=404, detail="No applications with this status")
        return filtered
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
