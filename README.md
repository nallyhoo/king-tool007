# Video Manager

A comprehensive tool for managing, searching, and analyzing video content. This project provides a backend API built with FastAPI and a frontend client built with React. It includes features for video downloading, processing, and advanced search using Elasticsearch.

## Features

*   **Video Downloading:** Download videos from various sources.
*   **Video Processing:** Automatically transcode and process videos.
*   **Advanced Search:** Full-text search on video metadata and transcripts using Elasticsearch.
*   **Real-time Updates:** WebSocket integration for real-time progress updates.
*   **User Authentication:** Secure user authentication and authorization.
*   **Task Queue:** Asynchronous task handling with Celery and Redis.

## Technologies

*   **Backend:**
    *   Python
    *   FastAPI
    *   SQLAlchemy
    *   PostgreSQL
    *   Elasticsearch
    *   Celery
    *   Redis
*   **Frontend:**
    *   React
    *   TypeScript
    *   Vite
*   **DevOps:**
    *   Docker
    *   Nginx

## Installation

1.  **Prerequisites:**
    *   Docker and Docker Compose
2.  **Clone the repository:**
    ```bash
    git clone https://github.com/nallyhoo/king-tool007.git
    cd king-tool007
    ```
3.  **Set up environment variables:**
    *   Copy the `.env.example` file to `.env` and update the values as needed.
4.  **Build and run the application:**
    ```bash
    docker-compose up -d --build
    ```

## Usage

*   **API:** The backend API is accessible at `http://localhost:8000`.
*   **Frontend:** The frontend application is accessible at `http://localhost:3000`.

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes and commit them (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/your-feature-name`).
5.  Create a new Pull Request.
