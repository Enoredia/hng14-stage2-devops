# HNG Stage 2 DevOps – Multi-Service Job Processing System

## Project Description

This project is part of the HNG Stage 2 DevOps task.

The application is a multi-service job processing system consisting of:

- A Node.js frontend for submitting and tracking jobs
- A Python FastAPI API for creating and retrieving job status
- A Python worker that processes jobs from a queue
- A Redis instance used as a shared queue and data store

The goal of this task is to make the application production-ready through:

- Fixing application bugs
- Containerizing all services
- Orchestrating services with Docker Compose
- Implementing a full CI/CD pipeline

---

## Prerequisites

Ensure the following tools are installed:

- Git
- Docker
- Docker Compose
- Python 3.11+
- Node.js 18+
- npm

---

## Environment Setup

Create a `.env` file from the example:

```bash
cp .env.example .env


