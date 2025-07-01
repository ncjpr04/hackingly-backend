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

# Global variable to store initialization error
initialization_error = None

# Debug environment variables (without exposing sensitive data)
print("Environment check:")
print(f"LINKEDIN_AGENT_USERNAME set: {'Yes' if os.getenv('LINKEDIN_AGENT_USERNAME') else 'No'}")
print(f"LINKEDIN_AGENT_PASSWORD set: {'Yes' if os.getenv('LINKEDIN_AGENT_PASSWORD') else 'No'}")

try:
    linkedin_agent = LinkedInAgent()
except ChallengeException as e:
    error_msg = f"LinkedIn login challenge required: {str(e)}"
    print(f"LinkedIn login challenge required, you're screwed 💀: {str(e)}")
    print(f"ChallengeException details: {type(e).__name__}: {str(e)}")
    linkedin_agent = None
    initialization_error = error_msg
except Exception as e:
    error_msg = f"Failed to initialize LinkedInAgent: {str(e)}"
    print(f"Failed to initialize LinkedInAgent: {str(e)}")
    print(f"Exception type: {type(e).__name__}")
    print(f"Exception details: {str(e)}")
    import traceback
    traceback.print_exc()
    linkedin_agent = None
    initialization_error = error_msg

@app.get("/")
async def read_root():
    return {
        "message": "LinkedIngest API",
        "status": "running",
        "linkedin_agent_initialized": linkedin_agent is not None,
        "initialization_error": initialization_error,
        "endpoints": {
            "profile": "/api/profile/{profile_id}",
            "health": "/api/health", 
            "queue": "/api/queue",
            "startup_info": "/api/startup-info"
        },
        "docs": "/docs"
    }

@app.get("/api/startup-info")
async def startup_info():
    """Debug endpoint to check startup status and environment"""
    return {
        "linkedin_agent_initialized": linkedin_agent is not None,
        "initialization_error": initialization_error,
        "environment_variables": {
            "username_set": bool(os.getenv('LINKEDIN_AGENT_USERNAME')),
            "password_set": bool(os.getenv('LINKEDIN_AGENT_PASSWORD')),
        }
    }

@app.get("/api/profile/{profile_id}", response_model=ProfileResponse)
async def get_profile(profile_id: str):
    try:
        if linkedin_agent is None:
            if initialization_error:
                raise HTTPException(status_code=503, detail=f"LinkedIn service unavailable: {initialization_error}")
            else:
                raise HTTPException(status_code=503, detail="LinkedIn service not initialized")
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
        if initialization_error:
            raise HTTPException(
                status_code=503, 
                detail=f"LinkedIn service unavailable: {initialization_error}"
            )
        else:
            raise HTTPException(
                status_code=503, 
                detail="LinkedIn service not initialized"
            )
    return {"status": "ok"}

@app.get("/api/queue")
async def waiting_count():
    if linkedin_agent is None:
        if initialization_error:
            raise HTTPException(
                status_code=503, 
                detail=f"LinkedIn service unavailable: {initialization_error}"
            )
        else:
            raise HTTPException(
                status_code=503, 
                detail="LinkedIn service not initialized"
            )
    return linkedin_agent.get_queue_status()
