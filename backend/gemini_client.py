import google.generativeai as genai
import os, json
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))
model = genai.GenerativeModel("gemini-2.0-flash-exp")

async def extract_resume_info(resume_text: str) -> dict:
    prompt = f"""
    Extract key info from this resume. Return ONLY valid JSON with these fields:
    - full_name, email, phone, skills (array), experience_years (int),
      job_titles_sought (array), summary (2 sentences)

    Resume:
    {resume_text[:3000]}
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(text)
    except Exception as e:
        print(f"Error parsing resume via Gemini: {e}")
        return {"skills": []}

async def generate_cover_letter(profile: dict, job_title: str, company: str) -> str:
    prompt = f"""
    Write a short, professional cover letter (150 words max) for:
    - Candidate: {profile.get('full_name')}
    - Skills: {', '.join(profile.get('skills', []))}
    - Job: {job_title} at {company}
    Keep it compelling and personal.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return ""

async def should_apply_to_job(profile: dict, job_description: str) -> bool:
    prompt = f"""
    Skills: {profile.get('skills')}
    Experience: {profile.get('experience_years')} years
    Job description: {job_description[:500]}
    
    Should this person apply? Answer only YES or NO.
    """
    try:
        response = model.generate_content(prompt)
        return "YES" in response.text.upper()
    except Exception:
        return True
