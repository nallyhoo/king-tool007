
# Video Manager API - Developer Guide

Welcome to the developer guide for the Video Manager API! This guide will walk you through everything you need to know to start integrating our powerful video processing services into your application.

## 1. Getting Started

Before you can make any calls to the API, you need to obtain an access token. Our API uses OAuth2 Bearer tokens for authentication.

**API Base URL**: `https://api.yourvideomanager.com/v1`

### 1.1 Authentication Flow

1.  **Request a Token**: Send a `POST` request to the `/token` endpoint with your client ID and secret.

    ```bash
    curl -X POST \
      https://api.yourvideomanager.com/v1/token \
      -H 'Content-Type: application/x-www-form-urlencoded' \
      -d 'grant_type=client_credentials&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET'
    ```

2.  **Receive Your Token**: The API will return an access token that is valid for one hour.

    ```json
    {
      "access_token": "your-super-secret-token",
      "token_type": "bearer"
    }
    ```

3.  **Authorize Your Requests**: Include this token in the `Authorization` header of all subsequent requests.

    ```bash
    -H 'Authorization: Bearer your-super-secret-token'
    ```

## 2. Common Use Cases

Here are some examples of how to interact with the API for common tasks.

### 2.1 Submit a Video for Processing

This is the primary way to add a new video to the system. You provide a video URL and a list of operations to perform.

**Endpoint**: `POST /jobs`

**Python Example**

```python
import requests

api_url = "https://api.yourvideomanager.com/v1/jobs"
headers = {"Authorization": "Bearer your-super-secret-token"}

data = {
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "operations": ["thumbnail", "transcode_720p"]
}

response = requests.post(api_url, headers=headers, json=data)

if response.status_code == 202:
    job = response.json()
    print(f"Successfully submitted job: {job['job_id']}")
else:
    print(f"Error: {response.text}")
```

**JavaScript (fetch) Example**

```javascript
const apiUrl = 'https://api.yourvideomanager.com/v1/jobs';
const headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer your-super-secret-token'
};

const body = JSON.stringify({
  video_url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
  operations: ['thumbnail', 'transcode_720p']
});

fetch(apiUrl, { method: 'POST', headers, body })
  .then(response => response.json())
  .then(data => {
    console.log('Job submitted:', data.job_id);
  })
  .catch(error => {
    console.error('Error submitting job:', error);
  });
```

### 2.2 Check Job Status

Once a job is submitted, you can poll this endpoint to check its progress.

**Endpoint**: `GET /jobs/{job_id}`

**cURL Example**

```bash
curl -X GET \
  https://api.yourvideomanager.com/v1/jobs/abc-123-def-456 \
  -H 'Authorization: Bearer your-super-secret-token'
```

## 3. WebSocket Notifications

For real-time updates on job status, you can connect to our WebSocket server.

**Connection URL**: `wss://ws.yourvideomanager.com/v1/ws?token=your-super-secret-token`

### 3.1 Event Types & Payloads

-   **`job:queued`**: When a job is first accepted.
-   **`job:processing`**: When processing begins.
-   **`job:completed`**: When all operations are finished successfully.
-   **`job:failed`**: If an error occurs during processing.

**Example JavaScript Client**

```javascript
const socket = new WebSocket('wss://ws.yourvideomanager.com/v1/ws?token=your-super-secret-token');

socket.onopen = () => {
  console.log('WebSocket connection established.');
};

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received message:', data);

  // Example: update UI based on job status
  if (data.event === 'job:completed') {
    // Unlock video, show thumbnail, etc.
  }
};

socket.onerror = (error) => {
  console.error('WebSocket error:', error);
};
```

## 4. Rate Limiting

To ensure fair usage, our API has the following rate limits:

-   **Authenticated Users**: 1000 requests per hour.
-   **Job Submission**: 60 jobs per hour.

If you exceed these limits, you will receive a `429 Too Many Requests` response.

## 5. Best Practices

-   **Use WebSockets**: For status updates, prefer WebSockets over polling the `GET /jobs/{job_id}` endpoint to conserve resources.
-   **Cache Results**: Cache the results of API calls, especially for video metadata that does not change often.
-   **Handle Errors Gracefully**: Implement logic to handle different HTTP error codes and WebSocket connection issues.
-   **Keep Your Token Secure**: Never expose your access token on the client-side of a web application.
