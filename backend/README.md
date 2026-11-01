# MediNova AI - Backend

FastAPI backend for the MediNova AI healthcare platform.

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- MongoDB Atlas account
- pip (Python package manager)

### Installation

1. **Create virtual environment**

```bash
python -m venv venv
```

2. **Activate virtual environment**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

```bash
copy .env.example .env
```

Edit `.env` and configure:
- `MONGODB_URL` - Your MongoDB Atlas connection string
- `JWT_SECRET_KEY` - Generate a secure random key (min 32 characters)
- Other settings as needed

5. **Run the application**

```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI application entry point
│   ├── config.py                # Configuration management
│   ├── database.py              # MongoDB connection
│   │
│   ├── api/                     # API routes
│   │   ├── __init__.py
│   │   └── v1/                  # API version 1
│   │       ├── __init__.py      # API router
│   │       └── health.py        # Health check endpoint
│   │
│   ├── core/                    # Core utilities
│   │   ├── __init__.py
│   │   └── logging.py           # Logging configuration
│   │
│   ├── models/                  # MongoDB models (future)
│   │   └── __init__.py
│   │
│   ├── schemas/                 # Pydantic schemas (future)
│   │   └── __init__.py
│   │
│   ├── services/                # Business logic (future)
│   │   └── __init__.py
│   │
│   └── utils/                   # Helper functions (future)
│       └── __init__.py
│
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 📚 API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔌 Available Endpoints

### Root Endpoint
- `GET /` - API information

### Health Check
- `GET /api/v1/health` - System health status

### Authentication 🆕
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user (protected)

**Quick Start:** See [README_AUTH.md](./README_AUTH.md) for testing guide

## 🗄️ Database

The application uses **MongoDB Atlas** as the database.

### Collections (to be created in future modules):
- `users` - User authentication and profiles
- `patient_profiles` - Patient medical information
- `doctor_profiles` - Doctor professional information
- `appointments` - Appointment bookings
- `symptom_reports` - AI symptom analysis sessions
- `medical_documents` - Uploaded medical reports
- `prescriptions` - Doctor prescriptions
- `medications` - Medication schedules
- `health_records` - Vital signs and health data
- `ai_conversations` - AI chat history
- `notifications` - User notifications
- `hospitals` - Hospital information
- `analytics_events` - User activity tracking
- `admin_audit_logs` - Admin action logging

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MONGODB_URL` | MongoDB Atlas connection string | Yes |
| `MONGODB_DB_NAME` | Database name | Yes |
| `JWT_SECRET_KEY` | Secret key for JWT tokens | Yes |
| `JWT_ALGORITHM` | JWT algorithm (HS256) | No |
| `CORS_ORIGINS` | Allowed CORS origins | No |
| `DEBUG` | Enable debug mode | No |
| `LOG_LEVEL` | Logging level | No |

## 🧪 Testing

```bash
# Run health check
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "app_name": "MediNova AI",
  "version": "1.0.0",
  "environment": "development",
  "timestamp": "2026-07-03T10:00:00",
  "database_connected": true
}
```

## 🛠️ Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Document functions with docstrings
- Keep functions small and focused

### Adding New Endpoints

1. Create a new router file in `app/api/v1/`
2. Define your endpoints
3. Include the router in `app/api/v1/__init__.py`

Example:
```python
# app/api/v1/example.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def example_endpoint():
    return {"message": "Hello"}
```

```python
# app/api/v1/__init__.py
from app.api.v1 import example

api_router.include_router(
    example.router,
    prefix="/example",
    tags=["Example"]
)
```

## 📦 Dependencies

Main dependencies:
- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation
- **python-jose** - JWT handling
- **passlib** - Password hashing

## 🔄 Next Steps

Future modules will add:
- Authentication (JWT)
- User management
- Patient profiles
- Doctor profiles
- Appointments
- AI symptom checker
- Medical document upload
- And more...

## 📝 License

Academic project - Final Year Engineering

## 🤝 Contributing

This is an academic project. Internal team only.
