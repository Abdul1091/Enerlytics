# Enerlytics Backend

Backend service for the Enerlytics platform, built with FastAPI.

## Overview

The backend provides the REST API that powers Enerlytics. It handles consumer reports, analytics, authentication, and data management.

## Tech Stack

- Python
- FastAPI
- uv
- PostgreSQL (planned)
- SQLAlchemy (planned)
- Alembic (planned)

## Project Structure

```text
backend/
├── app/
│   ├── __init__.py
│   └── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12+
- uv

### Installation

Clone the repository and navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
uv venv
```

Activate it:

**Linux/macOS**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
uv sync
```

## Running the Development Server

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at:

- http://127.0.0.1:8000

Interactive API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Development Status

🚧 The backend is under active development.

Upcoming features include:

- API routing
- Configuration management
- Database integration
- Authentication
- Outage reporting
- Analytics services

## License

This project is licensed under the MIT License.