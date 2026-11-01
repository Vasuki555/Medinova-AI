# MediNova Project Files Guide

## 📁 Essential Documentation (Root Directory)

### Core Documentation
- **README.md** - Main project documentation and overview
- **QUICK_START.md** - Quick setup and run instructions
- **PROJECT_STRUCTURE.md** - Project organization and structure

### Design & Architecture
- **MediNova_AI_SRS_PRD.md** - Software Requirements & Product Requirements
- **MediNova_Architecture_Document.md** - System architecture
- **MediNova_MongoDB_Database_Design.md** - Database schema and design
- **MediNova_Dashboard_Designs.md** - Dashboard UI designs
- **MediNova_Page_Designs.md** - Page layouts and designs
- **MediNova_Design_System.md** - UI/UX design system
- **MediNova_UX_Flows.md** - User experience flows

### Testing & Credentials
- **TEST_ACCOUNTS.md** - All test user accounts with credentials (8 accounts)
- **QUICK_LOGIN_REFERENCE.txt** - Quick reference for login credentials
- **IMPLEMENTATION_COMPLETE_SUMMARY.md** - Current implementation status

---

## 📁 Backend Files

### Essential Files
```
backend/
├── .env                          # Environment variables (MongoDB, JWT, etc.)
├── .env.example                  # Example environment configuration
├── requirements.txt              # Python dependencies
├── create_test_users.py          # Script to create test accounts
├── README.md                     # Backend documentation
├── AUTHENTICATION_MODULE.md      # Authentication system docs
├── FILE_EXPLANATIONS.md          # Explanation of backend files
└── app/                          # Main application code
    ├── main.py                   # FastAPI application entry
    ├── config.py                 # Configuration settings
    ├── database.py               # MongoDB connection
    ├── api/v1/                   # API endpoints
    ├── models/                   # Database models
    ├── schemas/                  # Pydantic schemas
    ├── services/                 # Business logic
    ├── core/                     # Core utilities
    └── utils/                    # Helper utilities
```

### Key Backend Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run backend server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Create test users
python create_test_users.py
```

---

## 📁 Frontend Files

### Essential Files
```
frontend/
├── .env                          # Environment variables (API URLs)
├── .env.example                  # Example environment configuration
├── package.json                  # Node.js dependencies
├── vite.config.js                # Vite configuration
├── tailwind.config.js            # Tailwind CSS configuration
├── README.md                     # Frontend documentation
└── src/                          # Source code
    ├── main.jsx                  # Application entry
    ├── App.jsx                   # Root component with routing
    ├── index.css                 # Global styles
    ├── components/               # Reusable components
    ├── pages/                    # Page components
    ├── context/                  # React context (Auth, Theme, Toast)
    ├── services/                 # API services
    └── utils/                    # Utility functions
```

### Key Frontend Commands
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

---

## 🗑️ Removed Files (Cleaned Up)

### Root Directory - Removed:
- ❌ AUTHENTICATION_BACKEND_FINAL.md (duplicate)
- ❌ AUTHENTICATION_FRONTEND_COMPLETE.md (duplicate)
- ❌ AUTHENTICATION_MODULE_SUMMARY.md (duplicate)
- ❌ BUG_FIX_STATUS.md (outdated)
- ❌ DEPLOYMENT_STATUS_REPORT.md (outdated)
- ❌ FIXES_IMPLEMENTATION_PLAN.md (consolidated)
- ❌ MONGODB_CLUSTER_ISSUE_REPORT.md (outdated)
- ❌ PROJECT_FOUNDATION_COMPLETE.md (outdated)
- ❌ PROJECT_TREE.txt (regenerable)
- ❌ QA_TESTING_REPORT.md (outdated)
- ❌ SAMPLE_DATA_CREDENTIALS.md (replaced by TEST_ACCOUNTS.md)
- ❌ SERVERS_RUNNING.md (temporary)
- ❌ SETUP_GUIDE.md (duplicate)
- ❌ MediNova_Architecture_Flows.md (duplicate)
- ❌ MediNova_Simplified_Architecture.md (duplicate)

### Backend - Removed:
- ❌ APP_STRUCTURE.txt (not needed)
- ❌ AUTHENTICATION_COMPLETE.md (duplicate)
- ❌ AUTHENTICATION_FLOW.md (duplicate)
- ❌ README_AUTH.md (duplicate)
- ❌ TESTING_GUIDE.md (outdated)
- ❌ test_auth.py (old test file)
- ❌ test_mongodb_connection.py (old test)
- ❌ test_mongodb_connection_v2.py (old test)
- ❌ test_direct_connection.py (old test)
- ❌ seed.py (old seed script)
- ❌ seed_direct.py (old seed script)
- ❌ seed_sample_data.py (old seed script)
- ❌ setup_complete_data.ps1 (old script)
- ❌ start_backend.ps1 (old script)

### Frontend - Removed:
- ❌ AUTHENTICATION_FRONTEND_MODULE.md (duplicate)
- ❌ AUTHENTICATION_TESTING_GUIDE.md (duplicate)
- ❌ FOLDER_STRUCTURE_EXPLAINED.md (not needed)

---

## 📝 Quick Reference

### Test Accounts (8 total)
See **TEST_ACCOUNTS.md** or **QUICK_LOGIN_REFERENCE.txt** for:
- 3 Patient accounts
- 3 Doctor accounts
- 2 Admin accounts

### Running the Project
1. **Backend:** `cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
2. **Frontend:** `cd frontend && npm run dev`
3. **Access:** http://localhost:5173

### Important URLs
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/v1/health

---

## 🎯 Current Status

### ✅ Working
- Authentication system
- All dashboards (Patient, Doctor, Admin)
- QR code system (Patient & Doctor)
- Navigation and routing
- Dark mode
- Responsive design

### ⚠️ Needs Attention
- **MongoDB Atlas Connection** - Currently using in-memory database
- Fix connection string in `backend/.env`
- Data will persist once MongoDB is connected

---

## 📚 Documentation Priority

1. **Start Here:** README.md
2. **Quick Setup:** QUICK_START.md
3. **Test Accounts:** TEST_ACCOUNTS.md
4. **Current Status:** IMPLEMENTATION_COMPLETE_SUMMARY.md
5. **Architecture:** MediNova_Architecture_Document.md
6. **Database:** MediNova_MongoDB_Database_Design.md

---

**Last Updated:** September 7, 2026
**Total Files Removed:** 32 duplicate/outdated files
**Project Status:** Clean and organized ✅
