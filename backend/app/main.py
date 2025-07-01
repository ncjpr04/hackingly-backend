from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .api.linkedin import LinkedInAgent, FetchException, ParseException
from .api.linkedin import ChallengeException
from .models.profile import ProfileResponse
import os

app = FastAPI(title="LinkedIngest API", description="LinkedIn profile data API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check if LinkedIn credentials are available
linkedin_username = os.getenv("nitinchoudhary22112004@gmail.com")
linkedin_password = os.getenv("sumitra@1984")

if linkedin_username and linkedin_password:
    try:
        linkedin_agent = LinkedInAgent()
    except ChallengeException as e:
        print("LinkedIn login challenge required, you're screwed 💀")
        linkedin_agent = None
    except Exception as e:
        print(f"Failed to initialize LinkedInAgent: {e}")
        linkedin_agent = None
else:
    print("LinkedIn credentials not provided. Set LINKEDIN_AGENT_USERNAME and LINKEDIN_AGENT_PASSWORD environment variables.")
    linkedin_agent = None

@app.get("/")
async def read_root():
    return {
        "message": "LinkedIngest API",
        "endpoints": {
            "profile": "/api/profile/{profile_id}",
            "health": "/api/health", 
            "queue": "/api/queue"
        },
        "docs": "/docs"
    }

@app.get("/api/profile/{profile_id}", response_model=ProfileResponse)
async def get_profile(profile_id: str):
    try:
        if linkedin_agent is None:
            raise HTTPException(status_code=503, detail="LinkedIn service unavailable. Please ensure LINKEDIN_AGENT_USERNAME and LINKEDIN_AGENT_PASSWORD environment variables are set.")
        profile_data = await linkedin_agent.get_ingest(profile_id)
        return profile_data
    except FetchException:
        raise HTTPException(status_code=400, detail="Failed to fetch profile")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    if linkedin_agent is None:
        raise HTTPException(
            status_code=503, 
            detail="LinkedIn service unavailable. Please ensure LinkedIn credentials are configured."
        )
    return {"status": "ok"}

@app.get("/api/queue")
async def waiting_count():
    if linkedin_agent is None:
        raise HTTPException(
            status_code=503, 
            detail="LinkedIn service unavailable. Please ensure LinkedIn credentials are configured."
        )
    return linkedin_agent.get_queue_status()
