# IMS Project Plan

## Objective

Build a distributed Incident Management System capable of:
- Async signal ingestion
- Incident lifecycle management
- RCA workflows
- Dashboard monitoring

---

# Architecture

Signal Producers
↓
FastAPI API
↓
Redis Queue
↓
Async Worker
↓
MongoDB + PostgreSQL
↓
React Dashboard

---

# Tech Stack

- FastAPI
- ReactJS
- PostgreSQL
- MongoDB
- Redis
- Docker

---

# Backpressure Handling

Redis queue absorbs burst traffic and prevents backend crashes during persistence slowdowns.

---

# Features

- Async processing
- RCA workflow
- MTTR calculation
- CSV export
- Live dashboard
- Debouncing logic
- Rate limiting
- Health endpoint
