from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_activities_include_required_clubs_and_sports():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()

    required_activities = {"Debate Club", "Robotics", "Soccer", "Art Club"}
    assert required_activities.issubset(set(data.keys()))

    for activity in required_activities:
        assert data[activity]["description"]
        assert data[activity]["schedule"]


def test_signup_endpoint_allows_student_joining_activity():
    email = "newstudent@mergington.edu"
    activity_name = "Debate Club"
    participants = activities[activity_name]["participants"]

    if email in participants:
        participants.remove(email)

    before_count = len(participants)
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert len(participants) == before_count + 1
    assert participants[-1] == email

    participants.remove(email)
