# MediNova AI - Project Structure Documentation

## 📋 Complete File and Folder Explanation

This document explains the purpose and content of every file and folder in the MediNova AI project.

---

## 🗂️ Root Directory

```
MediNova/
├── backend/              # FastAPI Backend Application
├── frontend/             # React Frontend Application
├── README.md             # Main project documentation
└── PROJECT_STRUCTURE.md  # This file
```

### `README.md`
- **Purpose**: Main project documentation
- **Contains**: 
  - Project overview and description
  - Technology stack summary
  - Quick start instructions for both frontend and backend
  - Links to detailed documentation
  - API documentation URLs
  - Development workflow

---

## 🔧 Backend Directory (`backend/`)

### Root Files

#### `requirements.txt`
- **Purpose**: Python dependencies list
- **Contains**: All Python packages needed for the backend
- **Key Dependencies**:
  - `fastapi` - Web framework
  - `uvicorn` - ASGI server
  - `motor` - Async MongoDB driver
  - `pydantic` - Data validation
  - `python-jose` - JWT handling
  - `passlib` - Password hashing
  - `python-dotenv` - Environment variable management

#### `.env.example`
- **Purpose**: Template for environment variables
- **Contains**: All configuration variables with example values
- **Key Variables**:
  - MongoDB connection string
  - JWT secret key
  - CORS origins
  - Server configuration
  - OpenAI API key (for future use)
- **Usage**: Copy to `.env` and fill in actual values

#### `.gitignore`
- **Purpose**: Specifies files Git should ignore
- **Excludes**:
  - Python cache files (`__pycache__/`)
  - Virtual environment (`venv/`)
  - Environment files (`.env`)
  - IDE files (`.vscode/`, `.idea/`)
  - Log files (`*.log`)

#### `README.md`
- **Purpose**: Backend-specific documentation
- **Contains**:
  - Backend setup instructions
  - Project structure explanation
  - API endpoint documentation
  - Database schema overview
  - Development guidelines

---

### Application Directory (`backend/app/`)

#### `__init__.py`
- **Purpose**: Marks directory as Python package
- **Contains**: Package metadata (version, author)

#### `main.py`
- **Purpose**: FastAPI application entry point
- **Contains**:
  - FastAPI app initialization
  - CORS middleware configuration
  - Database connection lifecycle (startup/shutdown)
  - Route inclusion
  - Root endpoint
  - Application lifespan manager
- **Key Features**:
  - Automatic API documentation (/docs, /redoc)
  - Database connection on startup
  - Graceful shutdown handling

#### `config.py`
- **Purpose**: Configuration management
- **Contains**:
  - Settings class using Pydantic
  - Environment variable loading
  - Configuration validation
  - Helper properties (is_production, cors_origins_list)
- **Key Features**:
  - Type-safe configuration
  - Automatic validation
  - Environment-based settings

#### `database.py`
- **Purpose**: MongoDB connection management
- **Contains**:
  - Database class with connection methods
  - Async MongoDB client initialization
  - Connection health check
  - Dependency injection for routes
- **Key Methods**:
  - `connect_to_database()` - Establish connection
  - `close_database_connection()` - Close connection
  - `get_database()` - Get database instance
  - `check_connection()` - Health check

---

### Core Directory (`backend/app/core/`)

#### `__init__.py`
- **Purpose**: Core package marker
- **Contains**: Empty (package initialization)

#### `logging.py`
- **Purpose**: Logging configuration
- **Contains**:
  - Centralized logging setup
  - Development vs production formatting
  - Log level configuration
  - Suppression of noisy loggers
- **Features**:
  - Human-readable format for development
  - JSON format for production
  - Configurable log levels

---

### API Directory (`backend/app/api/`)

#### `__init__.py`
- **Purpose**: API package marker

#### `v1/__init__.py`
- **Purpose**: API version 1 router aggregation
- **Contains**:
  - Main API router
  - All route module inclusions
  - Route prefixes and tags
- **Current Routes**: Health check
- **Future Routes**: Authentication, Patients, Doctors, etc.

#### `v1/health.py`
- **Purpose**: Health check endpoint
- **Contains**:
  - Health check route handler
  - HealthResponse schema
  - Database connectivity check
- **Endpoint**: `GET /api/v1/health`
- **Response**:
  - System status (healthy/degraded)
  - App name and version
  - Environment
  - Database connection status
  - Current timestamp

---

### Models Directory (`backend/app/models/`)

#### `__init__.py`
- **Purpose**: Database models package
- **Status**: Empty (placeholder for future modules)
- **Future Content**: MongoDB document models

---

### Schemas Directory (`backend/app/schemas/`)

#### `__init__.py`
- **Purpose**: Pydantic schemas package
- **Status**: Empty (placeholder for future modules)
- **Future Content**: Request/Response validation schemas

---

### Services Directory (`backend/app/services/`)

#### `__init__.py`
- **Purpose**: Business logic package
- **Status**: Empty (placeholder for future modules)
- **Future Content**: Service layer for business logic

---

### Utils Directory (`backend/app/utils/`)

#### `__init__.py`
- **Purpose**: Utilities package
- **Status**: Empty (placeholder for future modules)
- **Future Content**: Helper functions and utilities

---

## 🎨 Frontend Directory (`frontend/`)

### Root Files

#### `package.json`
- **Purpose**: Node.js project configuration
- **Contains**:
  - Project metadata
  - Dependencies list
  - Scripts for development and build
  - ESLint and Prettier configuration references
- **Key Scripts**:
  - `npm run dev` - Start development server
  - `npm run build` - Build for production
  - `npm run preview` - Preview production build
  - `npm run lint` - Run ESLint

#### `.env.example`
- **Purpose**: Template for environment variables
- **Contains**:
  - API base URL
  - API timeout
  - App name and version
  - Environment setting
- **Usage**: Copy to `.env` and configure

#### `.gitignore`
- **Purpose**: Git ignore rules
- **Excludes**:
  - Node modules (`node_modules/`)
  - Build output (`dist/`)
  - Environment files (`.env`)
  - IDE files
  - OS files

#### `vite.config.js`
- **Purpose**: Vite bundler configuration
- **Contains**:
  - React plugin setup
  - Path aliases (`@/` → `src/`)
  - Development server configuration
  - API proxy configuration
  - Build optimization settings
- **Key Features**:
  - Hot module replacement
  - Proxy API calls to backend
  - Fast build times

#### `tailwind.config.js`
- **Purpose**: Tailwind CSS configuration
- **Contains**:
  - Custom color palette (Medical Blue theme)
  - Font family definitions (Inter, Manrope, JetBrains Mono)
  - Custom spacing values
  - Extended border radius
  - Custom box shadows
  - Content paths for purging
- **Brand Colors**: Primary (Medical Blue), Neutral, Success, Warning, Error

#### `postcss.config.js`
- **Purpose**: PostCSS configuration
- **Contains**: Tailwind and Autoprefixer plugins
- **Role**: Process CSS with Tailwind directives

#### `eslint.config.js`
- **Purpose**: ESLint configuration
- **Contains**:
  - React plugin rules
  - React Hooks rules
  - ES2020 syntax support
  - Browser globals
- **Standards**: Enforces code quality and React best practices

#### `index.html`
- **Purpose**: HTML template
- **Contains**:
  - HTML structure
  - Meta tags
  - Google Fonts links (Inter, Manrope, JetBrains Mono)
  - Root div for React
  - Script tag for main.jsx
- **Features**: SEO-friendly meta tags, responsive viewport

#### `README.md`
- **Purpose**: Frontend-specific documentation
- **Contains**:
  - Frontend setup instructions
  - Project structure details
  - Design system documentation
  - Available scripts
  - API integration guide
  - Development guidelines

---

### Public Directory (`frontend/public/`)

#### `vite.svg`
- **Purpose**: Vite logo (temporary favicon)
- **Contains**: SVG icon
- **Future**: Will be replaced with MediNova logo

---

### Source Directory (`frontend/src/`)

#### `main.jsx`
- **Purpose**: Application entry point
- **Contains**:
  - React DOM render
  - App component mount
  - Strict mode wrapper
- **Role**: Initializes React application

#### `App.jsx`
- **Purpose**: Root component with routing
- **Contains**:
  - BrowserRouter setup
  - Route definitions
  - Layout component usage
- **Current Routes**: Home page
- **Future Routes**: Login, Register, Dashboard, etc.

#### `index.css`
- **Purpose**: Global styles
- **Contains**:
  - Tailwind directives (@tailwind base, components, utilities)
  - Custom CSS components (buttons, inputs, cards)
  - Glassmorphism styles
  - Animation keyframes
  - Typography defaults
- **Features**:
  - `.btn-primary`, `.btn-secondary` - Button styles
  - `.input-field` - Form input styles
  - `.glass-card`, `.card` - Card styles
  - `.animate-fade-in`, `.animate-slide-up` - Animations

---

### Utils Directory (`frontend/src/utils/`)

#### `constants.js`
- **Purpose**: Application constants
- **Contains**:
  - API configuration (base URL, timeout)
  - Application info (name, version)
  - Route paths
  - User roles
  - Storage keys (for localStorage)
  - API endpoints
  - Date formats
  - Pagination settings
  - File upload limits
- **Usage**: Import constants throughout the app for consistency

---

### Services Directory (`frontend/src/services/`)

#### `api.js`
- **Purpose**: API service layer
- **Contains**:
  - Axios instance configuration
  - Request interceptor (adds JWT token)
  - Response interceptor (handles errors)
  - API methods (get, post, put, patch, delete)
  - Health check API
- **Features**:
  - Automatic authentication token injection
  - Error logging
  - 401 handling (logout)
  - Development request/response logging
  - Network error handling

---

### Components Directory (`frontend/src/components/`)

#### `layout/Header.jsx`
- **Purpose**: Global navigation header
- **Contains**:
  - Logo and app name
  - Navigation links
  - Sign In and Get Started buttons (placeholders)
- **Features**:
  - Sticky positioning
  - Responsive design
  - Links to home page
- **Future**: User menu, notifications, search

#### `layout/Footer.jsx`
- **Purpose**: Global footer
- **Contains**:
  - Brand logo and description
  - Link sections (Product, Support)
  - Copyright notice
  - Version display
- **Features**:
  - Multi-column layout
  - Responsive grid
  - Current year auto-update

#### `layout/Layout.jsx`
- **Purpose**: Main layout wrapper
- **Contains**:
  - Header component
  - Main content area (Outlet for routes)
  - Footer component
- **Features**:
  - Flexbox layout (header, content, footer)
  - Consistent page structure
  - React Router Outlet for nested routes

#### `common/.gitkeep`
- **Purpose**: Placeholder for common UI components
- **Future Content**: Buttons, inputs, modals, alerts, loaders, etc.

---

### Assets Directory (`frontend/src/assets/`)

#### `.gitkeep`
- **Purpose**: Ensures directory is tracked by Git
- **Future Content**: Images, icons, fonts, logos

---

### Pages Directory (`frontend/src/pages/`)

#### `Home.jsx`
- **Purpose**: Landing page
- **Contains**:
  - Hero section with welcome message
  - System status card with health check
  - Features preview section
- **Features**:
  - Real-time health check display
  - Automatic health check on page load
  - Manual refresh button
  - Error handling for backend connection
  - Loading states
  - System information display:
    - Overall status badge
    - App name and version
    - Environment
    - Database connection status
    - Last checked timestamp
- **API Integration**: Calls `/api/v1/health` endpoint
- **Design**: Uses Tailwind classes, glassmorphism, animations

---

## 📄 Documentation Files

### `PROJECT_STRUCTURE.md` (This File)
- **Purpose**: Complete project structure documentation
- **Contains**: Detailed explanation of every file and folder
- **Audience**: Developers and project reviewers

---

## 🔄 Data Flow

### Backend Request Flow
```
Client Request
    ↓
FastAPI (main.py)
    ↓
CORS Middleware
    ↓
API Router (api/v1/__init__.py)
    ↓
Route Handler (api/v1/health.py)
    ↓
Database (database.py)
    ↓
Response
```

### Frontend Request Flow
```
User Action
    ↓
React Component (pages/Home.jsx)
    ↓
API Service (services/api.js)
    ↓
Axios Request Interceptor
    ↓
Backend API (http://localhost:8000)
    ↓
Axios Response Interceptor
    ↓
Component State Update
    ↓
UI Re-render
```

---

## 🚀 Running the Project

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your MongoDB URL and JWT secret
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with backend API URL
npm run dev
```

### Access Points
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:5173

---

## 📊 Project Statistics

### Backend
- **Total Files**: 15
- **Lines of Code**: ~800
- **API Endpoints**: 2 (root + health)
- **Dependencies**: 12 main packages

### Frontend
- **Total Files**: 18
- **Lines of Code**: ~1000
- **Components**: 4 (Layout, Header, Footer, Home)
- **Dependencies**: 4 main packages

---

## 🎯 Next Steps

This foundation is complete. Future modules will add:

1. **Authentication Module**
   - User registration and login
   - JWT token generation
   - Password hashing
   - Protected routes

2. **Patient Module**
   - Patient profile management
   - Health records
   - Appointments

3. **Doctor Module**
   - Doctor profiles
   - Appointment management
   - Prescription writing

4. **AI Modules**
   - Symptom checker
   - Document analysis (OCR)
   - AI chat assistant

---

**Document Version**: 1.0  
**Last Updated**: July 3, 2026  
**Status**: ✅ Project Foundation Complete
