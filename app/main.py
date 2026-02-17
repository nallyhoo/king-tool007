
from fastapi import FastAPI
from app.api.endpoints import processing_jobs

# Detailed description for the OpenAPI documentation
description = """
Welcome to the Video Manager API! 🚀

This API provides a powerful and flexible interface for downloading, processing, and managing video content.

## Key Features:

*   **Video Downloading**: Download videos from popular platforms using their URLs.
*   **Asynchronous Processing**: All video operations are handled asynchronously in the background, so your application remains responsive.
*   **Rich Processing Options**: A wide range of video processing capabilities, including:
    *   Thumbnail generation (single, strip, animated GIF)
    *   Format transcoding
    *   Resolution changes
    *   And much more!
*   **Secure**: Endpoints are protected using OAuth2 Bearer tokens.

## Getting Started:

1.  **Authenticate**: Obtain a token by providing your credentials to the `/token` endpoint.
2.  **Authorize**: Include the token in the `Authorization` header of your requests as a `Bearer` token.
3.  **Submit a Job**: Use the `/jobs` endpoint to submit a new video for processing.
4.  **Check Status**: Monitor the status of your job using the `/jobs/{job_id}` endpoint.
"""

app = FastAPI(
    title="Video Manager API",
    description=description,
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# Include the processing jobs router
app.include_router(processing_jobs.router, prefix="/jobs", tags=["Processing Jobs"])

# A simple root endpoint to confirm the API is running
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Video Manager API. Visit /docs for documentation."}

# In a real application, you would also have a /token endpoint
# For demonstration, we are using a hardcoded token check in the dependency
