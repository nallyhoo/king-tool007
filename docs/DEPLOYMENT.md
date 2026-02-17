
# Deployment Guide

Welcome to the deployment guide for the Video Manager application. This document provides a high-level overview of the different deployment options and links to detailed guides for each.

## Table of Contents

1.  **[Self-Hosted Deployment](./SELF_HOSTED.md)**
    -   **Best for**: Small-scale deployments, development, or staging environments on a single Virtual Private Server (VPS) or dedicated server.
    -   **Technology**: Docker Compose
    -   **Complexity**: Low

2.  **[Cloud Deployment (AWS)](./CLOUD_DEPLOYMENT_AWS.md)**
    -   **Best for**: Scalable, highly available production deployments.
    -   **Technology**: AWS ECS, Fargate, RDS, S3, ElastiCache
    -   **Complexity**: Medium to High

3.  **[Monitoring & Logging](./MONITORING.md)**
    -   A guide to setting up robust monitoring, logging, and alerting for your application.

4.  **[Backup & Disaster Recovery](./BACKUP.md)**
    -   Strategies and scripts for backing up your data and recovering from a disaster.

## Choosing a Deployment Strategy

-   If you are just getting started or have a small user base, the **Self-Hosted** option is the simplest and most cost-effective.
-   For production applications that require high availability, scalability, and managed services, a **Cloud Deployment** is the recommended approach.
