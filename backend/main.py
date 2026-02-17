from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import init_db
from backend.routes import auth, students, observations, schedule, materials, daily_entries, settings, chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Monty API",
    description="Backend API for the Monty Teacher Assistant",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(observations.router)
app.include_router(schedule.router)
app.include_router(materials.router)
app.include_router(daily_entries.router)
app.include_router(settings.router)
app.include_router(chat.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
