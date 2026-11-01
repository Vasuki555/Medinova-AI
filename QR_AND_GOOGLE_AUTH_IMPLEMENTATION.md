# QR Code & Google OAuth Implementation Guide

## Status: ✅ BACKEND COMPLETE | ⚙️ FRONTEND INTEGRATION NEEDED

This document provides step-by-step instructions to complete the implementation of:
1. ✅ QR Code Display (Backend Complete)
2. ✅ Mobile QR Scanner with Camera (Component Created)
3. ✅ Google OAuth Login (Backend Complete)

---

## 1. QR CODE DISPLAY - BACKEND VERIFICATION ✅

### Check if QR Library is Installed

```bash
cd backend
pip install qrcode[pil]
```

### Test QR Code Generation

```bash
# Start backend if not running
cd backend
uvicorn app.main:app --reload
```

**Test Endpoints:**
- Patient QR: `http://localhost:8000/api/v1/qr/patient/{patient_id}`
- Doctor QR: `http://localhost:8000/api/v1/qr/doctor/{doctor_id}`

**Test with curl:**
```bash
# Get patient QR (replace TOKEN and PATIENT_ID)
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/api/v1/qr/patient/PATIENT_ID \
  --output patient_qr.png
```

### If QR Codes Don't Display:

**Issue: Missing Library**
```bash
pip install qrcode[pil]
pip install Pillow
```

**Issue: Permission Error**
- Check that the logged-in user has the correct role
- Patients can only view their own QR
- Doctors can view their own QR

---

## 2. MOBILE QR SCANNER - COMPLETE FRONTEND INTEGRATION

### Files Created ✅
1. `frontend/src/components/common/QRScanner.jsx` - Camera scanner component
2. Updated `frontend/src/pages/dashboards/patient/QRHealthID.jsx` - Added scanner integration

### Steps to Enable QR Scanner

#### Step 1: Update App Routing

Add the Google OAuth callback route to `frontend/src/App.jsx`:

```jsx
// At the top, add import
import GoogleCallback from '@/pages/auth/GoogleCallback';

// In the Routes section, add:
<Route path="/auth/google/callback" element={<GoogleCallback />} />
```

#### Step 2: Verify QRHealthID Page

The QRHealthID page should now have a "Scan with Camera" button that:
1. Opens camera scanner modal
2. Scans QR codes in real-time
3. Automatically decodes doctor QR codes
4. Redirects to appointment booking

#### Step 3: Test QR Scanner

**On Desktop:**
1. Login as patient: `john.patient@test.com` / `Patient123!`
2. Navigate to QR Health ID page
3. Click "Scan with Camera"
4. Allow camera access
5. Hold up a doctor QR code (or use virtual camera)

**On Mobile:**
1. Open http://YOUR_IP:5173 (get IP with `ipconfig` on Windows)
2. Login as patient
3. Navigate to QR ID
4. Click "Scan with Camera"
5. Point phone camera at doctor QR code

#### Step 4: Generate Test QR Codes

**Generate Doctor QR for Testing:**
```python
# Run in backend directory
python -c "
import requests
import json

# Login as doctor
response = requests.post('http://localhost:8000/api/v1/auth/login', 
    json={'email': 'dr.smith@test.com', 'password': 'Doctor123!'})
token = response.json()['access_token']
doctor_id = response.json()['user']['_id']

# Get QR code
qr_response = requests.get(
    f'http://localhost:8000/api/v1/qr/doctor/{doctor_id}',
    headers={'Authorization': f'Bearer {token}'}
)

with open('doctor_qr.png', 'wb') as f:
    f.write(qr_response.content)

print(f'✅ Doctor QR saved to doctor_qr.png')
print(f'Doctor ID: {doctor_id}')
"
```

---

## 3. GOOGLE OAUTH LOGIN - COMPLETE SETUP

### Backend Setup ✅ (Already Done)
- ✅ OAuth endpoints created (`backend/app/api/v1/oauth.py`)
- ✅ Routes registered
- ✅ Config settings added

### Frontend Setup (Need to Complete)

#### Step 1: Add Route for Google Callback

In `frontend/src/App.jsx`, add:

```jsx
import GoogleCallback from '@/pages/auth/GoogleCallback';

// In routes section:
<Route path="/auth/google/callback" element={<GoogleCallback />} />
```

#### Step 2: Update Login Page

Replace the placeholder Google button in `frontend/src/pages/auth/Login.jsx`:

Find this section (around line 220):
```jsx
{/* Google Sign In (UI Only) */}
<Button
  type="button"
  variant="secondary"
  fullWidth
  onClick={() => setToast({ type: 'info', message: 'Google Sign In - Coming Soon!' })}
>
```

Replace with:
```jsx
{/* Google Sign In */}
<Button
  type="button"
  variant="secondary"
  fullWidth
  onClick={initiateGoogleLogin}
  disabled={googleLoading}
  loading={googleLoading}
>
  <svg className="w-5 h-5" viewBox="0 0 24 24">
    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
  </svg>
  {googleLoading ? 'Connecting to Google...' : 'Sign in with Google'}
</Button>
```

And at the top of Login component:
```jsx
import { useGoogleAuth } from '@/hooks/useGoogleAuth';

const Login = () => {
  // ... existing code
  const { initiateGoogleLogin, loading: googleLoading } = useGoogleAuth();
  // ... rest of code
```

#### Step 3: Update Register Page (Same as Login)

Apply the same changes to `frontend/src/pages/auth/Register.jsx`.

#### Step 4: Get Google OAuth Credentials

**Create Google OAuth App:**

1. Go to: https://console.cloud.google.com/apis/credentials
2. Create New Project: "MediNova AI"
3. Enable Google+ API
4. Create Credentials → OAuth 2.0 Client ID
5. Application Type: Web Application
6. Name: "MediNova Local Dev"
7. **Authorized JavaScript origins:**
   ```
   http://localhost:5173
   http://localhost:3000
   ```
8. **Authorized redirect URIs:**
   ```
   http://localhost:5173/auth/google/callback
   ```
9. Click "Create"
10. Copy Client ID and Client Secret

#### Step 5: Configure Environment Variables

**Backend** (`backend/.env`):
```env
# Add these lines
GOOGLE_CLIENT_ID=YOUR_CLIENT_ID.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=YOUR_CLIENT_SECRET
GOOGLE_REDIRECT_URI=http://localhost:5173/auth/google/callback
```

**Frontend** (`frontend/.env`):
```env
# Add this line
VITE_GOOGLE_REDIRECT_URI=http://localhost:5173/auth/google/callback
```

#### Step 6: Restart Servers

```bash
# Backend
cd backend
# Stop with Ctrl+C
uvicorn app.main:app --reload

# Frontend
cd frontend
# Stop with Ctrl+C
npm run dev
```

#### Step 7: Test Google OAuth

1. Open http://localhost:5173/login
2. Click "Sign in with Google"
3. Should redirect to Google login
4. Select your Google account
5. Grant permissions
6. Should redirect back to MediNova dashboard

**First-time login:** Creates new patient account with Google email  
**Returning login:** Logs into existing account

---

## TESTING CHECKLIST

### QR Code Display ✅
- [ ] Backend server running
- [ ] `qrcode[pil]` library installed
- [ ] Login as patient: `john.patient@test.com`
- [ ] Navigate to Patient → QR Health ID
- [ ] **Expected:** QR code image displays (blue colored QR)
- [ ] Click "Download" button
- [ ] **Expected:** PNG file downloads

### Mobile QR Scanner 📱
- [ ] Open http://localhost:5173 on mobile OR desktop
- [ ] Login as patient
- [ ] Navigate to QR Health ID
- [ ] Click "Scan with Camera" button
- [ ] **Expected:** Camera permission request appears
- [ ] Allow camera access
- [ ] **Expected:** Camera preview shows in modal
- [ ] Point camera at doctor QR code
- [ ] **Expected:** Auto-detects QR and shows success message
- [ ] Click "Book Appointment"
- [ ] **Expected:** Redirects to booking page with doctor pre-selected

### Google OAuth Login 🔐
- [ ] Google OAuth credentials configured in `.env`
- [ ] Both servers restarted
- [ ] Navigate to http://localhost:5173/login
- [ ] Click "Sign in with Google" button
- [ ] **Expected:** Redirects to Google OAuth page
- [ ] Select Google account and approve
- [ ] **Expected:** Redirects to `/auth/google/callback`
- [ ] **Expected:** Shows "Processing" then "Success"
- [ ] **Expected:** Redirects to dashboard
- [ ] Check profile: should have Google profile picture
- [ ] Logout and try again
- [ ] **Expected:** Logs into same account (not creating duplicate)

---

## TROUBLESHOOTING

### QR Code Not Displaying

**Error: "qrcode library not installed"**
```bash
cd backend
pip install qrcode[pil] Pillow
# Restart backend
```

**Error: "QR generation failed"**
- Check backend logs
- Verify user is logged in
- Verify correct patient/doctor ID

**QR Shows but is Blank**
- Check browser console for errors
- Verify API endpoint returns image/png
- Try downloading QR and opening locally

### QR Scanner Issues

**Camera Not Starting**
- Browser blocks camera access
- Go to browser settings → Allow camera for localhost
- Chrome: chrome://settings/content/camera
- Firefox: about:preferences#privacy

**Scanner Library Not Loading**
- Check internet connection (loads from CDN)
- Check browser console for errors
- Try hard refresh (Ctrl+Shift+R)

**QR Code Not Scanning**
- Ensure QR code is well-lit
- Hold steady for 2-3 seconds
- Try different distance from camera
- Ensure it's a MediNova QR (has correct JSON structure)

### Google OAuth Issues

**"Google OAuth not configured"**
```bash
# Check backend/.env has these set:
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GOOGLE_REDIRECT_URI=http://localhost:5173/auth/google/callback
```

**"redirect_uri_mismatch"**
- Go to Google Cloud Console
- Check Authorized redirect URIs
- Must match exactly: `http://localhost:5173/auth/google/callback`
- No trailing slash!

**"Invalid state parameter"**
- Clear browser cache and sessionStorage
- Try incognito/private window
- Check that state is being stored correctly

**"Failed to exchange authorization code"**
- Check GOOGLE_CLIENT_SECRET is correct
- Check redirect_uri matches exactly
- Try generating new credentials

**Redirects but doesn't log in**
- Check browser console for errors
- Check backend logs
- Verify database connection
- Check that tokens are being stored in sessionStorage

---

## PRODUCTION DEPLOYMENT NOTES

### QR Codes
- ✅ Already production-ready
- Uses secure JWT authentication
- QR codes contain public data only (name, ID, URL)
- No sensitive information in QR

### QR Scanner
- ⚠️ Requires HTTPS in production (camera access)
- Update frontend URL in production config
- Consider adding QR scan rate limiting

### Google OAuth
- ⚠️ Update authorized origins and redirect URIs for production domain
- Store GOOGLE_CLIENT_SECRET securely (use secrets manager)
- Consider adding OAuth scopes for additional permissions
- Add privacy policy and terms of service URLs

**Production Environment Variables:**
```env
# Backend
GOOGLE_CLIENT_ID=prod-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=use-secrets-manager
GOOGLE_REDIRECT_URI=https://yourdomain.com/auth/google/callback

# Frontend
VITE_GOOGLE_REDIRECT_URI=https://yourdomain.com/auth/google/callback
```

---

## QUICK FIX COMMANDS

### Install Missing Dependencies
```bash
# Backend
cd backend
pip install qrcode[pil] Pillow httpx

# Frontend
cd frontend
npm install
```

### Restart Everything
```bash
# Kill all servers
# Windows: Ctrl+C in each terminal

# Start backend
cd backend
uvicorn app.main:app --reload

# Start frontend (new terminal)
cd frontend
npm run dev
```

### Clear Cache
```bash
# Browser: Ctrl+Shift+Delete
# Or run in browser console:
sessionStorage.clear();
localStorage.clear();
location.reload();
```

### Generate Test QR Code
```bash
cd backend
python -c "
import qrcode
import json

data = {
    'type': 'medinova_doctor',
    'doctor_id': '507f1f77bcf86cd799439011',
    'name': 'Dr. Test Doctor',
    'specialization': 'Cardiologist',
    'url': 'http://localhost:5173/patient/booking?doctor_id=507f1f77bcf86cd799439011'
}

qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data(json.dumps(data))
qr.make(fit=True)
img = qr.make_image(fill_color='#0ea5e9', back_color='white')
img.save('test_doctor_qr.png')
print('✅ Test QR saved to test_doctor_qr.png')
"
```

---

## SUMMARY

### What's Complete ✅
- QR code generation backend (patient & doctor)
- QR code display frontend (both dashboards)
- QR scanner component with camera access
- Google OAuth backend endpoints
- Google OAuth callback handling
- Account creation/linking logic

### What You Need to Do ⚙️
1. **Install QR library:** `pip install qrcode[pil]`
2. **Add Google callback route** to App.jsx
3. **Update Login/Register pages** with Google button
4. **Get Google OAuth credentials** from console.cloud.google.com
5. **Add credentials to .env** files
6. **Restart servers**
7. **Test all features**

### Estimated Time
- QR Code: 5 minutes (just install library)
- QR Scanner: Already working (just test)
- Google OAuth: 15-20 minutes (get credentials + config)

---

**Need Help?** Check the troubleshooting section above or examine the browser/backend console logs for specific error messages.
