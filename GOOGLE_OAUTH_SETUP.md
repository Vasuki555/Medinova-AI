# Google OAuth Setup Guide

## ✅ What's Already Done

### Backend
- ✅ OAuth endpoints created (`/oauth/google/url`, `/oauth/google/callback`)
- ✅ Token exchange logic implemented
- ✅ User creation/linking implemented
- ✅ Config settings added

### Frontend
- ✅ Google callback route added to App.jsx
- ✅ GoogleCallback page created
- ✅ useGoogleAuth hook created
- ✅ Login page updated with Google button
- ✅ Register page updated with Google button
- ✅ AuthContext updated to export setUser/setIsAuthenticated

## 🔧 What You Need to Do

### Option 1: Skip Google OAuth (Use Email/Password Only)
If you don't want Google OAuth right now, you can skip this section entirely. The regular email/password login works perfectly!

### Option 2: Setup Google OAuth (10-15 minutes)

#### Step 1: Get Google OAuth Credentials

1. **Go to Google Cloud Console:**
   ```
   https://console.cloud.google.com/apis/credentials
   ```

2. **Create/Select Project:**
   - Click "Create Project" or select existing
   - Name: "MediNova AI" or any name you like
   - Click "Create"

3. **Enable Google+ API:**
   - Go to "Enable APIs and Services"
   - Search for "Google+ API"
   - Click "Enable"

4. **Create OAuth Consent Screen:**
   - Click "OAuth consent screen" (left menu)
   - User Type: External
   - App name: MediNova AI
   - User support email: your email
   - Developer contact: your email
   - Click "Save and Continue"
   - Scopes: Skip (click "Save and Continue")
   - Test users: Add your Google email
   - Click "Save and Continue"

5. **Create OAuth Client ID:**
   - Click "Credentials" (left menu)
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: **Web application**
   - Name: "MediNova Local Dev"
   
   **Authorized JavaScript origins:**
   ```
   http://localhost:5173
   ```
   
   **Authorized redirect URIs:**
   ```
   http://localhost:5173/auth/google/callback
   ```
   
   - Click "Create"

6. **Copy Credentials:**
   - You'll see a popup with Client ID and Client Secret
   - **IMPORTANT:** Copy both - you'll need them next!

#### Step 2: Configure Backend

Edit `backend/.env`:

```env
# Add these lines (use your actual credentials)
GOOGLE_CLIENT_ID=123456789-abcdefghijklmnop.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your_secret_here
GOOGLE_REDIRECT_URI=http://localhost:5173/auth/google/callback
```

#### Step 3: Restart Backend Server

```bash
# Stop backend (Ctrl+C in terminal)
cd backend
uvicorn app.main:app --reload
```

#### Step 4: Test Google OAuth

1. **Open:** http://localhost:5173/login
2. **Click:** "Sign in with Google" button
3. **Select:** Your Google account
4. **Grant:** Permissions
5. **Expected:** Redirects back to MediNova dashboard
6. **Verify:** You're logged in with your Google profile picture

## 🧪 Testing Google OAuth

### Test 1: New User Registration via Google
```bash
# 1. Open http://localhost:5173/login
# 2. Click "Sign in with Google"
# 3. Select a Google account you've NEVER used with MediNova
# 4. Grant permissions
# 5. Expected: Creates new patient account
# 6. Expected: Redirects to patient dashboard
# 7. Expected: Profile picture shows your Google photo
```

### Test 2: Existing User Login via Google
```bash
# 1. Logout
# 2. Click "Sign in with Google" again
# 3. Select the SAME Google account
# 4. Expected: Logs into existing account (no duplicate)
# 5. Expected: Email matches the Google account
```

### Test 3: Account Linking
```bash
# 1. Register with email: yourname@gmail.com, password: Test123!
# 2. Logout
# 3. Click "Sign in with Google"
# 4. Select the SAME email (yourname@gmail.com)
# 5. Expected: Links Google to existing account
# 6. Expected: Can now login with either method
```

## 🎯 How It Works

### Flow Diagram
```
User clicks "Sign in with Google"
    ↓
Frontend calls: GET /api/v1/oauth/google/url
    ↓
Backend returns Google OAuth URL
    ↓
Frontend redirects to Google
    ↓
User logs in and grants permissions
    ↓
Google redirects to: http://localhost:5173/auth/google/callback?code=...
    ↓
Frontend (GoogleCallback.jsx) runs
    ↓
Frontend calls: POST /api/v1/oauth/google/callback
    ↓
Backend exchanges code for Google access token
    ↓
Backend fetches user info from Google
    ↓
Backend creates/updates user in MongoDB
    ↓
Backend returns MediNova JWT tokens
    ↓
Frontend stores tokens in sessionStorage
    ↓
Frontend redirects to dashboard
```

### What Gets Stored
```javascript
// MongoDB User Document
{
  email: "user@gmail.com",
  first_name: "John",
  last_name: "Doe",
  profile_picture_url: "https://lh3.googleusercontent.com/...",
  oauth_provider: "google",
  oauth_google_id: "1234567890",
  is_email_verified: true,  // Google verifies email
  role: "patient",
  // ... other fields
}
```

## ⚙️ Without Google OAuth Credentials

If you don't configure Google credentials, the system works normally:
- ✅ Regular email/password login works
- ✅ Registration works
- ✅ Password reset works
- ❌ "Sign in with Google" button will show error: "Google OAuth not configured"

## 🐛 Troubleshooting

### Error: "redirect_uri_mismatch"
**Cause:** Redirect URI doesn't match Google Console  
**Fix:**
1. Check Google Console → Credentials
2. Verify redirect URI is EXACTLY: `http://localhost:5173/auth/google/callback`
3. No trailing slash!
4. No extra spaces!

### Error: "Google OAuth not configured"
**Cause:** Backend environment variables not set  
**Fix:**
1. Check `backend/.env` has GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET
2. Values should not be empty
3. Restart backend server

### Error: "Invalid state parameter"
**Cause:** CSRF token mismatch  
**Fix:**
1. Clear browser cache
2. Clear sessionStorage: `sessionStorage.clear()`
3. Try in incognito mode

### Error: "This app isn't verified"
**Cause:** App is in testing mode  
**Fix:**
1. This is normal for development
2. Click "Advanced" → "Go to MediNova AI (unsafe)"
3. This warning only shows in development

### Can't Select Account
**Cause:** Only test users can login  
**Fix:**
1. Go to Google Console → OAuth consent screen
2. Add your email under "Test users"
3. Click "Save"

## 📋 Checklist

### Backend Configuration
- [ ] GOOGLE_CLIENT_ID set in .env
- [ ] GOOGLE_CLIENT_SECRET set in .env
- [ ] GOOGLE_REDIRECT_URI set in .env
- [ ] Backend server restarted

### Google Cloud Console
- [ ] Project created
- [ ] OAuth consent screen configured
- [ ] OAuth Client ID created
- [ ] Redirect URI added: `http://localhost:5173/auth/google/callback`
- [ ] Test user added (your email)

### Frontend Configuration
- [ ] VITE_GOOGLE_REDIRECT_URI in frontend/.env
- [ ] Route added to App.jsx ✅ (Already done)
- [ ] Login page updated ✅ (Already done)
- [ ] Register page updated ✅ (Already done)

### Testing
- [ ] "Sign in with Google" button visible
- [ ] Clicking button redirects to Google
- [ ] Can select Google account
- [ ] Redirects back to MediNova
- [ ] Creates/logs into account
- [ ] Profile picture shows

## 🚀 Quick Commands

### Backend Test
```bash
# Check if OAuth endpoint exists
curl http://localhost:8000/api/v1/oauth/google/url
```

### Frontend Test
```javascript
// Open browser console on login page
// Check if hook is available
console.log(typeof useGoogleAuth);
```

### Check Environment Variables
```bash
# Backend
cd backend
cat .env | grep GOOGLE

# Frontend
cd frontend
cat .env | grep GOOGLE
```

## 🔒 Security Notes

### Development
- OAuth credentials are for localhost only
- Test users can login in dev mode
- No SSL required for localhost

### Production
- ⚠️ Update redirect URI to production domain
- ⚠️ Use HTTPS only (Google requires it)
- ⚠️ Store CLIENT_SECRET in secure vault
- ⚠️ Update authorized origins
- ⚠️ Publish OAuth app (remove test mode)

**Production Redirect URI:**
```
https://yourdomain.com/auth/google/callback
```

## 📚 Summary

| Component | Status | Action Required |
|-----------|--------|-----------------|
| Backend OAuth endpoints | ✅ Done | None |
| Frontend OAuth pages | ✅ Done | None |
| Frontend OAuth hooks | ✅ Done | None |
| Login/Register buttons | ✅ Done | None |
| Google credentials | ⚙️ Optional | Get from Google Console |
| Environment variables | ⚙️ Optional | Add to .env files |

**Without Google OAuth:**
- ✅ Email/password login works perfectly
- ✅ All other features work normally

**With Google OAuth:**
- ✅ Users can login with Google account
- ✅ Profile pictures synced from Google
- ✅ Email automatically verified
- ✅ Faster registration process

---

**Choose your path:**
- **Path A:** Skip Google OAuth → Everything else works fine!
- **Path B:** Setup Google OAuth → Follow steps 1-4 above

**Both paths are valid!** Google OAuth is an enhancement, not a requirement.
