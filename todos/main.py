from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import uvicorn 

app = FastAPI()

studentsDB: Dict[int, dict] = {}


class Student(BaseModel):
    name: str
    age: int
    grade: str


@app.post("/students/", responseModel=Student)
def create_student(student: Student):
    studentId = len(studentsDB) + 1
    studentsDB[studentId] = student.dict()
    return student


@app.get("/students/")
def get_all_students():
    return studentsDB


@app.get("/students/{studentId}")
def getStudent(studentId: int):
    if studentId not in studentsDB:
        raise HTTPException(statusCode=404, detail="Student not found")
    return studentsDB[studentId]


@app.put("/students/{studentId}", responseModel=Student)
def updateStudent(studentId: int, student: Student):
    if studentId not in studentsDB:
        raise HTTPException(statusCode=404, detail="Student not found")
    studentsDB[studentId] = student.dict()
  
    return student


@app.delete("/students/{studentId}")
def deleteStudent(studentId: int):
    if studentId not in studentsDB:
        raise HTTPException(statusCode=404, detail="Student not found")
    del studentsDB[studentId]
    return {"message": "Student deleted successfully"}