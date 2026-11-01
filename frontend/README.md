# MediNova AI - Frontend

React frontend for the MediNova AI healthcare platform.

## 🚀 Quick Start

### Prerequisites

- Node.js 18 or higher
- npm or yarn

### Installation

1. **Install dependencies**

```bash
npm install
```

2. **Configure environment variables**

```bash
copy .env.example .env
```

Edit `.env` and configure:
- `VITE_API_BASE_URL` - Backend API URL (default: http://localhost:8000/api/v1)

3. **Run development server**

```bash
npm run dev
```

The application will be available at: `http://localhost:5173`

## 📁 Project Structure

```
frontend/
├── public/                      # Static assets
│   └── vite.svg
│
├── src/
│   ├── assets/                  # Images, fonts (future)
│   │
│   ├── components/              # Reusable components
│   │   ├── common/              # Common UI components (future)
│   │   └── layout/              # Layout components
│   │       ├── Header.jsx       # Global header with navigation
│   │       ├── Footer.jsx       # Global footer
│   │       └── Layout.jsx       # Main layout wrapper
│   │
│   ├── pages/                   # Page components
│   │   └── Home.jsx             # Landing page with health check
│   │
│   ├── services/                # API services
│   │   └── api.js               # Axios configuration and API methods
│   │
│   ├── utils/                   # Utility functions
│   │   └── constants.js         # Application constants
│   │
│   ├── App.jsx                  # Root component with routes
│   ├── main.jsx                 # Application entry point
│   └── index.css                # Global styles with Tailwind
│
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── eslint.config.js             # ESLint configuration
├── index.html                   # HTML template
├── package.json                 # Dependencies and scripts
├── postcss.config.js            # PostCSS configuration
├── tailwind.config.js           # Tailwind CSS configuration
├── vite.config.js               # Vite configuration
└── README.md                    # This file
```

## 🎨 Design System

The application uses a custom design system based on:
- **Primary Color**: Medical Blue (#2E90FA)
- **Font Family**: Inter (body), Manrope (headings), JetBrains Mono (code)
- **Design Pattern**: Glassmorphism
- **Accessibility**: WCAG 2.1 AA compliant

### Color Palette

```javascript
// Primary (Medical Blue)
primary-50  to primary-900

// Neutral (Grays)
neutral-50 to neutral-900

// Status Colors
success: #10B981
warning: #F59E0B
error: #EF4444
```

### Custom CSS Classes

```css
/* Buttons */
.btn-primary         /* Primary button */
.btn-secondary       /* Secondary button */

/* Cards */
.glass-card          /* Glassmorphism card */
.card                /* Standard card */

/* Inputs */
.input-field         /* Form input field */
```

## 📚 Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run ESLint
npm run lint

# Format code with Prettier
npm run format
```

## 🔌 API Integration

The frontend connects to the FastAPI backend through Axios.

### API Service Usage

```javascript
import { apiService, healthAPI } from '@/services/api';

// Health check
const status = await healthAPI.check();

// Generic API calls
const data = await apiService.get('/endpoint');
const result = await apiService.post('/endpoint', { data });
```

### API Configuration

- **Base URL**: Configured via `VITE_API_BASE_URL` environment variable
- **Timeout**: 30 seconds
- **Authentication**: JWT tokens (automatically added to requests)
- **Error Handling**: Automatic error logging and 401 redirect

## 🧪 Testing the Application

1. **Start the backend server**
```bash
cd ../backend
uvicorn app.main:app --reload
```

2. **Start the frontend server**
```bash
npm run dev
```

3. **Open browser**
```
http://localhost:5173
```

4. **Verify health check**
- The home page should display system status
- Green checkmark indicates successful connection
- If connection fails, verify backend is running

## 🔧 Configuration Files

### `vite.config.js`
- React plugin configuration
- Path aliases (`@/` for `src/`)
- Proxy configuration for API calls
- Build optimization

### `tailwind.config.js`
- Custom color palette
- Font families
- Custom spacing
- Component utilities

### `eslint.config.js`
- React linting rules
- Code quality standards

## 📱 Responsive Design

The application is fully responsive:
- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

Uses mobile-first approach with Tailwind breakpoints.

## 🎯 Current Features

- ✅ Project foundation setup
- ✅ Responsive header and footer
- ✅ Landing page with hero section
- ✅ Health check integration
- ✅ System status display
- ✅ Features preview section

## 🔜 Next Steps

Future modules will add:
- Authentication pages (Login, Register)
- Patient dashboard
- Doctor dashboard
- Appointment booking
- Symptom checker interface
- Document upload
- And more...

## 🛠️ Development Guidelines

### Component Structure
```javascript
/**
 * Component Name
 * Brief description
 */

import { useState } from 'react';

const ComponentName = ({ prop1, prop2 }) => {
  // State and logic
  
  return (
    // JSX
  );
};

export default ComponentName;
```

### File Naming
- Components: PascalCase (e.g., `Header.jsx`)
- Utilities: camelCase (e.g., `constants.js`)
- Styles: kebab-case (e.g., `global-styles.css`)

### Import Order
1. React and third-party libraries
2. Components
3. Services and utilities
4. Styles

## 📝 License

Academic project - Final Year Engineering

## 🤝 Contributing

This is an academic project. Internal team only.
