# Multi-Tab Feature - Testing Instructions

## 🎯 Quick Test Scenario

Follow these exact steps to test the multi-tab feature:

---

## Step 1: Patient Dashboard (Tab 1)

1. **Open your browser** (Chrome, Edge, Firefox)
2. **Navigate to:** http://localhost:5173/login
3. **Login with:**
   - Email: `john.patient@test.com`
   - Password: `Patient123!`
4. **Verify:** You see the Patient Dashboard
5. **Keep this tab open!**

---

## Step 2: Doctor Dashboard (Tab 2)

1. **Open a NEW TAB** (Ctrl+T or Cmd+T)
2. **Navigate to:** http://localhost:5173/login
3. **Login with:**
   - Email: `dr.smith@test.com`
   - Password: `Doctor123!`
4. **Verify:** You see the Doctor Dashboard
5. **Important:** Check that Tab 1 is still logged in as Patient!

---

## Step 3: Admin Dashboard (Tab 3)

1. **Open another NEW TAB** (Ctrl+T or Cmd+T)
2. **Navigate to:** http://localhost:5173/login
3. **Login with:**
   - Email: `admin@medinova.com`
   - Password: `Admin123!`
4. **Verify:** You see the Admin Dashboard
5. **Important:** Check that Tabs 1 & 2 are still logged in!

---

## ✅ Success Criteria

You should now have **3 tabs open simultaneously:**

```
Tab 1: 👤 Patient Dashboard (john.patient@test.com)
  └─ Shows: Patient home, appointments, health records, QR code

Tab 2: 🩺 Doctor Dashboard (dr.smith@test.com)
  └─ Shows: Doctor home, patient queue, schedule, QR code

Tab 3: ⚙️  Admin Dashboard (admin@medinova.com)
  └─ Shows: Admin console, user management, verifications
```

**Switch between tabs** - each should maintain its own session!

---

## 🧪 Additional Tests

### Test 1: Independent Sessions
1. In Tab 1 (Patient): Navigate to "QR Health ID"
2. In Tab 2 (Doctor): Navigate to "My QR Code"
3. In Tab 3 (Admin): Navigate to "Platform Users"
4. **Verify:** Each tab works independently

### Test 2: Logout in One Tab
1. In Tab 2 (Doctor): Click logout
2. **Verify:** Tab 2 goes to login page
3. **Verify:** Tab 1 (Patient) is still logged in
4. **Verify:** Tab 3 (Admin) is still logged in
5. **Success:** Only the logged-out tab was affected!

### Test 3: Refresh Tab
1. Refresh Tab 1 (F5)
2. **Expected:** You'll need to login again in Tab 1
3. **Reason:** sessionStorage is cleared on refresh
4. **Verify:** Tabs 2 & 3 are still logged in

### Test 4: Close and Reopen Tab
1. Close Tab 1 completely
2. Open new tab and go to http://localhost:5173
3. **Expected:** You see login page
4. **Reason:** sessionStorage was cleared when tab closed
5. **Verify:** Tabs 2 & 3 are still logged in

---

## 🎭 Real-World Test Scenario

**Scenario:** Patient books appointment, Doctor sees and manages it

### Patient Side (Tab 1):
```
1. Login as: john.patient@test.com
2. Go to: "Book Appointment"
3. Select: Dr. Smith
4. Choose: Tomorrow, 10:00 AM
5. Add reason: "Annual checkup"
6. Submit appointment
```

### Doctor Side (Tab 2):
```
1. Already logged in as: dr.smith@test.com
2. Go to: "Patient Queue"
3. Should see: John Doe's appointment
4. Click: View details
5. Update status: Confirmed
```

### Admin Monitoring (Tab 3):
```
1. Already logged in as: admin@medinova.com
2. Go to: "Platform Users"
3. See: Both john.patient@test.com and dr.smith@test.com
4. Monitor: System activity
```

**Test complete workflow without switching accounts!** 🎉

---

## 🔧 Troubleshooting

### Problem: Second login logs out first tab
**Cause:** Multi-tab mode might be disabled
**Fix:**
```javascript
// Open browser console (F12), run:
localStorage.setItem('multiTabEnabled', 'true');
// Then refresh all tabs and try again
```

### Problem: Can't login in new tab
**Cause:** Frontend might not be running
**Fix:**
```bash
cd frontend
npm run dev
```

### Problem: Backend API errors
**Cause:** Backend might not be running
**Fix:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Problem: All tabs showing same dashboard
**Cause:** Browser cache issue
**Fix:**
1. Clear browser cache (Ctrl+Shift+Delete)
2. Or use Incognito/Private mode
3. Try again with fresh tabs

---

## 📊 Visual Test Checklist

- [ ] Tab 1: Patient dashboard displays correctly
- [ ] Tab 2: Doctor dashboard displays correctly
- [ ] Tab 3: Admin dashboard displays correctly
- [ ] Can switch between tabs without issues
- [ ] Each tab maintains independent session
- [ ] Logout in one tab doesn't affect others
- [ ] Can navigate within each dashboard independently
- [ ] QR codes display correctly in each role
- [ ] Notifications work per tab
- [ ] Dark mode toggle works per tab

---

## 🎉 Success!

If all tests pass, you have successfully:
- ✅ Enabled multi-tab dashboard support
- ✅ Can test multiple user roles simultaneously
- ✅ Can compare different user experiences side-by-side
- ✅ Improved development and testing workflow

---

## 💡 Use Cases

### For Development:
- Test patient-doctor interactions in real-time
- Compare UI across different roles
- Debug role-specific features
- Verify access control

### For Demos:
- Show patient view and doctor view simultaneously
- Demonstrate real-time updates
- Display different role capabilities
- Impress stakeholders! 😎

### For Testing:
- End-to-end workflow testing
- Multi-user scenario testing
- Concurrent session testing
- Role-based access testing

---

## 📝 Notes

- **sessionStorage is temporary** - cleared when tab closes
- **Each tab is isolated** - no cross-tab interference
- **Default behavior** - multi-tab mode is enabled by default
- **No backend changes** - all changes are frontend-only
- **Fully compatible** - works with existing authentication system

---

**Test Date:** September 7, 2026
**Feature Status:** ✅ Ready for Testing
**Recommended:** Test all scenarios before production deployment
