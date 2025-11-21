import requests

API_URL = "http://127.0.0.1:8000"

# ---------- Workspaces ----------
def get_workspaces():
    return requests.get(f"{API_URL}/workspaces/").json()

def create_workspace(name, description, color):
    payload = {
        "name": name,
        "description": description,
        "color": color
    }
    return requests.post(f"{API_URL}/workspaces/", json=payload).json()


# ---------- Tasks ----------
def get_tasks(workspace_id):
    return requests.get(f"{API_URL}/tasks/?workspace_id={workspace_id}").json()

def create_task(task):
    return requests.post(f"{API_URL}/tasks/", json=task).json()

def update_task(task_id, data):
    return requests.put(f"{API_URL}/tasks/{task_id}", json=data).json()


# ---------- Habits ----------
def get_habits(workspace_id):
    return requests.get(f"{API_URL}/habits/?workspace_id={workspace_id}").json()

def create_habit(habit):
    return requests.post(f"{API_URL}/habits/", json=habit).json()

def check_habit(habit_id):
    return requests.post(f"{API_URL}/habits/{habit_id}/check").json()


# ---------- Notes ----------
def get_notes(workspace_id):
    return requests.get(f"{API_URL}/notes/?workspace_id={workspace_id}").json()

def create_note(note):
    return requests.post(f"{API_URL}/notes/", json=note).json()

def update_note(note_id, note):
    return requests.put(f"{API_URL}/notes/{note_id}", json=note).json()


# ---------- Analytics ----------
def get_analytics():
    return requests.get(f"{API_URL}/analytics/").json()
