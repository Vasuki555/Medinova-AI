# MediNova AI

A comprehensive healthcare management platform with AI-powered features for patients, doctors, and administrators.

## Features

### For Patients
- 📋 **Health Records Management** - Store and manage medical records (vitals, diagnoses, lab tests, notes)
- 📅 **Appointment Booking** - Schedule appointments with doctors
- 💊 **Medication Tracking** - Manage prescriptions and medication schedules
- 🤖 **AI Health Assistant** - Chat with AI for health queries
- 📄 **Smart Document Upload** - OCR-powered medical document processing
- 🔔 **Notifications** - Real-time updates for appointments and medications
- 📱 **QR Code** - Quick medical information sharing

### For Doctors
- 👥 **Patient Management** - View and manage patient records
- 📅 **Appointment Management** - Handle appointment requests
- 📝 **Prescription Writing** - Create and manage prescriptions
- 📊 **Dashboard Analytics** - Patient statistics and insights
- ⏰ **Availability Management** - Set consultation hours and fees
- 📱 **QR Code** - Share booking page with patients

### For Admins
- 👨‍⚕️ **Doctor Verification** - Approve and manage doctor registrations
- 👤 **User Management** - Manage all platform users
- 📊 **System Analytics** - Monitor platform usage and statistics

## Tech Stack

### Frontend
- React 18 with Vite
- TailwindCSS for styling
- React Router for navigation
- Lucide React icons
- Axios for API calls

### Backend
- Python FastAPI
- MongoDB (MongoDB Atlas)
- JWT authentication
- Google OAuth integration
- OpenAI API for AI features
- Tesseract OCR for document processing
- QR code generation

## Setup Instructions

### Prerequisites
- Node.js 18+
- Python 3.11+
- MongoDB Atlas account
- OpenAI API key (optional, for AI features)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file (copy from `.env.example`):
```env
MONGODB_URI=your_mongodb_atlas_uri
SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

5. Run the backend:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

4. Run the frontend:
```bash
npm run dev
```

5. Open browser at `http://localhost:5173`

## Project Structure

```
MediNova/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # API endpoints
│   │   ├── models/          # MongoDB models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   ├── core/            # Core utilities
│   │   └── utils/           # Helper functions
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── context/         # React context
│   │   ├── services/        # API services
│   │   └── utils/           # Utilities
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Default Credentials

For testing purposes:
- **Patient**: sharma333@test.com / password123
- **Doctor**: john.doctor@example.com / password123
- **Admin**: admin@medinova.com / admin123

## Security Features

- JWT-based authentication with refresh tokens
- Password hashing with bcrypt
- CORS configuration
- Rate limiting
- Input validation
- Secure file upload handling

## License

MIT License

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Support

For issues and questions, please open a GitHub issue.
