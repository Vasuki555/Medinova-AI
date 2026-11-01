# MediNova AI — Quick Start Guide

## ✅ Current Status: FULLY OPERATIONAL

Both backend and frontend are running successfully!

---

## 🚀 Start the Application

### 1. Start Backend (Port 8000)
```powershell
cd C:\Users\vasuk\OneDrive\Desktop\MediNova\backend
.\start_backend.ps1
```

### 2. Start Frontend (Port 5173)
```powershell
cd C:\Users\vasuk\OneDrive\Desktop\MediNova\frontend
npm run dev
```

### 3. Open Application
- **Frontend:** http://localhost:5173
- **API Docs:** http://localhost:8000/docs

---

## 🔑 Test Authentication

### Registration
1. Go to: http://localhost:5173/register
2. Fill form and submit
3. Should redirect to dashboard

### Login
1. Go to: http://localhost:5173/login
2. Enter credentials
3. Should redirect to dashboard

---

## ⚠️ Important Note

**Database Status:** Currently using **in-memory mock database**
- ✅ All features work
- ⚠️ Data lost on backend restart
- 🔧 Fix: Whitelist your IP in MongoDB Atlas (see DEPLOYMENT_STATUS_REPORT.md)

---

## 🐛 Troubleshooting

### Backend won't start?
- Ensure Python 3.11 virtual environment is active
- Check if port 8000 is free

### Frontend won't start?
- Ensure `node_modules` exist (run `npm install` if needed)
- Check if port 5173 is free

### Registration fails?
- Check backend is running (http://localhost:8000/api/v1/health)
- Open browser console (F12) for error messages

---

## 📚 Documentation

For detailed information, see:
- **DEPLOYMENT_STATUS_REPORT.md** - Full deployment details
- **BUG_FIX_STATUS.md** - All bugs that were fixed
- **backend/README.md** - Backend API documentation
- **frontend/README.md** - Frontend setup guide

---

## ✨ What's Working

- ✅ User Registration
- ✅ User Login
- ✅ JWT Authentication
- ✅ Protected Routes
- ✅ Role-based Access (Patient/Doctor/Admin)
- ✅ Auto-profile Creation
- ✅ Password Hashing
- ✅ Token Refresh

---

## 🎯 Next Steps

1. **Enable MongoDB Atlas:**
   - Whitelist IP in Atlas dashboard
   - Restart backend
   - Data will persist

2. **Test All Features:**
   - Register as patient
   - Register as doctor
   - Test login
   - Access dashboards

3. **Continue Development:**
   - All modules ready
   - APIs documented at http://localhost:8000/docs

---

**Ready to use!** 🎉
