# Multi-Tab Dashboard Support

## ✨ New Feature: Multiple Dashboards in Different Tabs

You can now login with **different user accounts simultaneously** in different browser tabs!

---

## 🎯 How It Works

### Default Behavior: Multi-Tab Mode (ENABLED)
- **Each browser tab has its own independent session**
- You can login as a Patient in Tab 1, Doctor in Tab 2, Admin in Tab 3
- Sessions don't interfere with each other
- Uses `sessionStorage` (tab-specific storage)

### Alternative: Single-Session Mode (DISABLED)
- Traditional behavior where all tabs share the same login
- Logging in with a different account in another tab logs you out everywhere
- Uses `localStorage` (shared across all tabs)

---

## 🚀 Usage Examples

### Example 1: Test Multiple Roles Simultaneously
```
Tab 1: http://localhost:5173/login
  → Login as: john.patient@test.com (Patient)
  → Dashboard: Patient Dashboard

Tab 2: http://localhost:5173/login (new tab)
  → Login as: dr.smith@test.com (Doctor)
  → Dashboard: Doctor Dashboard

Tab 3: http://localhost:5173/login (new tab)
  → Login as: admin@medinova.com (Admin)
  → Dashboard: Admin Dashboard

All three sessions work independently! ✅
```

### Example 2: Compare Patient Views
```
Tab 1: Login as john.patient@test.com
Tab 2: Login as sarah.patient@test.com
Tab 3: Login as mike.patient@test.com

Compare different patient data side-by-side!
```

---

## 🔧 How to Toggle Multi-Tab Mode

### Method 1: Browser Console
Open browser console (F12) and run:

```javascript
// Enable multi-tab mode (default)
localStorage.setItem('multiTabEnabled', 'true');
// Then refresh the page

// Disable multi-tab mode (single session)
localStorage.setItem('multiTabEnabled', 'false');
// Then refresh the page
```

### Method 2: Manual Storage Edit
1. Open DevTools (F12)
2. Go to "Application" tab
3. Click "Local Storage" → http://localhost:5173
4. Set key: `multiTabEnabled` = `true` or `false`
5. Refresh the page

---

## 📊 Session Comparison

| Feature | Multi-Tab Mode (Enabled) | Single-Session Mode (Disabled) |
|---------|-------------------------|-------------------------------|
| **Storage** | sessionStorage (tab-specific) | localStorage (shared) |
| **Multiple Logins** | ✅ Yes - different accounts per tab | ❌ No - one account across all tabs |
| **Session Persistence** | Lost when tab closes | Persists across browser restarts |
| **Use Case** | Testing, comparing accounts | Normal user experience |
| **Default** | ✅ YES | No |

---

## 🧪 Testing Scenarios

### Scenario 1: Patient + Doctor Workflow
```
Tab 1 (Patient): john.patient@test.com
  • Book appointment with Dr. Smith
  • View QR Health ID
  • Check health records

Tab 2 (Doctor): dr.smith@test.com  
  • See appointment from John in queue
  • View patient profile via QR scan
  • Update appointment status

Test the complete workflow without switching logins!
```

### Scenario 2: Admin Monitoring
```
Tab 1 (Patient): Testing patient features
Tab 2 (Doctor): Testing doctor features  
Tab 3 (Admin): admin@medinova.com
  • Monitor all users
  • Verify doctor credentials
  • View system-wide notifications
```

---

## 🔐 Security Notes

1. **sessionStorage is cleared when tab closes**
   - Multi-tab sessions are temporary
   - Good for security - no persistent sessions

2. **Each tab is isolated**
   - Tokens stored per tab
   - No cross-tab interference

3. **API calls use correct token**
   - Automatically uses the token from current tab
   - No manual configuration needed

---

## 💡 Tips

### For Development/Testing
- ✅ Keep multi-tab mode **ENABLED** (default)
- Open multiple tabs to test different user roles
- Compare UIs side-by-side

### For Production/End Users
- Consider **DISABLING** multi-tab mode
- Users typically don't need multiple simultaneous logins
- Provides more traditional web app experience

---

## 🐛 Troubleshooting

### Problem: Login doesn't work in new tab
**Solution:** Check if `multiTabEnabled` is set correctly:
```javascript
console.log(localStorage.getItem('multiTabEnabled'));
// Should show: "true" for multi-tab mode
```

### Problem: All tabs logout when I logout in one tab
**Expected behavior in single-session mode**
- If `multiTabEnabled = false`, this is normal
- Set to `true` to enable independent sessions

### Problem: Session lost when I refresh
**Expected in multi-tab mode**
- sessionStorage is cleared on tab close
- Re-login required after refresh
- Use single-session mode for persistence

---

## 📝 Implementation Details

### Files Modified:
1. `frontend/src/context/AuthContext.jsx`
   - Added multi-tab support with sessionStorage
   - Added `toggleMultiTabMode()` function
   - Storage selection based on `multiTabEnabled` preference

2. `frontend/src/services/api.js`
   - Updated token reading to check correct storage
   - Helper functions: `getToken()`, `clearTokens()`
   - Works seamlessly with both storage modes

### Technical Details:
- **sessionStorage**: Unique per tab, cleared on tab close
- **localStorage**: Shared across tabs, persists across browser restarts
- **Storage selection**: Based on `localStorage.getItem('multiTabEnabled')`
- **Default**: Multi-tab mode enabled (`multiTabEnabled` defaults to `true`)

---

## 🎉 Benefits

### For Developers:
- ✅ Test multiple user roles simultaneously
- ✅ Debug cross-role interactions
- ✅ Compare UI variations
- ✅ Faster development workflow

### For QA/Testing:
- ✅ Test patient-doctor workflows end-to-end
- ✅ Verify role-based access control
- ✅ Test concurrent user scenarios
- ✅ Reproduce multi-user bugs

### For Demos:
- ✅ Show different dashboards side-by-side
- ✅ Demonstrate role-specific features
- ✅ Live patient-doctor interaction demo

---

## 🔄 Migration Notes

### Existing Sessions:
- Existing localStorage sessions will continue to work
- First login after update will use multi-tab mode
- No data loss or breaking changes

### Backward Compatibility:
- ✅ Fully backward compatible
- ✅ Existing code continues to work
- ✅ No breaking changes to API

---

## 📞 Quick Reference

```javascript
// Check current mode
console.log(localStorage.getItem('multiTabEnabled')); // "true" or "false" or null

// Enable multi-tab (independent sessions per tab)
localStorage.setItem('multiTabEnabled', 'true');

// Disable multi-tab (shared session across tabs)
localStorage.setItem('multiTabEnabled', 'false');

// Check current storage type being used
const isMultiTab = localStorage.getItem('multiTabEnabled') !== 'false';
console.log('Using:', isMultiTab ? 'sessionStorage' : 'localStorage');
```

---

**Status:** ✅ Implemented and Ready to Use
**Default Mode:** Multi-Tab Enabled
**Last Updated:** September 7, 2026
