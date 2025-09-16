# PLAYALTER Deployment Guide

## Deployment Overview

This comprehensive deployment guide provides step-by-step instructions for deploying PLAYALTER across multiple environments, from local development to production-grade infrastructure. The deployment strategy follows Ph.D level engineering standards with enterprise-grade reliability and security.

## Prerequisites

### System Requirements

**Minimum Requirements:**

- **CPU**: 4 cores (8 cores recommended)
- **RAM**: 8GB (16GB recommended)
- **Storage**: 50GB SSD (100GB recommended)
- **Network**: 100Mbps bandwidth
- **OS**: Ubuntu 20.04 LTS / CentOS 8 / Windows Server 2019

**Recommended Production Setup:**

- **CPU**: 16+ cores
- **RAM**: 32GB+
- **Storage**: 500GB+ NVMe SSD
- **Network**: 1Gbps+ bandwidth
- **OS**: Ubuntu 22.04 LTS

### Software Dependencies

**Core Dependencies:**

```bash
# Python 3.11+
python --version  # Should be 3.11 or higher

# Docker & Docker Compose
docker --version
docker-compose --version

# Git
git --version

# Node.js (for frontend builds)
node --version  # Should be 18+ LTS
npm --version
```

**Database Requirements:**

- PostgreSQL 14+ (recommended 15+)
- Redis 6+ (recommended 7+)

### Platform API Keys

Ensure you have valid API keys for all integrated platforms:

- **N8N**: Webhook endpoint and API credentials
- **Stripe**: Secret key and webhook endpoint secret
- **OpenAI**: API key with appropriate billing setup
- **Replicate**: API token with model access
- **Agora**: App ID and App Certificate
- **Vercel**: Access token and team ID

## Environment Setup

### Development Environment

**1. Clone Repository:**

```bash
git clone https://github.com/your-org/playalter-project.git
cd playalter-project
```

**2. Create Virtual Environment:**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate
```

**3. Install Dependencies:**

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Install frontend dependencies (if applicable)
npm install
```

**4. Environment Configuration:**

```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

**Environment Variables (.env):**

```bash
# Application Settings
APP_NAME=PLAYALTER
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=your-super-secret-key-here

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/playalter_dev
REDIS_URL=redis://localhost:6379/0

# Platform API Keys
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/
N8N_API_KEY=your-n8n-api-key

STRIPE_SECRET_KEY=sk_test_your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret

OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_ORG_ID=org-your-organization-id

REPLICATE_API_TOKEN=r8_your-replicate-token

AGORA_APP_ID=your-agora-app-id
AGORA_APP_CERTIFICATE=your-agora-certificate

VERCEL_ACCESS_TOKEN=your-vercel-token
VERCEL_TEAM_ID=your-team-id

# Security Settings
JWT_SECRET_KEY=your-jwt-secret-key
ENCRYPTION_KEY=your-encryption-key
```

**5. Database Setup:**

```bash
# Start local PostgreSQL and Redis
docker-compose up -d postgres redis

# Run database migrations
python scripts/migrate_database.py

# Seed initial data (optional)
python scripts/seed_data.py
```

**6. Start Development Server:**

```bash
# Start the application
python platform_orchestrator.py

# Or use development mode with auto-reload
python -m uvicorn platform_orchestrator:app --reload --host 0.0.0.0 --port 8000
```

### Staging Environment

**1. Infrastructure Setup:**

```bash
# Create staging environment
mkdir -p environments/staging
cd environments/staging

# Copy staging configuration
cp ../../docker-compose.staging.yml docker-compose.yml
cp ../../.env.staging .env
```

**2. Docker Deployment:**

```bash
# Build application image
docker build -t playalter:staging .

# Start staging environment
docker-compose up -d

# Verify deployment
docker-compose ps
```

**3. SSL Configuration:**

```bash
# Generate SSL certificates with Let's Encrypt
certbot certonly --standalone -d staging.playalter.com

# Update nginx configuration
cp nginx/staging.conf /etc/nginx/sites-available/playalter-staging
ln -s /etc/nginx/sites-available/playalter-staging /etc/nginx/sites-enabled/
nginx -s reload
```

### Production Environment

**1. Infrastructure Provisioning:**

**AWS ECS Deployment:**

```yaml
# ecs-task-definition.json
{
  "family": "playalter-production",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::account:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "playalter-app",
      "image": "your-account.dkr.ecr.region.amazonaws.com/playalter:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "ENVIRONMENT",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:playalter/database-url"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/playalter",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

**Kubernetes Deployment:**

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: playalter-deployment
  labels:
    app: playalter
spec:
  replicas: 3
  selector:
    matchLabels:
      app: playalter
  template:
    metadata:
      labels:
        app: playalter
    spec:
      containers:
      - name: playalter
        image: playalter:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: playalter-secrets
              key: database-url
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: playalter-service
spec:
  selector:
    app: playalter
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```

**2. Database Migration:**

```bash
# Production database setup
python scripts/prod_migrate.py --environment=production

# Backup verification
python scripts/verify_backup.py --environment=production
```

**3. Security Hardening:**

```bash
# SSL/TLS configuration
certbot certonly --dns-cloudflare -d playalter.com -d *.playalter.com

# Firewall configuration
ufw enable
ufw allow 22/tcp  # SSH
ufw allow 80/tcp  # HTTP
ufw allow 443/tcp # HTTPS
ufw deny 8000/tcp # Block direct app access

# Security headers in nginx
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
```

## Container Deployment

### Docker Configuration

**Dockerfile:**

```dockerfile
# Multi-stage build for optimized production image
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim as production

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Start application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "platform_orchestrator:app"]
```

**Docker Compose (Production):**

```yaml
version: '3.8'

services:
  app:
    build: .
    image: playalter:latest
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
    env_file:
      - .env.production
    depends_on:
      - postgres
      - redis
    volumes:
      - ./logs:/app/logs
    networks:
      - playalter-network

  postgres:
    image: postgres:15
    restart: unless-stopped
    environment:
      POSTGRES_DB: playalter
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    networks:
      - playalter-network

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - playalter-network

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - ./nginx/logs:/var/log/nginx
    depends_on:
      - app
    networks:
      - playalter-network

volumes:
  postgres_data:
  redis_data:

networks:
  playalter-network:
    driver: bridge
```

### Kubernetes Deployment

**Complete Kubernetes Configuration:**

```bash
# Create namespace
kubectl create namespace playalter

# Apply secrets
kubectl apply -f kubernetes/secrets.yaml -n playalter

# Apply configmaps
kubectl apply -f kubernetes/configmap.yaml -n playalter

# Deploy PostgreSQL
kubectl apply -f kubernetes/postgres.yaml -n playalter

# Deploy Redis
kubectl apply -f kubernetes/redis.yaml -n playalter

# Deploy application
kubectl apply -f kubernetes/deployment.yaml -n playalter

# Apply ingress
kubectl apply -f kubernetes/ingress.yaml -n playalter
```

**Ingress Configuration:**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: playalter-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - playalter.com
    - api.playalter.com
    secretName: playalter-tls
  rules:
  - host: playalter.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: playalter-service
            port:
              number: 80
  - host: api.playalter.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: playalter-service
            port:
              number: 80
```

## Cloud Deployment

### AWS Deployment

**Infrastructure as Code (Terraform):**

```hcl
# terraform/main.tf
provider "aws" {
  region = var.aws_region
}

# VPC Configuration
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "playalter-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  
  enable_nat_gateway = true
  enable_vpn_gateway = false
  
  tags = {
    Terraform = "true"
    Environment = var.environment
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "playalter" {
  name = "playalter-${var.environment}"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# Application Load Balancer
resource "aws_lb" "playalter" {
  name               = "playalter-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = module.vpc.public_subnets
  
  enable_deletion_protection = var.environment == "production"
}

# RDS PostgreSQL
resource "aws_db_instance" "playalter" {
  identifier = "playalter-${var.environment}"
  
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = var.db_instance_class
  
  allocated_storage     = var.db_allocated_storage
  max_allocated_storage = var.db_max_allocated_storage
  storage_type          = "gp3"
  
  db_name  = "playalter"
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.playalter.name
  
  backup_retention_period = var.environment == "production" ? 30 : 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = var.environment != "production"
  deletion_protection = var.environment == "production"
  
  tags = {
    Name = "playalter-${var.environment}"
    Environment = var.environment
  }
}

# ElastiCache Redis
resource "aws_elasticache_subnet_group" "playalter" {
  name       = "playalter-cache-subnet"
  subnet_ids = module.vpc.private_subnets
}

resource "aws_elasticache_replication_group" "playalter" {
  replication_group_id       = "playalter-${var.environment}"
  description                = "Redis cluster for PLAYALTER"
  
  port               = 6379
  parameter_group_name = "default.redis7"
  
  num_cache_clusters = var.environment == "production" ? 3 : 1
  node_type          = var.redis_node_type
  
  subnet_group_name  = aws_elasticache_subnet_group.playalter.name
  security_group_ids = [aws_security_group.elasticache.id]
  
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  auth_token                 = var.redis_auth_token
  
  tags = {
    Name = "playalter-${var.environment}"
    Environment = var.environment
  }
}
```

**Deployment Script:**

```bash
#!/bin/bash
# scripts/deploy_aws.sh

set -e

ENVIRONMENT=${1:-staging}
AWS_REGION=${2:-us-east-1}

echo "Deploying PLAYALTER to AWS - Environment: $ENVIRONMENT"

# Build and push Docker image
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

docker build -t playalter:$ENVIRONMENT .
docker tag playalter:$ENVIRONMENT $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/playalter:$ENVIRONMENT
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/playalter:$ENVIRONMENT

# Deploy infrastructure
cd terraform
terraform init
terraform plan -var="environment=$ENVIRONMENT" -var="aws_region=$AWS_REGION"
terraform apply -var="environment=$ENVIRONMENT" -var="aws_region=$AWS_REGION" -auto-approve

# Update ECS service
aws ecs update-service \
    --cluster playalter-$ENVIRONMENT \
    --service playalter-service \
    --force-new-deployment \
    --region $AWS_REGION

echo "Deployment completed successfully!"
```

### Azure Deployment

**Azure Resource Manager Template:**

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "environment": {
      "type": "string",
      "allowedValues": ["dev", "staging", "production"]
    },
    "location": {
      "type": "string",
      "defaultValue": "[resourceGroup().location]"
    }
  },
  "variables": {
    "appName": "[concat('playalter-', parameters('environment'))]"
  },
  "resources": [
    {
      "type": "Microsoft.ContainerInstance/containerGroups",
      "apiVersion": "2021-09-01",
      "name": "[variables('appName')]",
      "location": "[parameters('location')]",
      "properties": {
        "containers": [
          {
            "name": "playalter-app",
            "properties": {
              "image": "playalter:latest",
              "ports": [
                {
                  "port": 8000,
                  "protocol": "TCP"
                }
              ],
              "environmentVariables": [
                {
                  "name": "ENVIRONMENT",
                  "value": "[parameters('environment')]"
                }
              ],
              "resources": {
                "requests": {
                  "cpu": 2,
                  "memoryInGB": 4
                }
              }
            }
          }
        ],
        "osType": "Linux",
        "ipAddress": {
          "type": "Public",
          "ports": [
            {
              "port": 8000,
              "protocol": "TCP"
            }
          ]
        }
      }
    }
  ]
}
```

### Google Cloud Platform

**Cloud Run Deployment:**

```bash
#!/bin/bash
# scripts/deploy_gcp.sh

PROJECT_ID="your-project-id"
SERVICE_NAME="playalter"
REGION="us-central1"

# Build and push to Container Registry
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME .

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --max-instances 100 \
    --set-env-vars ENVIRONMENT=production \
    --set-secrets DATABASE_URL=database-url:latest \
    --set-secrets OPENAI_API_KEY=openai-key:latest
```

## Database Deployment

### PostgreSQL Setup

**Production Configuration:**

```sql
-- scripts/postgres_setup.sql

-- Create database
CREATE DATABASE playalter;

-- Create application user
CREATE USER playalter_app WITH PASSWORD 'secure_password_here';

-- Grant privileges
GRANT CONNECT ON DATABASE playalter TO playalter_app;
GRANT USAGE ON SCHEMA public TO playalter_app;
GRANT CREATE ON SCHEMA public TO playalter_app;

-- Create tables
\c playalter;

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    type VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    parameters JSONB,
    result JSONB,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE platform_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID REFERENCES workflows(id),
    platform VARCHAR(50) NOT NULL,
    action VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    request_data JSONB,
    response_data JSONB,
    response_time INTEGER,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_workflows_user_id ON workflows(user_id);
CREATE INDEX idx_workflows_status ON workflows(status);
CREATE INDEX idx_platform_logs_workflow_id ON platform_logs(workflow_id);
CREATE INDEX idx_platform_logs_platform ON platform_logs(platform);
CREATE INDEX idx_platform_logs_created_at ON platform_logs(created_at);

-- Grant table permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO playalter_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO playalter_app;
```

**Migration Script:**

```python
#!/usr/bin/env python3
# scripts/migrate_database.py

import asyncio
import asyncpg
import os
from pathlib import Path

async def run_migrations():
    """Run database migrations"""
    
    # Database connection
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is required")
    
    # Connect to database
    conn = await asyncpg.connect(database_url)
    
    try:
        # Read migration files
        migrations_dir = Path(__file__).parent / 'migrations'
        migration_files = sorted(migrations_dir.glob('*.sql'))
        
        for migration_file in migration_files:
            print(f"Running migration: {migration_file.name}")
            
            with open(migration_file, 'r') as f:
                sql = f.read()
            
            await conn.execute(sql)
            print(f"✓ Completed: {migration_file.name}")
            
    finally:
        await conn.close()
    
    print("All migrations completed successfully!")

if __name__ == "__main__":
    asyncio.run(run_migrations())
```

### Redis Configuration

**Production Redis Setup:**

```bash
# redis.conf for production
bind 127.0.0.1
protected-mode yes
port 6379
tcp-backlog 511
timeout 0
tcp-keepalive 300

# Authentication
requirepass your_secure_redis_password

# Memory management
maxmemory 2gb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb

# Append only file
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# Logging
loglevel notice
logfile /var/log/redis/redis-server.log

# Security
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command KEYS ""
rename-command CONFIG "CONFIG_b835729a0d_"
```

## Monitoring & Logging

### Application Monitoring

**Prometheus Configuration:**

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'playalter'
    static_configs:
      - targets: ['playalter:8000']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
```

**Grafana Dashboard:**

```json
{
  "dashboard": {
    "id": null,
    "title": "PLAYALTER Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{status}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      },
      {
        "title": "Platform Integration Status",
        "type": "stat",
        "targets": [
          {
            "expr": "platform_integration_health",
            "legendFormat": "{{platform}}"
          }
        ]
      }
    ]
  }
}
```

### Centralized Logging

**ELK Stack Configuration:**

```yaml
# docker-compose.logging.yml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.8.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"

  logstash:
    image: docker.elastic.co/logstash/logstash:8.8.0
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline
    ports:
      - "5044:5044"
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.8.0
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

volumes:
  elasticsearch_data:
```

## Security Deployment

### SSL/TLS Configuration

**Nginx SSL Configuration:**

```nginx
# nginx/ssl.conf
server {
    listen 80;
    server_name playalter.com www.playalter.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name playalter.com www.playalter.com;

    # SSL Configuration
    ssl_certificate /etc/nginx/ssl/playalter.com.crt;
    ssl_certificate_key /etc/nginx/ssl/playalter.com.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Application proxy
    location / {
        proxy_pass http://playalter:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Secrets Management

**Kubernetes Secrets:**

```bash
# Create secrets for production
kubectl create secret generic playalter-secrets \
    --from-literal=database-url="postgresql://user:pass@host:5432/db" \
    --from-literal=openai-api-key="sk-your-openai-key" \
    --from-literal=stripe-secret-key="sk_live_your-stripe-key" \
    --from-literal=jwt-secret="your-jwt-secret" \
    -n playalter
```

**AWS Secrets Manager:**

```bash
# Store secrets in AWS Secrets Manager
aws secretsmanager create-secret \
    --name "playalter/database-url" \
    --description "Database connection URL for PLAYALTER" \
    --secret-string "postgresql://user:pass@host:5432/playalter"

aws secretsmanager create-secret \
    --name "playalter/openai-api-key" \
    --description "OpenAI API key for PLAYALTER" \
    --secret-string "sk-your-openai-api-key"
```

## Backup & Recovery

### Database Backup

**Automated Backup Script:**

```bash
#!/bin/bash
# scripts/backup_database.sh

BACKUP_DIR="/backups"
RETENTION_DAYS=30
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create backup
pg_dump $DATABASE_URL > "$BACKUP_DIR/playalter_backup_$TIMESTAMP.sql"

# Compress backup
gzip "$BACKUP_DIR/playalter_backup_$TIMESTAMP.sql"

# Upload to S3
aws s3 cp "$BACKUP_DIR/playalter_backup_$TIMESTAMP.sql.gz" \
    s3://playalter-backups/database/

# Clean old backups
find $BACKUP_DIR -name "playalter_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup completed: playalter_backup_$TIMESTAMP.sql.gz"
```

**Recovery Procedure:**

```bash
#!/bin/bash
# scripts/restore_database.sh

BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

# Download from S3 if needed
if [[ $BACKUP_FILE == s3://* ]]; then
    aws s3 cp $BACKUP_FILE ./restore_temp.sql.gz
    BACKUP_FILE="./restore_temp.sql.gz"
fi

# Decompress if needed
if [[ $BACKUP_FILE == *.gz ]]; then
    gunzip -c $BACKUP_FILE > restore_temp.sql
    BACKUP_FILE="restore_temp.sql"
fi

# Restore database
psql $DATABASE_URL < $BACKUP_FILE

# Cleanup
rm -f restore_temp.sql restore_temp.sql.gz

echo "Database restore completed"
```

## Performance Optimization

### Application Tuning

**Gunicorn Configuration:**

```python
# gunicorn.conf.py
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
keepalive = 2
timeout = 30
graceful_timeout = 30

# Logging
accesslog = "/app/logs/access.log"
errorlog = "/app/logs/error.log"
loglevel = "info"

# Process naming
proc_name = "playalter"

# Worker tuning
worker_tmp_dir = "/dev/shm"
```

### Database Optimization

**PostgreSQL Tuning:**

```sql
-- PostgreSQL configuration for production
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
ALTER SYSTEM SET random_page_cost = 1.1;
ALTER SYSTEM SET effective_io_concurrency = 200;

-- Reload configuration
SELECT pg_reload_conf();
```

This comprehensive deployment guide provides enterprise-grade deployment procedures for PLAYALTER across multiple environments and cloud platforms, ensuring Ph.D level reliability and performance standards.
