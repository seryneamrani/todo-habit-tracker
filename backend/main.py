from fastapi import FastAPI
from routers import tasks, habits, workspaces, notes, analytics

app = FastAPI()

app.include_router(tasks.router)
app.include_router(habits.router)
app.include_router(workspaces.router)
app.include_router(notes.router)
app.include_router(analytics.router)




@app.get("/")
def root():
    return {"message": "Backend API is running"}
