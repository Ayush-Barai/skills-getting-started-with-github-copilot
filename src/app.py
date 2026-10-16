"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Debate Club": {
        "description": "Build public speaking and critical thinking through team debates.",
        "schedule": "Monday, 3:30 PM - 4:45 PM",
        "max_participants": 24,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Robotics": {
        "description": "Design, code, and test robots for regional competitions.",
        "schedule": "Tuesday, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Soccer": {
        "description": "Develop teamwork and skills with practices and scrimmages.",
        "schedule": "Wednesday, 3:45 PM - 5:15 PM",
        "max_participants": 28,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore painting, sketching, and mixed-media creative projects.",
        "schedule": "Thursday, 3:30 PM - 4:45 PM",
        "max_participants": 18,
        "participants": ["ava@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
