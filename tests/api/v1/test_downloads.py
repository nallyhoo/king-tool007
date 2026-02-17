
import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.models.user import User
from app.schemas.download import DownloadStatus

# Note: This test file assumes you have a pytest setup with fixtures for:
# - an async test client (`client`)
# - an async database session (`db`)
# - a test user created in the database (`test_user`)
# - a way to get authentication headers for a user (`get_user_token_headers`)

# Placeholder for auth header utility
def get_user_token_headers(user: User) -> dict[str, str]:
    # In a real test suite, you would generate a JWT token for the user.
    # This is a simplified placeholder.
    return {"Authorization": f"Bearer fake-token-for-user-{user.id}"}

@pytest.mark.asyncio
async def test_initiate_download_success(client: AsyncClient, db: AsyncSession, test_user: User):
    """
    Test successful initiation of a YouTube download.
    """
    headers = get_user_token_headers(test_user)
    data = {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
    response = await client.post(f"{settings.API_V1_STR}/downloads/", headers=headers, json=data)
    
    assert response.status_code == status.HTTP_202_ACCEPTED
    content = response.json()
    assert content["url"] == data["url"]
    assert content["status"] == DownloadStatus.PENDING
    assert "id" in content

@pytest.mark.asyncio
async def test_initiate_download_unsupported_platform(client: AsyncClient, test_user: User):
    """
    Test initiating a download from an unsupported platform.
    """
    headers = get_user_token_headers(test_user)
    data = {"url": "https://www.an-unsupported-site.com/video"}
    response = await client.post(f"{settings.API_V1_STR}/downloads/", headers=headers, json=data)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio
async def test_list_downloads(client: AsyncClient, db: AsyncSession, test_user: User):
    """
    Test listing downloads for the current user.
    """
    # First, create a download to ensure there is data to list
    headers = get_user_token_headers(test_user)
    await client.post(f"{settings.API_V1_STR}/downloads/", headers=headers, json={"url": "https://www.vimeo.com/537925749"})

    response = await client.get(f"{settings.API_V1_STR}/downloads/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert "items" in content
    assert "total" in content
    assert content["total"] > 0
    assert len(content["items"]) > 0

@pytest.mark.asyncio
async def test_get_download_status(client: AsyncClient, db: AsyncSession, test_user: User):
    """
    Test getting the status of a specific download.
    """
    headers = get_user_token_headers(test_user)
    # Create a download
    create_response = await client.post(f"{settings.API_V1_STR}/downloads/", headers=headers, json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"})
    download_id = create_response.json()["id"]

    # Get status
    status_response = await client.get(f"{settings.API_V1_STR}/downloads/{download_id}/status", headers=headers)
    assert status_response.status_code == status.HTTP_200_OK
    content = status_response.json()
    assert content["id"] == download_id
    assert "status" in content
    assert "progress" in content

@pytest.mark.asyncio
async def test_get_nonexistent_download_status(client: AsyncClient, test_user: User):
    """
    Test getting the status of a download that does not exist.
    """
    headers = get_user_token_headers(test_user)
    response = await client.get(f"{settings.API_V1_STR}/downloads/99999/status", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

