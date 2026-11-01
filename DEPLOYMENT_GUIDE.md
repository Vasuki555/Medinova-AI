# MediNova AI - Deployment Guide

This guide walks you through deploying MediNova AI to production using **Vercel (Frontend)** and **Render (Backend)**.

## 🎯 Architecture

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │         │                 │
│  Vercel         │────────▶│  Render         │────────▶│  MongoDB Atlas  │
│  (Frontend)     │   API   │  (Backend)      │   Data  │  (Database)     │
│                 │         │                 │         │                 │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

---

## 📋 Prerequisites

Before deploying, ensure you have:

- ✅ GitHub account (your code is already pushed)
- ✅ Vercel account (free: https://vercel.com/signup)
- ✅ Render account (free: https://render.com/register)
- ✅ MongoDB Atlas account (free: https://www.mongodb.com/cloud/atlas/register)
- ✅ Google Cloud Console project (for OAuth & Gemini API)
- ✅ Gmail/SMTP credentials for email

---

## 🗄️ Step 1: Set Up MongoDB Atlas (Database)

### 1.1 Create Cluster
1. Go to https://cloud.mongodb.com
2. Sign in or create account
3. Click **"Build a Database"**
4. Select **FREE** tier (M0)
5. Choose region closest to your users
6. Click **"Create"**

### 1.2 Configure Network Access
1. In MongoDB Atlas, go to **Network Access**
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (0.0.0.0/0)
   - For production, you can restrict this to Render's IP ranges later
4. Click **"Confirm"**

### 1.3 Create Database User
1. Go to **Database Access**
2. Click **"Add New Database User"**
3. Choose **Password** authentication
4. Username: `medinova_admin`
5. Generate secure password (save it!)
6. Built-in Role: **"Atlas admin"** (or Read and write to any database)
7. Click **"Add User"**

### 1.4 Get Connection String
1. Go to **Database** → **Connect**
2. Click **"Connect your application"**
3. Driver: **Python**, Version: **3.11 or later**
4. Copy the connection string (looks like):
   ```
   mongodb+srv://medinova_admin:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
5. Replace `<password>` with your actual password
6. Add database name before the `?`:
   ```
   mongodb+srv://medinova_admin:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/medinova_ai?retryWrites=true&w=majority&appName=Cluster0
   ```

**Save this connection string** - you'll need it for Render!

---

## 🚀 Step 2: Deploy Backend to Render

### 2.1 Create Web Service
1. Go to https://render.com/dashboard
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select repository: **`Medinova-AI`**
5. Click **"Connect"**

### 2.2 Configure Service
**Basic Settings:**
- **Name**: `medinova-backend`
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Runtime**: **Python 3**
- **Build Command**:
  ```bash
  cd backend && pip install -r requirements.txt
  ```
- **Start Command**:
  ```bash
  cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

**Instance Type:**
- Select **Free** (spins down after 15 min inactivity)
- Or **Starter** ($7/month) for always-on service

### 2.3 Add Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**

Add these variables one by one:

```bash
# Application
ENVIRONMENT=production
HOST=0.0.0.0
DEBUG=False
LOG_LEVEL=INFO

# MongoDB (use your connection string from Step 1.4)
MONGODB_URL=mongodb+srv://medinova_admin:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/medinova_ai?retryWrites=true&w=majority&appName=Cluster0
MONGODB_DB_NAME=medinova_ai

# JWT Secrets (generate using: python -c "import secrets; print(secrets.token_urlsafe(64))")
JWT_SECRET_KEY=GENERATE_A_RANDOM_64_CHARACTER_STRING
JWT_REFRESH_SECRET_KEY=GENERATE_A_DIFFERENT_RANDOM_64_CHARACTER_STRING
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS (update after deploying frontend - for now use *)
CORS_ORIGINS=*
CORS_ALLOW_CREDENTIALS=True

# Frontend URL (update after deploying frontend)
FRONTEND_URL=https://your-app.vercel.app

# AI API Keys
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

# Google OAuth (from Google Cloud Console)
GOOGLE_CLIENT_ID=YOUR_CLIENT_ID.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=YOUR_CLIENT_SECRET
GOOGLE_REDIRECT_URI=https://your-app.vercel.app/auth/google/callback

# Email (Gmail example)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
SMTP_FROM_EMAIL=noreply@medinova.ai
SMTP_FROM_NAME=MediNova AI

# File Uploads
UPLOAD_DIR=/var/data/uploads
MAX_UPLOAD_SIZE_MB=50

# Rate Limiting (use memory for free tier, Redis for paid)
RATE_LIMIT_ENABLED=True
REDIS_URL=memory://
```

### 2.4 Deploy
1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Once deployed, you'll get a URL like: `https://medinova-backend.onrender.com`
4. **Save this URL** - you'll need it for frontend!

### 2.5 Test Backend
Visit: `https://medinova-backend.onrender.com/api/v1/health`

You should see:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "..."
}
```

---

## 🎨 Step 3: Deploy Frontend to Vercel

### 3.1 Update API URL in Frontend
First, update your frontend to use the Render backend URL:

1. Create `frontend/.env.production`:
   ```bash
   VITE_API_BASE_URL=https://medinova-backend.onrender.com
   ```

2. Commit and push:
   ```bash
   git add frontend/.env.production
   git commit -m "Add production API URL"
   git push origin main
   ```

### 3.2 Deploy to Vercel
1. Go to https://vercel.com/new
2. Click **"Import Git Repository"**
3. Select **`Medinova-AI`**
4. Click **"Import"**

### 3.3 Configure Project
**Framework Preset:** Vite
**Root Directory:** `frontend`
**Build Command:**
```bash
npm run build
```
**Output Directory:**
```
dist
```

### 3.4 Add Environment Variables
Click **"Environment Variables"**:

```bash
VITE_API_BASE_URL=https://medinova-backend.onrender.com
```

### 3.5 Deploy
1. Click **"Deploy"**
2. Wait for deployment (2-5 minutes)
3. Once deployed, you'll get a URL like: `https://medinova-ai.vercel.app`

---

## 🔧 Step 4: Update Backend with Frontend URL

### 4.1 Update Render Environment Variables
Go back to Render dashboard:

1. Select your backend service
2. Go to **"Environment"**
3. Update these variables:

```bash
CORS_ORIGINS=https://medinova-ai.vercel.app
FRONTEND_URL=https://medinova-ai.vercel.app
GOOGLE_REDIRECT_URI=https://medinova-ai.vercel.app/auth/google/callback
```

4. Click **"Save Changes"**
5. Service will automatically redeploy

### 4.2 Update Google OAuth
1. Go to https://console.cloud.google.com/apis/credentials
2. Select your OAuth 2.0 Client
3. Under **"Authorized redirect URIs"**, add:
   ```
   https://medinova-ai.vercel.app/auth/google/callback
   ```
4. Click **"Save"**

---

## ✅ Step 5: Test Your Deployment

### 5.1 Test Backend
Visit: `https://medinova-backend.onrender.com/docs`
- Should see FastAPI interactive docs

### 5.2 Test Frontend
Visit: `https://medinova-ai.vercel.app`
- Should see login page
- Try registering a new account
- Try logging in
- Test all features

---

## 🔒 Step 6: Security Hardening (Production)

### 6.1 MongoDB IP Whitelist
1. In MongoDB Atlas → **Network Access**
2. Remove `0.0.0.0/0`
3. Add Render's IP ranges or use VPC peering

### 6.2 Enable HTTPS Only
Both Vercel and Render provide free SSL certificates automatically!

### 6.3 Set Up Monitoring
**Render:**
- Enable **"Log Streams"** for real-time logs
- Set up **"Notifications"** for deployment failures

**Vercel:**
- Check **"Analytics"** for performance metrics
- Review **"Logs"** for errors

---

## 💰 Costs

### Free Tier (Total: $0/month)
- **Vercel**: Free (commercial projects allowed)
- **Render**: Free (backend sleeps after 15 min inactivity)
- **MongoDB Atlas**: Free (M0 cluster, 512MB storage)

**Limitations:**
- Backend cold starts (first request after sleep takes ~30 seconds)
- 512MB database storage limit
- No custom domain on free tier

### Paid Tier (Total: ~$12/month)
- **Vercel Pro**: $20/month (optional, custom domain + analytics)
- **Render Starter**: $7/month (always-on, no cold starts)
- **MongoDB M10**: $0.08/hour (~$57/month for production workloads)

---

## 🐛 Troubleshooting

### Backend not starting
- Check Render logs for errors
- Verify MongoDB connection string is correct
- Ensure all required environment variables are set

### Frontend can't connect to backend
- Check CORS_ORIGINS includes your Vercel URL
- Verify VITE_API_BASE_URL is correct
- Check browser console for CORS errors

### Google OAuth not working
- Verify redirect URI matches exactly in Google Console
- Check GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET are correct
- Ensure frontend URL is whitelisted in Google Console

### Database connection errors
- Check MongoDB Atlas IP whitelist
- Verify connection string has correct password
- Ensure database user has proper permissions

---

## 📞 Support

If you encounter issues:
1. Check Render logs: Dashboard → Service → Logs
2. Check Vercel logs: Dashboard → Project → Deployments → [Latest] → Logs
3. Check MongoDB Atlas logs: Monitoring → Logs

---

## 🎉 Congratulations!

Your MediNova AI application is now live! 

**Next Steps:**
- Set up custom domain (optional)
- Configure monitoring and alerts
- Set up automated backups for MongoDB
- Enable rate limiting with Redis (for production traffic)
- Set up CI/CD for automated deployments

---

## 📝 Quick Reference

**Your URLs:**
- Frontend: `https://medinova-ai.vercel.app`
- Backend: `https://medinova-backend.onrender.com`
- Backend API Docs: `https://medinova-backend.onrender.com/docs`
- Backend Health Check: `https://medinova-backend.onrender.com/api/v1/health`

**Deployment Commands:**
```bash
# Push changes to deploy automatically
git add .
git commit -m "Update: description"
git push origin main

# Both Vercel and Render will auto-deploy!
```
