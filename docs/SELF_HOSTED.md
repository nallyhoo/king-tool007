
# Self-Hosted Deployment Guide

This guide will walk you through deploying the application to a single server running Ubuntu 22.04 using Docker Compose.

## 1. Prerequisites

-   A server running Ubuntu 22.04 with at least 4GB of RAM and 2 CPUs.
-   A domain name pointed at your server's IP address.
-   Sudo or root access to the server.

## 2. Initial Server Setup

Connect to your server via SSH and perform the following initial setup.

### 2.1. Update the System

```bash
sudo apt update && sudo apt upgrade -y
```

### 2.2. Create a Non-Root User

```bash
sudo adduser deployer
sudo usermod -aG sudo deployer
su - deployer
```

### 2.3. Install Docker and Docker Compose

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Add user to the docker group
sudo usermod -aG docker ${USER}

# Install Docker Compose
sudo apt install docker-compose-plugin
```

## 3. Application Setup

### 3.1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### 3.2. Configure Environment Variables

Create a `.env` file from the example and fill in your production values.

```bash
cp .env.example .env
nano .env
```

### 3.3. Configure Nginx for Production

Edit the production Nginx configuration to use your domain name.

```bash
nano nginx/nginx.prod.conf
```

Replace `your_domain.com` with your actual domain name.

## 4. SSL Certificate (Let's Encrypt)

We will use Certbot to obtain a free SSL certificate.

### 4.1. Install Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 4.2. Obtain the Certificate

Certbot will automatically edit your Nginx configuration to enable SSL.

```bash
sudo certbot --nginx -d your_domain.com
```

Follow the on-screen instructions. Certbot will also set up a cron job to automatically renew your certificate.

## 5. Firewall Configuration

We will use `ufw` (Uncomplicated Firewall) to secure the server.

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## 6. Running the Application

Now you can build and run your application in production mode.

```bash
make build-prod
make up-prod
```

Your application should now be accessible at `https://your_domain.com`.

## 7. Backup Strategy

Refer to the [Backup & Disaster Recovery Guide](./BACKUP.md) for detailed instructions on how to back up your data.
