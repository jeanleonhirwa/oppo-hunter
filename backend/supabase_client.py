import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")

def get_supabase() -> Client:
    if not url or not key:
        return None
    return create_client(url, key)

async def save_profile(session_id: str, profile: dict):
    supabase = get_supabase()
    if not supabase:
        print(f"MOCK: Saved profile for session {session_id}")
        return
        
    try:
        data = {
            "session_id": session_id,
            "full_name": profile.get("full_name"),
            "email": profile.get("email"),
            "phone": profile.get("phone"),
            "skills": profile.get("skills", []),
            "experience_years": int(profile.get("experience_years", 0)) if profile.get("experience_years") else None,
            "resume_text": profile.get("resume_text"),
            "job_preferences": profile.get("job_preferences"),
            "linkedin_url": profile.get("linkedin_url"),
            "portfolio_url": profile.get("portfolio_url")
        }
        supabase.table("user_profiles").insert(data).execute()
    except Exception as e:
        print(f"Error saving profile: {e}")

async def get_applications(session_id: str):
    supabase = get_supabase()
    if not supabase:
        # Return mock data if no supabase configured
        return [
            {"id": "1", "job_title": "Software Engineer", "company": "TechCorp", "platform": "JobInRwanda", "status": "applied", "job_url": "https://example.com/job1"},
            {"id": "2", "job_title": "Frontend Dev", "company": "Kigali Solutions", "platform": "BrighterMonday", "status": "applied", "job_url": "https://example.com/job2"},
            {"id": "3", "job_title": "Data Analyst", "company": "Bank of Kigali", "platform": "Rwanda Jobs", "status": "failed", "job_url": "https://example.com/job3"},
        ]
        
    try:
        response = supabase.table("applications").select("*").eq("session_id", session_id).order("applied_at", desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Error getting applications: {e}")
        return []

async def save_application(session_id: str, job_title: str, company: str, platform: str, job_url: str, status: str = "applied"):
    supabase = get_supabase()
    if not supabase:
        print(f"MOCK: Saved app {job_title} at {company}")
        return
        
    try:
        data = {
            "session_id": session_id,
            "job_title": job_title,
            "company": company,
            "platform": platform,
            "job_url": job_url,
            "status": status
        }
        supabase.table("applications").insert(data).execute()
    except Exception as e:
        print(f"Error saving application: {e}")
