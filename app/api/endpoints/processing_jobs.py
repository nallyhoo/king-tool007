
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from typing import List

router = APIRouter()

# --- Authentication ---
# Defines the security scheme for authentication.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    A dependency that can be used to protect endpoints.
    In a real app, this would validate the token and return a user model.
    """
    if token != "fake-super-secret-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": "testuser"}

# --- Pydantic Models with Examples ---
class JobRequest(BaseModel):
    video_url: str = Field(..., example="https://www.youtube.com/watch?v=dQw4w9WgXcQ", description="URL of the video to be processed.")
    operations: List[str] = Field(..., example=["thumbnail", "transcode_720p"], description="List of processing operations to perform.")

class JobResponse(BaseModel):
    job_id: str = Field(..., example="abc-123-def-456", description="Unique identifier for the processing job.")
    status: str = Field(..., example="queued", description="Current status of the job.")
    message: str = Field(..., example="Job has been successfully queued for processing.")

# --- API Endpoints with Rich Documentation ---
@router.post(
    "/",
    response_model=JobResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit a new video processing job",
    description="Submit a URL to a video and a list of operations to perform. The job will be added to a queue for processing.",
    responses={
        202: {
            "description": "Job accepted for processing.",
            "content": {
                "application/json": {
                    "example": {"job_id": "abc-123-def-456", "status": "queued", "message": "Job has been successfully queued for processing."}
                }
            },
        },
        400: {"description": "Invalid video URL or operations specified."},
        401: {"description": "Unauthorized. A valid token is required."},
        422: {"description": "Validation Error. The request body is invalid."},
    },
)
async def create_processing_job(
    job_request: JobRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new video processing job:

    - **video_url**: The public URL of the video to process.
    - **operations**: A list of operations to run on the video.
      - `thumbnail`: Generate a thumbnail.
      - `transcode_720p`: Transcode to 720p resolution.
      - `extract_audio`: Extract the audio track.
    """
    job_id = "abc-123-def-456" # In a real app, this would be dynamically generated
    return {"job_id": job_id, "status": "queued", "message": "Job has been successfully queued for processing."}


@router.get(
    "/{job_id}",
    summary="Get job status",
    description="Retrieve the current status and details of a specific processing job.",
    responses={
        200: {"description": "Job status retrieved successfully."},
        401: {"description": "Unauthorized."},
        404: {"description": "Job not found."},
    }
)
async def get_job_status(job_id: str, current_user: dict = Depends(get_current_user)):
    """
    Retrieves the status of a given job.
    In a real implementation, you would look this up in your database.
    """
    return {"job_id": job_id, "status": "processing", "progress": 50}
