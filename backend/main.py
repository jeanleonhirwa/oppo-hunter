from fastapi import FastAPI, UploadFile, File, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio, uuid
from resume_parser import parse_resume
from agent import run_job_agent
from supabase_client import save_profile, get_applications

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()
    parsed = await parse_resume(content, file.filename)
    return {"resume_text": parsed.get("text", ""), "skills": parsed.get("skills", [])}

@app.post("/api/start-agent")
async def start_agent(profile: dict):
    session_id = str(uuid.uuid4())
    await save_profile(session_id, profile)
    # Run agent in background
    asyncio.create_task(run_job_agent(session_id, profile))
    return {"session_id": session_id, "status": "agent_started"}

@app.get("/api/applications/{session_id}")
async def get_apps(session_id: str):
    apps = await get_applications(session_id)
    return {"applications": apps}

@app.websocket("/ws/{session_id}")
async def websocket_status(websocket: WebSocket, session_id: str):
    await websocket.accept()
    # Stream live updates from agent
    while True:
        try:
            apps = await get_applications(session_id)
            if apps:
                await websocket.send_json({"count": len(apps), "latest": apps[:5]})
            await asyncio.sleep(3)
        except Exception:
            break
