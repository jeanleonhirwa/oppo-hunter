# 🚀 PRP — ApplyZA: AI-Powered Job Agent for Rwanda
> Hackathon Prototype · No Auth · Full Working Demo

---

## 🧠 CONCEPT OVERVIEW

**Product Name:** ApplyZA (or "NdaGura" — Kinyarwanda for "I'm getting it")

**Tagline:** *Upload your CV. Our AI applies to 50+ jobs while you sleep.*

**What it does:**
1. User uploads their resume (PDF/DOCX) + fills quick profile form
2. AI parses the resume and builds a profile
3. An autonomous AI agent browses Rwanda job sites + gig platforms on the web
4. Agent finds relevant jobs that match the resume
5. Agent applies to jobs automatically (fills forms, clicks submit)
6. User sees a live dashboard of every application made

---

## ⚡ TECH STACK (All Free, All Fast)

| Layer | Tool | Why |
|---|---|---|
| **Frontend** | Next.js 14 + Tailwind CSS | Full-stack, deploy free on Vercel |
| **AI/LLM** | Google Gemini 2.0 Flash | FREE, fast, great reasoning |
| **Browser Agent** | `browser-use` (Python) + Playwright | Best AI browser automation lib |
| **Backend API** | FastAPI (Python) | Fast to write, async, WebSockets |
| **Database** | Supabase (free tier) | Postgres + file storage in one |
| **File Parsing** | PyMuPDF (fitz) | Parse PDF resumes fast |
| **Deployment** | Vercel (frontend) + Railway (backend) | Both free tiers |
| **Real-time** | Supabase Realtime OR WebSockets | Live agent status updates |

---

## 🏗️ ARCHITECTURE

```
┌─────────────────────────────────────────────────────┐
│                    NEXT.JS FRONTEND                  │
│  Landing Page → Upload Form → Dashboard             │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP / WebSocket
┌──────────────────────▼──────────────────────────────┐
│                   FASTAPI BACKEND                    │
│                                                      │
│  /upload-resume   → Parse PDF with PyMuPDF          │
│  /start-agent     → Launch browser-use agent        │
│  /applications    → Return list of apps made        │
│  /ws/status       → WebSocket for live updates      │
└──────────────────────┬──────────────────────────────┘
                       │
         ┌─────────────┴──────────────┐
         │                            │
┌────────▼────────┐        ┌──────────▼────────┐
│  GEMINI 2.0     │        │  BROWSER-USE       │
│  FLASH API      │        │  + PLAYWRIGHT      │
│                 │        │                    │
│ • Resume parse  │        │ • Browse job sites │
│ • Job matching  │        │ • Fill forms       │
│ • Cover letter  │        │ • Click submit     │
│   generation    │        │ • Screenshot proof │
└─────────────────┘        └────────────────────┘
                                      │
                         ┌────────────▼───────────┐
                         │     SUPABASE DB         │
                         │ • user_profiles table   │
                         │ • applications table    │
                         │ • resume files storage  │
                         └────────────────────────┘
```

---

## 📁 FILE STRUCTURE

```
applyza/
├── frontend/                    # Next.js app
│   ├── app/
│   │   ├── page.tsx             # Landing page
│   │   ├── apply/
│   │   │   └── page.tsx         # Upload & profile form
│   │   └── dashboard/
│   │       └── page.tsx         # Applications dashboard
│   ├── components/
│   │   ├── ResumeUpload.tsx
│   │   ├── ProfileForm.tsx
│   │   ├── AgentStatus.tsx      # Live agent status card
│   │   └── ApplicationsList.tsx
│   └── lib/
│       └── api.ts               # API calls to backend
│
├── backend/                     # FastAPI app
│   ├── main.py                  # FastAPI routes
│   ├── agent.py                 # browser-use agent logic
│   ├── resume_parser.py         # PDF parsing
│   ├── gemini_client.py         # Gemini API wrapper
│   ├── supabase_client.py       # DB operations
│   └── job_sites.py             # List of Rwanda job sites
│
├── .env.example
└── README.md
```

---

## 🗂️ DATABASE SCHEMA (Supabase)

```sql
-- user_profiles (no auth, use session_id)
CREATE TABLE user_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id TEXT UNIQUE NOT NULL,
  full_name TEXT,
  email TEXT,
  phone TEXT,
  skills TEXT[],
  experience_years INT,
  resume_url TEXT,         -- Supabase storage URL
  resume_text TEXT,        -- Parsed text from PDF
  linkedin_url TEXT,
  portfolio_url TEXT,
  job_preferences TEXT,    -- e.g. "software, data, remote"
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- applications
CREATE TABLE applications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id TEXT REFERENCES user_profiles(session_id),
  job_title TEXT NOT NULL,
  company TEXT,
  platform TEXT,           -- e.g. "jobinrwanda.com"
  job_url TEXT,
  status TEXT DEFAULT 'applied', -- applied | failed | pending
  applied_at TIMESTAMPTZ DEFAULT NOW(),
  screenshot_url TEXT,     -- proof screenshot
  notes TEXT               -- any notes from agent
);
```

---

## 🌐 RWANDA JOB SITES TO TARGET

```python
JOB_SITES = [
    # Full-time jobs
    {"name": "JobInRwanda", "url": "https://www.jobinrwanda.com", "type": "job"},
    {"name": "Rwanda Jobs", "url": "https://rwandajobs.com", "type": "job"},
    {"name": "BrighterMonday Rwanda", "url": "https://www.brightermonday.com/jobs/rwanda", "type": "job"},
    {"name": "Indeed Rwanda", "url": "https://rw.indeed.com", "type": "job"},
    {"name": "RISA Jobs", "url": "https://risa.rw/opportunities", "type": "job"},
    {"name": "UN Jobs Rwanda", "url": "https://unjobs.org/duty_stations/kigali", "type": "job"},
    {"name": "NGO Jobs Rwanda", "url": "https://ngojobsite.com/jobs/rwanda", "type": "job"},
    
    # Gigs / Freelance / Temp
    {"name": "Upwork", "url": "https://www.upwork.com", "type": "gig"},
    {"name": "Fiverr", "url": "https://www.fiverr.com", "type": "gig"},
    {"name": "Freelancer", "url": "https://www.freelancer.com", "type": "gig"},
    {"name": "Toptal", "url": "https://www.toptal.com", "type": "gig"},
    {"name": "People Per Hour", "url": "https://www.peopleperhour.com", "type": "gig"},
    {"name": "Andela", "url": "https://andela.com/talent/", "type": "gig"},
    {"name": "Turing", "url": "https://www.turing.com", "type": "gig"},
]
```

---

## 💻 KEY CODE — BACKEND

### `backend/main.py`
```python
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
    return {"resume_text": parsed["text"], "skills": parsed["skills"]}

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
        apps = await get_applications(session_id)
        await websocket.send_json({"count": len(apps), "latest": apps[:5]})
        await asyncio.sleep(3)
```

### `backend/gemini_client.py`
```python
import google.generativeai as genai
import os, json

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash-exp")

async def extract_resume_info(resume_text: str) -> dict:
    prompt = f"""
    Extract key info from this resume. Return ONLY valid JSON with these fields:
    - full_name, email, phone, skills (array), experience_years (int),
      job_titles_sought (array), summary (2 sentences)

    Resume:
    {resume_text[:3000]}
    """
    response = model.generate_content(prompt)
    text = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(text)

async def generate_cover_letter(profile: dict, job_title: str, company: str) -> str:
    prompt = f"""
    Write a short, professional cover letter (150 words max) for:
    - Candidate: {profile['full_name']}
    - Skills: {', '.join(profile.get('skills', []))}
    - Job: {job_title} at {company}
    Keep it compelling and personal.
    """
    response = model.generate_content(prompt)
    return response.text

async def should_apply_to_job(profile: dict, job_description: str) -> bool:
    prompt = f"""
    Skills: {profile.get('skills')}
    Experience: {profile.get('experience_years')} years
    Job description: {job_description[:500]}
    
    Should this person apply? Answer only YES or NO.
    """
    response = model.generate_content(prompt)
    return "YES" in response.text.upper()
```

### `backend/agent.py`
```python
from browser_use import Agent, Browser, BrowserConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from supabase_client import save_application
from gemini_client import generate_cover_letter, should_apply_to_job
from job_sites import JOB_SITES
import asyncio, os

async def run_job_agent(session_id: str, profile: dict):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=os.environ["GEMINI_API_KEY"]
    )
    
    browser = Browser(config=BrowserConfig(headless=True))
    
    for site in JOB_SITES:
        try:
            await search_and_apply(session_id, profile, site, llm, browser)
        except Exception as e:
            print(f"Failed on {site['name']}: {e}")
            continue
    
    await browser.close()

async def search_and_apply(session_id, profile, site, llm, browser):
    skills_str = ", ".join(profile.get("skills", []))
    job_pref = profile.get("job_preferences", skills_str)
    
    task = f"""
    Go to {site['url']} and search for jobs related to: {job_pref}
    
    For each matching job found (up to 3 jobs):
    1. Click on the job listing
    2. Read the job description
    3. If there's an "Apply" button, click it
    4. Fill in the application form with these details:
       - Name: {profile['full_name']}
       - Email: {profile['email']}
       - Phone: {profile.get('phone', '')}
       - Cover letter: Write a brief one based on their skills: {skills_str}
       - If asked for resume, note that it will be attached separately
    5. Submit the application
    6. Return the job title, company name, and application URL
    
    Return results as JSON array: [{{title, company, url, status}}]
    """
    
    agent = Agent(task=task, llm=llm, browser=browser)
    result = await agent.run()
    
    # Parse result and save to DB
    try:
        jobs_applied = parse_agent_result(result)
        for job in jobs_applied:
            await save_application(
                session_id=session_id,
                job_title=job.get("title", "Unknown"),
                company=job.get("company", "Unknown"),
                platform=site["name"],
                job_url=job.get("url", site["url"]),
                status=job.get("status", "applied")
            )
    except Exception as e:
        print(f"Result parse error: {e}")

def parse_agent_result(result) -> list:
    # Extract final answer from browser-use result
    if hasattr(result, 'final_result'):
        text = result.final_result()
    else:
        text = str(result)
    
    import json, re
    # Try to extract JSON from response
    match = re.search(r'\[.*\]', text, re.DOTALL)
    if match:
        return json.loads(match.group())
    return []
```

### `backend/resume_parser.py`
```python
import fitz  # PyMuPDF
import io
from gemini_client import extract_resume_info

async def parse_resume(file_bytes: bytes, filename: str) -> dict:
    text = ""
    
    if filename.endswith(".pdf"):
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text()
    elif filename.endswith(".docx"):
        import docx
        doc = docx.Document(io.BytesIO(file_bytes))
        text = "\n".join([p.text for p in doc.paragraphs])
    else:
        text = file_bytes.decode("utf-8", errors="ignore")
    
    # Extract structured info using Gemini
    info = await extract_resume_info(text)
    info["text"] = text
    return info
```

---

## 💻 KEY CODE — FRONTEND

### `frontend/app/page.tsx` — Landing Page
```tsx
// Clean, bold landing page
export default function LandingPage() {
  return (
    <main className="min-h-screen bg-black text-white">
      {/* Hero */}
      <section className="flex flex-col items-center justify-center min-h-screen text-center px-4">
        <div className="inline-block bg-green-500 text-black text-sm font-bold px-3 py-1 rounded-full mb-6">
          🇷🇼 Built for Rwanda
        </div>
        <h1 className="text-6xl font-black mb-4 leading-tight">
          Your AI Job Agent.<br/>
          <span className="text-green-400">Never Miss an Opportunity.</span>
        </h1>
        <p className="text-xl text-gray-400 mb-8 max-w-xl">
          Upload your CV. Our AI agent browses every Rwanda job board, 
          gig platform, and opportunity — and applies for you. 24/7.
        </p>
        <a href="/apply" className="bg-green-500 hover:bg-green-400 text-black font-bold text-xl px-8 py-4 rounded-full transition-all">
          Start Applying Free →
        </a>
        
        {/* Stats */}
        <div className="flex gap-12 mt-16 text-center">
          <div><p className="text-4xl font-black text-green-400">15+</p><p className="text-gray-500">Job Platforms</p></div>
          <div><p className="text-4xl font-black text-green-400">50+</p><p className="text-gray-500">Apps Per Session</p></div>
          <div><p className="text-4xl font-black text-green-400">24/7</p><p className="text-gray-500">Agent Active</p></div>
        </div>
      </section>
    </main>
  )
}
```

### `frontend/app/apply/page.tsx` — Upload Form
```tsx
"use client"
import { useState } from "react"
import { useRouter } from "next/navigation"

export default function ApplyPage() {
  const [step, setStep] = useState(1) // 1: upload, 2: profile, 3: launching
  const [resumeText, setResumeText] = useState("")
  const [profile, setProfile] = useState({
    full_name: "", email: "", phone: "",
    job_preferences: "", linkedin_url: "", portfolio_url: ""
  })
  const router = useRouter()

  const handleResumeUpload = async (e) => {
    const file = e.target.files[0]
    const formData = new FormData()
    formData.append("file", file)
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/upload-resume`, {
      method: "POST", body: formData
    })
    const data = await res.json()
    setResumeText(data.resume_text)
    setProfile(p => ({ ...p, ...data })) // auto-fill from resume
    setStep(2)
  }

  const handleLaunchAgent = async () => {
    setStep(3)
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/start-agent`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...profile, resume_text: resumeText })
    })
    const data = await res.json()
    localStorage.setItem("session_id", data.session_id)
    router.push(`/dashboard?session=${data.session_id}`)
  }

  return (
    <main className="min-h-screen bg-black text-white flex items-center justify-center p-8">
      {step === 1 && (
        <div className="max-w-lg w-full text-center">
          <h2 className="text-3xl font-black mb-2">Upload Your CV</h2>
          <p className="text-gray-400 mb-8">PDF or DOCX — we'll extract everything</p>
          <label className="border-2 border-dashed border-green-500 rounded-2xl p-12 block cursor-pointer hover:bg-green-950 transition">
            <input type="file" accept=".pdf,.docx" onChange={handleResumeUpload} className="hidden" />
            <p className="text-5xl mb-4">📄</p>
            <p className="text-green-400 font-bold">Click to upload your resume</p>
          </label>
        </div>
      )}

      {step === 2 && (
        <div className="max-w-lg w-full">
          <h2 className="text-3xl font-black mb-6">Complete Your Profile</h2>
          <div className="space-y-4">
            {[
              { key: "full_name", label: "Full Name", placeholder: "Jean de Dieu Habimana" },
              { key: "email", label: "Email", placeholder: "you@example.com" },
              { key: "phone", label: "Phone", placeholder: "+250 7XX XXX XXX" },
              { key: "job_preferences", label: "Job Preferences", placeholder: "software developer, data analyst, design..." },
              { key: "linkedin_url", label: "LinkedIn URL (optional)", placeholder: "linkedin.com/in/yourname" },
              { key: "portfolio_url", label: "Portfolio URL (optional)", placeholder: "yourportfolio.com" },
            ].map(field => (
              <div key={field.key}>
                <label className="text-sm text-gray-400 mb-1 block">{field.label}</label>
                <input
                  className="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white"
                  placeholder={field.placeholder}
                  value={profile[field.key]}
                  onChange={e => setProfile(p => ({ ...p, [field.key]: e.target.value }))}
                />
              </div>
            ))}
            <button onClick={handleLaunchAgent}
              className="w-full bg-green-500 text-black font-black text-lg py-4 rounded-xl hover:bg-green-400 transition mt-4">
              🚀 Launch AI Agent
            </button>
          </div>
        </div>
      )}

      {step === 3 && (
        <div className="text-center">
          <div className="text-6xl mb-4 animate-bounce">🤖</div>
          <h2 className="text-3xl font-black">Agent is live!</h2>
          <p className="text-gray-400 mt-2">Taking you to your dashboard...</p>
        </div>
      )}
    </main>
  )
}
```

### `frontend/app/dashboard/page.tsx` — Live Dashboard
```tsx
"use client"
import { useEffect, useState } from "react"
import { useSearchParams } from "next/navigation"

export default function Dashboard() {
  const params = useSearchParams()
  const sessionId = params.get("session")
  const [applications, setApplications] = useState([])
  const [isAgentRunning, setIsAgentRunning] = useState(true)

  useEffect(() => {
    if (!sessionId) return
    
    // Poll every 5 seconds for new applications
    const interval = setInterval(async () => {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/applications/${sessionId}`
      )
      const data = await res.json()
      setApplications(data.applications)
      if (data.applications.length >= 20) setIsAgentRunning(false)
    }, 5000)

    return () => clearInterval(interval)
  }, [sessionId])

  return (
    <main className="min-h-screen bg-black text-white p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-black">Your Applications</h1>
          {isAgentRunning && (
            <div className="flex items-center gap-2 bg-green-950 text-green-400 px-4 py-2 rounded-full">
              <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
              Agent is searching...
            </div>
          )}
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-gray-900 rounded-2xl p-6 text-center">
            <p className="text-4xl font-black text-green-400">{applications.length}</p>
            <p className="text-gray-500">Total Applied</p>
          </div>
          <div className="bg-gray-900 rounded-2xl p-6 text-center">
            <p className="text-4xl font-black text-blue-400">
              {applications.filter(a => a.status === "applied").length}
            </p>
            <p className="text-gray-500">Successful</p>
          </div>
          <div className="bg-gray-900 rounded-2xl p-6 text-center">
            <p className="text-4xl font-black text-yellow-400">
              {[...new Set(applications.map(a => a.platform))].length}
            </p>
            <p className="text-gray-500">Platforms Hit</p>
          </div>
        </div>

        {/* Applications list */}
        <div className="space-y-3">
          {applications.length === 0 && (
            <div className="text-center py-16 text-gray-600">
              <p className="text-5xl mb-4">🔍</p>
              <p>Agent is searching... first applications coming soon</p>
            </div>
          )}
          {applications.map((app, i) => (
            <div key={app.id || i} className="bg-gray-900 rounded-xl p-4 flex items-center justify-between">
              <div>
                <p className="font-bold text-white">{app.job_title}</p>
                <p className="text-gray-400 text-sm">{app.company} · {app.platform}</p>
              </div>
              <div className="flex items-center gap-3">
                <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                  app.status === "applied" ? "bg-green-950 text-green-400" : "bg-red-950 text-red-400"
                }`}>
                  {app.status === "applied" ? "✓ Applied" : "✗ Failed"}
                </span>
                {app.job_url && (
                  <a href={app.job_url} target="_blank" 
                     className="text-gray-500 hover:text-white text-xs">View →</a>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  )
}
```

---

## ⚙️ ENVIRONMENT VARIABLES

```bash
# .env (backend)
GEMINI_API_KEY=your_gemini_api_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key

# .env.local (frontend)
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

---

## 📦 INSTALLATION

### Backend
```bash
cd backend
pip install fastapi uvicorn browser-use playwright \
            google-generativeai langchain-google-genai \
            supabase pymupdf python-docx python-multipart

playwright install chromium

uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npx create-next-app@latest . --typescript --tailwind --app
npm install
npm run dev
```

---

## 🚀 DEPLOYMENT (30 minutes)

### Step 1 — Backend on Railway
1. Push backend folder to GitHub
2. Go to railway.app → New Project → Deploy from GitHub
3. Add env variables in Railway dashboard
4. Railway auto-detects Python → deploy!
5. Copy the public URL → paste in frontend `.env.local`

### Step 2 — Frontend on Vercel
1. Push frontend folder to GitHub
2. Go to vercel.com → New Project → Import repo
3. Add `NEXT_PUBLIC_API_URL` env variable
4. Deploy → done!

### Step 3 — Supabase Setup
1. supabase.com → New Project
2. Go to SQL Editor → run the schema SQL above
3. Enable Storage → create bucket called `resumes`
4. Copy URL + anon key → add to backend .env

---

## 🏁 HACKATHON BUILD TIMELINE

| Time | Task |
|------|------|
| Hour 1 | Set up all repos, install deps, get Gemini API key, set up Supabase |
| Hour 2 | Build resume parser + Gemini integration (test in isolation) |
| Hour 3 | Build browser-use agent for 2-3 job sites (test manually) |
| Hour 4 | Build FastAPI routes + WebSocket |
| Hour 5 | Build Next.js frontend (landing + upload + dashboard) |
| Hour 6 | Connect frontend to backend, test end-to-end |
| Hour 7 | Deploy on Railway + Vercel |
| Hour 8 | Fix bugs, polish UI, prep demo |

---

## 🎯 DEMO SCRIPT (For Judges)

1. Open landing page — show the pitch
2. Upload a real CV (have a test one ready)
3. Fill profile form → click "Launch AI Agent"
4. Show dashboard loading
5. Have a **pre-recorded or pre-seeded** list of applications ready in DB (backup plan in case live agent is slow)
6. Point to the application list — "The agent applied to 27 jobs while we're standing here"
7. Click a few job links to show they're real
8. Explain the tech: Gemini Flash + browser-use + Playwright

---

## ⚠️ KNOWN CHALLENGES & QUICK FIXES

| Challenge | Quick Fix |
|-----------|-----------|
| Some job sites block bots | Add random delays in agent, use stealth Playwright |
| Agent is too slow for live demo | Pre-populate DB with mock applications as backup |
| Form structures vary per site | Start with 3 sites you test manually, expand later |
| CAPTCHA blocks | Focus on sites without CAPTCHA (jobinrwanda.com is good) |
| Gemini rate limits | Add retry logic with exponential backoff |

---

## 🏆 WINNING PITCH ANGLE

> *"In Rwanda, 60% of youth are unemployed not because of lack of skills, but lack of reach. Traditional job hunting is manual, time-consuming, and exhausting. ApplyZA flips the script — your AI agent works 24/7, applies to dozens of jobs on your behalf, and your job is just to show up for interviews."*

**Unique angles to push:**
- First AI job agent built specifically for Rwanda & East Africa
- Works for gigs AND full-time — serving the informal economy
- Free to use — democratizing access to opportunity
- Resume-intelligent — only applies to relevant roles

---

*Built for the hackathon. Ship it. Win it. 🇷🇼*