# Incident Management System (IMS)

## Overview

A distributed Incident Management System designed to process infrastructure failures in real-time.

Supports:
- Async signal ingestion
- Incident workflows
- RCA management
- MTTR calculation
- Dashboard monitoring

---

# Architecture Diagram

```text
Signal Producers
        ↓
FastAPI Ingestion API
        ↓
Redis Queue
        ↓
Async Worker
   ↓           ↓
MongoDB    PostgreSQL
        ↓
React Dashboard
```

---

# Tech Stack

## Backend
- FastAPI
- Python
- SQLAlchemy

## Frontend
- ReactJS

## Databases
- PostgreSQL
- MongoDB
- Redis

## Containerization
- Docker
- Docker Compose

---

# Features

- Async Processing
- Incident Lifecycle Management
- RCA Validation
- MTTR Calculation
- CSV Export
- Live Dashboard
- Search Filtering
- Rate Limiting
- Health Monitoring
- Throughput Metrics

---

# APIs

## Health
GET /health

## Signal Ingestion
POST /signals

## Incident List
GET /incidents

## RCA Submission
POST /rca

## Update Incident State
PUT /incidents/{incident_id}/state

---

# Setup Instructions

## Start Containers

```bash
docker-compose up -d
```

## Run Backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Run Worker

```bash
python -m app.worker
```

## Run Frontend

```bash
npm start
```

---

# Dashboard

Frontend:
http://localhost:3000

Swagger:
http://localhost:8000/docs

---

# Backpressure Handling

Redis queue is used as an in-memory buffer to absorb high-volume incoming signals.

---

# Bonus Features

- Dark Theme Dashboard
- CSV Export
- Search Functionality
- Live Refresh
- Severity Highlighting

---

# Author

Sura Naga Vijay
