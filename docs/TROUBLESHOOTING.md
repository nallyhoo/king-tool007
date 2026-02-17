
# Troubleshooting Guide

This guide provides solutions to common problems you might encounter.

## 1. `502 Bad Gateway` Error

This error usually means that Nginx cannot communicate with the backend or frontend service.

-   **Check Service Logs**: Run `docker-compose logs backend` or `docker-compose logs frontend` to look for errors.
-   **Check Container Status**: Run `docker-compose ps` to ensure that all containers are running and healthy.
-   **Firewall**: Make sure your firewall is not blocking communication between the containers.

## 2. `Permission Denied` Errors

-   **Docker Socket**: If you get a `permission denied` error when running `docker` commands, make sure your user is in the `docker` group (`sudo usermod -aG docker ${USER}`). You may need to log out and log back in for this to take effect.
-   **File Permissions**: Ensure that the files and directories mounted as volumes have the correct permissions.

## 3. Database Connection Issues

-   **Check `.env` file**: Verify that the `DATABASE_URL` and other database-related environment variables are correct.
-   **Network**: Ensure that the backend container can reach the database container. You can test this with `docker-compose exec backend ping db`.

## 4. Worker Issues

-   **Redis Connection**: Check the worker logs (`docker-compose logs download-worker`) for any Redis connection errors.
-   **Task Queues**: Use a Redis client to inspect the task queues and see if tasks are being added and processed.

## 5. Scaling Recommendations

-   **Vertical Scaling**: Increase the resources (CPU/memory) allocated to your containers or server.
-   **Horizontal Scaling**: 
    -   For the backend and workers, you can increase the number of replicas in your `docker-compose.prod.yml` and run `docker-compose up -d --scale backend=3`.
    -   For a more robust solution, move to a container orchestration platform like Kubernetes or AWS ECS.
