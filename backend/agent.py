from browser_use import Agent, Browser, BrowserConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from supabase_client import save_application
from job_sites import JOB_SITES
import asyncio, os, json, re

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

async def run_job_agent(session_id: str, profile: dict):
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("Error: GEMINI_API_KEY not found.")
        return

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=api_key
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
       - Name: {profile.get('full_name')}
       - Email: {profile.get('email')}
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
        try:
            text = result.final_result()
        except:
            text = str(result)
    else:
        text = str(result)
    
    # Try to extract JSON from response
    match = re.search(r'\[.*\]', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass
    return []
