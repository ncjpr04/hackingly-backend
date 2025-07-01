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

try:
    linkedin_agent = LinkedInAgent()
except ChallengeException as e:
    print(f"LinkedIn login challenge required, you're screwed 💀: {str(e)}")
    linkedin_agent = None
except Exception as e:
    print(f"Failed to initialize LinkedInAgent: {str(e)}")
    import traceback
    traceback.print_exc()
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
            raise HTTPException(status_code=400, detail="LinkedIn login challenge required, you're screwed 💀 (please contact the maintainer if this issue persists).")
        profile_data = await linkedin_agent.get_ingest(profile_id)
        return profile_data
    except FetchException as e:
        print(f"FetchException occurred: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to fetch profile: {str(e)}")
    except ParseException as e:
        print(f"ParseException occurred: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to parse profile data: {str(e)}")
    except ChallengeException as e:
        print(f"ChallengeException occurred: {str(e)}")
        raise HTTPException(status_code=400, detail=f"LinkedIn authentication challenge: {str(e)}")
    except Exception as e:
        print(f"Unexpected error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/health")
async def health_check():
    if linkedin_agent is None:
        raise HTTPException(
            status_code=503, 
            detail="LinkedIn login challenge required."
        )
    return {"status": "ok"}

@app.get("/api/queue")
async def waiting_count():
    if linkedin_agent is None:
        raise HTTPException(
            status_code=503, 
            detail="LinkedIn login challenge required."
        )
    return linkedin_agent.get_queue_status()
