# MediNova Test Accounts

## 🚀 Quick Access

All accounts are ready to use for testing and development.

---

## 👤 PATIENT ACCOUNTS

### Patient 1 - John Doe
- **Email:** `john.patient@test.com`
- **Password:** `Patient123!`
- **User ID:** `6a9e4f44183cb2b23c8bc554`
- **Role:** Patient
- **Phone:** +14155551234

### Patient 2 - Sarah Johnson
- **Email:** `sarah.patient@test.com`
- **Password:** `Patient123!`
- **User ID:** `6a9e4f46183cb2b23c8bc556`
- **Role:** Patient
- **Phone:** +14155552345

### Patient 3 - Michael Brown
- **Email:** `mike.patient@test.com`
- **Password:** `Patient123!`
- **User ID:** `6a9e4f48183cb2b23c8bc558`
- **Role:** Patient
- **Phone:** +14155553333

---

## 🩺 DOCTOR ACCOUNTS

### Doctor 1 - Dr. Michael Smith
- **Email:** `dr.smith@test.com`
- **Password:** `Doctor123!`
- **User ID:** `6a9e4f4b183cb2b23c8bc55a`
- **Role:** Doctor
- **Phone:** +14155553456
- **Specialization:** Can be set via profile

### Doctor 2 - Dr. Emily Williams
- **Email:** `dr.williams@test.com`
- **Password:** `Doctor123!`
- **User ID:** `6a9e4f4d183cb2b23c8bc55c`
- **Role:** Doctor
- **Phone:** +14155554567
- **Specialization:** Can be set via profile

### Doctor 3 - Dr. Rajesh Patel
- **Email:** `dr.patel@test.com`
- **Password:** `Doctor123!`
- **User ID:** `6a9e4f4f183cb2b23c8bc55e`
- **Role:** Doctor
- **Phone:** +14155555555
- **Specialization:** Can be set via profile

---

## ⚙️ ADMIN ACCOUNTS

### Admin 1 - System Administrator
- **Email:** `admin@medinova.com`
- **Password:** `Admin123!`
- **User ID:** `6a9e4f56183cb2b23c8bc560`
- **Role:** Admin
- **Phone:** +14155558901
- **Permissions:** Full system access

### Admin 2 - Super Administrator
- **Email:** `superadmin@medinova.com`
- **Password:** `Admin123!`
- **User ID:** `6a9e4f58183cb2b23c8bc561`
- **Role:** Admin
- **Phone:** +14155559012
- **Permissions:** Full system access

---

## 🔐 Password Requirements

All passwords follow the security requirements:
- ✅ Minimum 8 characters
- ✅ At least one uppercase letter
- ✅ At least one lowercase letter
- ✅ At least one number
- ✅ At least one special character (!@#$%^&*(),.?":{}|<>)

---

## 🧪 Testing Guide

### Login Test
```bash
# Using curl
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john.patient@test.com","password":"Patient123!"}'
```

### Quick Login URLs
- **Frontend:** http://localhost:5173/login
- **Backend API Docs:** http://localhost:8000/docs
- **Backend Health:** http://localhost:8000/api/v1/health

---

## 📝 Notes

1. **Database:** Currently using in-memory mongomock (data will NOT persist after restart)
2. **Hospital Role:** Not available in current schema (only patient, doctor, admin)
3. **Profile Setup:** After first login, doctors should complete their profile with specialization, qualifications, etc.
4. **Tokens:** Access tokens expire in 30 minutes, refresh tokens in 7 days

---

## 🔄 Re-creating Accounts

If you need to recreate all accounts:

```bash
cd backend
python create_test_users.py
```

---

## 📱 Available Roles

| Role | Description | Count |
|------|-------------|-------|
| **Patient** | End users seeking medical care | 3 |
| **Doctor** | Healthcare providers | 3 |
| **Admin** | System administrators | 2 |
| **Total** | | **8 accounts** |

---

**Last Updated:** September 7, 2026  
**Status:** ✅ All accounts active and ready for testing
