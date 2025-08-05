from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

NOTES = "notes"

class Note(BaseModel):
    content: str

# -----------------------------
@app.post("/notes/")
def create_note(title: str, note: Note):
    try:
        filepath = os.path.join(NOTES, f"{title}.txt")
        if os.path.exists(filepath):
            raise HTTPException(status_code=400, detail="Note already exists")
        with open(filepath, "w") as f:
            f.write(note.content)
        return {"message": "Note created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/notes/{title}")
def read_note(title: str):
    try:
        filepath = os.path.join(NOTES, f"{title}.txt")
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Note not found")
        with open(filepath, "r") as f:
            content = f.read()
        return {"title": title, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/notes/{title}")
def update_note(title: str, note: Note):
    try:
        filepath = os.path.join(NOTES, f"{title}.txt")
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Note not found")
        with open(filepath, "w") as f:
            f.write(note.content)
        return {"message": "Note updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/notes/{title}/delete")
def delete_note(title: str):
    try:
        filepath = os.path.join(NOTES, f"{title}.txt")
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Note not found")
        os.remove(filepath)
        return {"message": "Note deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
