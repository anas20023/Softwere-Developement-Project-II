import requests
from settings import API_AUTH_URL

def register_user(name, student_Id, dept, intake, section, password):
    """Sends registration data to the backend."""
    url = f"{API_AUTH_URL}/register"
    data = {
        "name": name,
        "student_Id": student_Id,
        "dept": dept,
        "intake": int(intake),
        "section": int(section),
        "password": password
    }
    #print(data)
    try:
        response = requests.post(url, json=data)
        return response.json()  # Expected: { "success": true, "message": "User registered" }
    except requests.RequestException as e:
        return {"success": False, "message": f"Request failed: {e}"}

def login_user(student_id, password):
    """Sends login data to the backend."""
    url = f"{API_AUTH_URL}/login"
    data = {
        "studentId": student_id,
        "password": password
    }

    try:
        response = requests.post(url, json=data)
        return response.json()  # Expected: { "success": true, "token": "JWT_TOKEN", "user": { ... } }
    except requests.RequestException as e:
        return {"success": False, "message": f"Request failed: {e}"}
