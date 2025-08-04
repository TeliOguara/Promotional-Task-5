from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import json
import os

app = FastAPI()

# Path to data file
DATA_FILE = "students.json"

# ----------------------------

class Student(BaseModel):
    name: str
    subject_scores: Dict[str, float]


def load_students():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_students(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def calculate_average(scores: Dict[str, float]) -> float:
    return round(sum(scores.values()) / len(scores), 2)

def calculate_grade(avg: float) -> str:
    if avg >= 70:
        return "A"
    elif avg >= 60:
        return "B"
    elif avg >= 50:
        return "C"
    elif avg >= 40:
        return "D"
    else:
        return "F"


@app.post("/students/")
def add_student(student: Student):
    try:
        students = load_students()
        avg = calculate_average(student.subject_scores)
        grade = calculate_grade(avg)
        new_student = {
            "name": student.name,
            "subject_scores": student.subject_scores,
            "average": avg,
            "grade": grade
        }
        students.append(new_student)
        save_students(students)
        return {"message": "Student added", "student": new_student}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/students/{name}")
def get_student(name: str):
    try:
        students = load_students()
        for s in students:
            if s["name"].lower() == name.lower():
                return s
        raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/students/")
def get_all_students():
    try:
        return load_students()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
