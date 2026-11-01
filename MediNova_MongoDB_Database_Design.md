# MediNova AI: MongoDB Database Design
## Production-Ready Database Architecture

---

**Project:** MediNova AI - Multi-Agent Healthcare Intelligence Platform  
**Database:** MongoDB Atlas  
**Document Type:** Database Design Specification  
**Date:** July 2, 2026  

---

## Table of Contents

1. [Database Overview](#1-database-overview)
2. [Collections Summary](#2-collections-summary)
3. [Collection Relationships](#3-collection-relationships)
4. [Detailed Collection Specifications](#4-detailed-collection-specifications)
5. [Validation Rules](#5-validation-rules)
6. [Indexing Strategy](#6-indexing-strategy)
7. [Embedded vs Referenced Documents](#7-embedded-vs-referenced-documents)
8. [Example JSON Documents](#8-example-json-documents)
9. [Data Optimization Strategy](#9-data-optimization-strategy)
10. [Scalability Considerations](#10-scalability-considerations)
11. [Security Considerations](#11-security-considerations)
12. [Entity Relationship Diagram](#12-entity-relationship-diagram)
13. [Collection to Module Mapping](#13-collection-to-module-mapping)

---

## 1. Database Overview

### 1.1 Database Architecture

**Database Name:** `medinova_db`  
**Platform:** MongoDB Atlas  
**Connection:** Cloud-based, replica set  
**Region:** Multi-region deployment for high availability  

### 1.2 Design Principles

1. **Document-Oriented:** Leverage MongoDB's flexible schema
2. **Denormalization:** Strategic data duplication for performance
3. **Embedding:** Related data together when accessed together
4. **Referencing:** Use ObjectId references for large or frequently changing data
5. **Indexing:** Comprehensive strategy for query optimization
6. **Validation:** Schema validation at database level
7. **Scalability:** Designed for horizontal scaling
8. **Security:** Field-level encryption for sensitive data

### 1.3 Naming Conventions

- **Collections:** Lowercase, plural, snake_case (e.g., `patient_profiles`)
- **Fields:** Lowercase, snake_case (e.g., `first_name`)
- **ObjectIds:** Suffix with `_id` (e.g., `user_id`)
- **Timestamps:** ISO 8601 format, UTC timezone
- **Booleans:** Prefix with `is_` or `has_` (e.g., `is_active`)

---

## 2. Collections Summary

### 2.1 Core Collections (14 Collections)

| # | Collection Name | Purpose | Avg Size | Growth Rate |
|---|-----------------|---------|----------|-------------|
| 1 | `users` | User authentication & basic info | 5 KB | High |
| 2 | `patient_profiles` | Patient medical information | 15 KB | High |
| 3 | `doctor_profiles` | Doctor professional information | 12 KB | Medium |
| 4 | `appointments` | Appointment bookings | 8 KB | High |
| 5 | `symptom_reports` | AI symptom checker sessions | 10 KB | Very High |
| 6 | `medical_documents` | Uploaded medical reports | 3 KB* | High |
| 7 | `prescriptions` | Doctor prescriptions | 6 KB | High |
| 8 | `medications` | Patient medication schedules | 4 KB | Medium |
| 9 | `health_records` | Vital signs & health data | 2 KB | Very High |
| 10 | `ai_conversations` | AI chat history | 12 KB | Very High |
| 11 | `notifications` | User notifications | 1 KB | Very High |
| 12 | `hospitals` | Hospital/clinic information | 8 KB | Low |
| 13 | `analytics_events` | User activity tracking | 2 KB | Very High |
| 14 | `admin_audit_logs` | Admin action logging | 3 KB | Medium |

**Note:** * Medical document metadata only (files stored in cloud storage)

### 2.2 Collection Categories

**User Management:**
- `users`
- `patient_profiles`
- `doctor_profiles`

**Healthcare Services:**
- `appointments`
- `symptom_reports`
- `prescriptions`
- `medications`

**Medical Records:**
- `medical_documents`
- `health_records`

**AI & Communication:**
- `ai_conversations`
- `notifications`

**Supporting Data:**
- `hospitals`
- `analytics_events`
- `admin_audit_logs`

---

## 3. Collection Relationships

### 3.1 Relationship Diagram

```
users (1) ──────┬────────> (1) patient_profiles
                │
                ├────────> (1) doctor_profiles
                │
                ├────────> (0..n) appointments
                │
                ├────────> (0..n) symptom_reports
                │
                ├────────> (0..n) medical_documents
                │
                ├────────> (0..n) health_records
                │
                ├────────> (0..n) ai_conversations
                │
                ├────────> (0..n) notifications
                │
                └────────> (0..n) analytics_events

patient_profiles (1) ────> (0..n) medications

appointments (n) ────────> (1) doctor_profiles
appointments (n) ────────> (1) patient_profiles
appointments (1) ────────> (0..1) prescriptions

prescriptions (n) ───────> (1) doctor_profiles
prescriptions (n) ───────> (1) patient_profiles

hospitals (1) ───────────> (0..n) doctor_profiles

symptom_reports (1) ─────> (0..1) appointments
```

### 3.2 Relationship Types

**One-to-One (1:1):**
- `users` ↔ `patient_profiles`
- `users` ↔ `doctor_profiles`
- `appointments` ↔ `prescriptions`

**One-to-Many (1:n):**
- `users` → `appointments`
- `users` → `symptom_reports`
- `users` → `medical_documents`
- `users` → `health_records`
- `users` → `ai_conversations`
- `patient_profiles` → `medications`
- `doctor_profiles` → `appointments`
- `hospitals` → `doctor_profiles`

**Many-to-Many (n:m) - Resolved:**
- Patients ↔ Doctors (through `appointments`)

---

## 4. Detailed Collection Specifications

### 4.1 Collection: `users`

**Purpose:** Core authentication and user account management

**Schema Definition:**

```javascript
{
  _id: ObjectId,
  email: String,              // Unique, indexed
  password_hash: String,      // bcrypt hashed
  role: String,               // "patient" | "doctor" | "admin"
  first_name: String,
  last_name: String,
  phone: String,              // Optional
  date_of_birth: ISODate,     // Optional
  gender: String,             // "male" | "female" | "other" | "prefer_not_to_say"
  profile_picture_url: String, // Cloud storage URL
  
  // Account Status
  is_active: Boolean,         // Account active/suspended
  is_email_verified: Boolean,
  is_phone_verified: Boolean,
  email_verification_token: String,  // Temporary
  email_verification_expires: ISODate,
  
  // Security
  password_reset_token: String,      // Temporary
  password_reset_expires: ISODate,
  mfa_enabled: Boolean,
  mfa_secret: String,                // Encrypted
  failed_login_attempts: Number,
  account_locked_until: ISODate,     // Temporary lock
  
  // Timestamps
  created_at: ISODate,
  updated_at: ISODate,
  last_login_at: ISODate,
  deleted_at: ISODate         // Soft delete
}
```

**Constraints:**
- `email`: Unique, required, lowercase, valid email format
- `password_hash`: Required, minimum length 60 (bcrypt)
- `role`: Required, enum ["patient", "doctor", "admin"]
- `is_active`: Default true
- `is_email_verified`: Default false
- `failed_login_attempts`: Default 0, max 5
- `created_at`: Auto-generated, indexed
- `updated_at`: Auto-updated on changes

**Field Justifications:**

**Embedded:**
- Basic user info (name, phone, DOB) - Always accessed together
- Account status flags - Small, frequently accessed
- Security fields - Part of authentication flow

**Not Included (Referenced):**
- Medical history - Large, separate concern → `patient_profiles`
- Professional info - Large, separate concern → `doctor_profiles`
- Activity data - High volume → Separate collections

---

### 4.2 Collection: `patient_profiles`

**Purpose:** Extended patient medical information

**Schema Definition:**

```javascript
{
  _id: ObjectId,
  user_id: ObjectId,          // Reference to users, unique indexed
  
  // Physical Attributes
  blood_group: String,        // "A+", "B-", etc.
  height_cm: Number,          // Decimal
  weight_kg: Number,          // Decimal
  bmi: Number,                // Calculated
  
  // Medical History (Embedded Arrays)
  allergies: [
    {
      allergen: String,       // Name of allergen
      type: String,           // "drug" | "food" | "environmental"
      severity: String,       // "mild" | "moderate" | "severe"
      reaction: String,       // Description
      diagnosed_date: ISODate,
      notes: String
    }
  ],
  
  chronic_conditions: [
    {
      condition: String,      // Disease name
      icd10_code: String,     // Standard code
      diagnosed_date: ISODate,
      status: String,         // "active" | "resolved" | "controlled"
      medications: [String],  // Current medications for this
      notes: String
    }
  ],
  
  past_surgeries: [
    {
      surgery_name: String,
      date: ISODate,
      hospital: String,
      surgeon: String,
      complications: String,
      notes: String
    }
  ],
  
  family_history: [
    {
      condition: String,
      relationship: String,   // "mother", "father", etc.
      age_of_onset: Number,
      notes: String
    }
  ],
  
  // Emergency Contact (Embedded Object)
  emergency_contact: {
    name: String,
    relationship: String,
    phone: String,
    email: String,
    address: String
  },
  
  // Insurance (Embedded Object)
  insurance: {
    provider: String,
    policy_number: String,
    group_number: String,
    expiry_date: ISODate,
    coverage_type: String
  },
  
  // Preferences (Embedded Object)
  preferences: {
    preferred_hospital: ObjectId,     // Reference to hospitals
    preferred_pharmacy: String,
    language: String,
    communication_preference: String  // "email" | "sms" | "both"
  },
  
  // Timestamps
  created_at: ISODate,
  updated_at: ISODate,
  last_health_check: ISODate
}
```

**Constraints:**
- `user_id`: Required, unique, indexed, foreign key
- `blood_group`: Enum ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
- `height_cm`: Positive number, range 50-250
- `weight_kg`: Positive number, range 2-300
- `allergies.severity`: Enum ["mild", "moderate", "severe"]
- `chronic_conditions.status`: Enum ["active", "resolved", "controlled"]
- `emergency_contact.phone`: Valid phone format

**Embedded vs Referenced:**

**Why Embed Medical History Arrays:**
1. Always accessed together with patient profile
2. Moderate size (typically <50 items per array)
3. Atomic updates needed
4. No independent querying required
5. Better read performance

**Why Reference Hospitals:**
- Hospitals are shared entities
- Prevent data duplication
- Hospital info may change independently

---

### 4.3 Collection: `doctor_profiles`

**Purpose:** Doctor professional information and credentials

**Schema Definition:**

```javascript
{
  _id: ObjectId,
  user_id: ObjectId,          // Reference to users, unique indexed
  
  // Professional Credentials
  license_number: String,     // Unique, indexed
  license_state: String,
  license_country: String,
  license_expiry: ISODate,
  license_document_url: String, // Cloud storage URL
  
  specialization: String,     // Primary specialty
  sub_specializations: [String], // Additional specialties
  
  // Qualifications (Embedded Array)
  qualifications: [
    {
      degree: String,         // "MBBS", "MD", "PhD", etc.
      institution: String,
      year: Number,
      country: String
    }
  ],
  
  // Experience
  years_of_experience: Number,
  total_consultations: Number, // Auto-incremented
  
  // Practice Details
  consultation_fee: Number,   // In USD
  consultation_duration: Number, // Minutes
  accepts_insurance: Boolean,
  languages_spoken: [String],
  
  bio: String,                // Professional summary
  
  // Hospital Affiliations (References)
  primary_hospital_id: ObjectId,    // Reference to hospitals
  affiliated_hospitals: [
    {
      hospital_id: ObjectId,          // Reference to hospitals
      position: String,               // "Staff", "Consultant", etc.
      department: String,
      since: ISODate
    }
  ],
  
  // Availability Schedule (Embedded)
  availability: [
    {
      day: String,            // "monday", "tuesday", etc.
      is_available: Boolean,
      time_slots: [
        {
          start_time: String, // "09:00"
          end_time: String,   // "17:00"
          slot_duration: Number // Minutes
        }
      ]
    }
  ],
  
  // Ratings & Reviews
  rating: Number,             // Average rating (0-5)
  review_count: Number,
  
  // Professional Status
  is_verified: Boolean,       // Admin verification
  verified_at: ISODate,
  verified_by: ObjectId,      // Admin user_id
  is_accepting_patients: Boolean,
  
  // Awards & Recognition (Embedded Array)
  awards: [
    {
      title: String,
      organization: String,
      year: Number,
      description: String
    }
  ],
  
  // Timestamps
  created_at: ISODate,
  updated_at: ISODate,
  last_active_at: ISODate
}
```

**Constraints:**
- `user_id`: Required, unique, indexed
- `license_number`: Required, unique, indexed
- `specialization`: Required
- `years_of_experience`: Non-negative integer
- `consultation_fee`: Positive number
- `consultation_duration`: Enum [15, 30, 45, 60]
- `rating`: Range 0-5, decimal
- `is_verified`: Default false
- `availability.day`: Enum ["monday", "tuesday", ..., "sunday"]
- `availability.time_slots.start_time`: Time format "HH:MM"

**Embedded vs Referenced:**

**Why Embed:**
- `qualifications`: Fixed size, accessed together, no independent querying
- `availability`: Frequently accessed, moderate size, part of doctor profile
- `awards`: Small list, display with profile

**Why Reference:**
- `hospitals`: Shared data, independent updates, prevent duplication
- `verified_by`: User reference for admin tracking

---

### 4.4 Collection: `appointments`

**Purpose:** Appointment bookings and consultation management

**Schema Definition:**

```javascript
{
  _id: ObjectId,
  appointment_number: String,  // Human-readable, unique, indexed
  
  // Participants (References)
  patient_id: ObjectId,       // Reference to users
  doctor_id: ObjectId,        // Reference to users
  
  // Appointment Details
  appointment_date: ISODate,  // Scheduled date & time
  duration_minutes: Number,   // Expected duration
  
  type: String,               // "video" | "in_person" | "chat"
  status: String,             // "scheduled" | "confirmed" | "in_progress" | "completed" | "cancelled" | "no_show"
  
  reason: String,             // Chief complaint
  symptoms: [String],         // List of symptoms
  
  // Symptom Report Link (Optional Reference)
  symptom_report_id: ObjectId, // If booked from AI checker
  
  // Consultation Details (Embedded)
  consultation: {
    started_at: ISODate,
    ended_at: ISODate,
    actual_duration: Number,  // Minutes
    
    // Doctor's Notes (Embedded)
    notes: String,
    diagnosis: String,
    icd10_codes: [String],
    
    // Recommendations (Embedded)
    lab_tests_ordered: [String],
    imaging_ordered: [String],
    follow_up_required: Boolean,
    follow_up_days: Number,
    
    // Vitals Recorded (Embedded)
    vitals: {
      blood_pressure: String,  // "120/80"
      heart_rate: Number,
      temperature: Number,     // Celsius
      oxygen_saturation: Number,
      weight: Number,
      height: Number
    }
  },
  
  // Prescription Reference
  prescription_id: ObjectId,   // Reference to prescriptions
  
  // Video Call Details (Embedded)
  video_call: {
    room_id: String,           // Video platform room
    join_url_patient: String,
    join_url_doctor: String,
    recording_url: String,     // If recorded
    duration_seconds: Number
  },
  
  // Payment Details (Embedded)
  payment: {
    amount: Number,
    currency: String,          // "USD"
    status: String,            // "pending" | "paid" | "refunded"
    payment_method: String,
    transaction_id: String,
    paid_at: ISODate
  },
  
  // Cancellation (Embedded)
  cancellation: {
    cancelled_by: ObjectId,    // user_id
    cancelled_at: ISODate,
    reason: String,
    refund_amount: Number
  },
  
  // Reminders Sent (Embedded Array)
  reminders_sent: [
    {
      type: String,            // "24h" | "1h" | "15m"
      sent_at: ISODate,
      channel: String          // "email" | "sms" | "push"
    }
  ],
  
  // Timestamps
  created_at: ISODate,
  updated_at: ISODate,
  completed_at: ISODate
}
```

**Constraints:**
- `appointment_number`: Unique, format "APT-YYYYMMDD-XXXX"
- `patient_id`: Required, indexed
- `doctor_id`: Required, indexed
- `appointment_date`: Required, indexed, future date
- `duration_minutes`: Enum [15, 30, 45, 60]
- `type`: Required, enum ["video", "in_person", "chat"]
- `status`: Required, enum list, default "scheduled"
- `payment.amount`: Non-negative
- `payment.status`: Enum ["pending", "paid", "refunded"]

**Embedded vs Referenced:**

**Why Embed:**
- `consultation`: Created once, accessed together, moderate size
- `video_call`: Specific to this appointment, not reused
- `payment`: Transaction specific to appointment
- `cancellation`: Event specific to this appointment
- `reminders_sent`: Log data, accessed with appointment

**Why Reference:**
- `patient_id`, `doctor_id`: Core entities, referenced everywhere
- `prescription_id`: Separate document, may be updated independently
- `symptom_report_id`: Previous session data, large document

---

### 4.5 Collection: `symptom_reports`

**Purpose:** AI symptom checker conversation and analysis

**Schema Definition:**

```javascript
{
  _id: ObjectId,
  session_id: String,          // UUID, unique, indexed
  patient_id: ObjectId,        // Reference to users
  
  // Conversation History (Embedded Array)
  conversation: [
    {
      timestamp: ISODate,
      speaker: String,         // "patient" | "ai"
      message: String,
      intent: String,          // AI-detected intent
      confidence: Number       // 0-1
    }
  ],
  
  // Extracted Symptoms (Embedded Array)
  symptoms: [
    {
      symptom: String,         // Symptom name
      body_part: String,       // "head", "chest", etc.
      severity: Number,        // 1-10
      duration: String,        // "2 days", "1 week"
      frequency: String,       // "constant", "intermittent"
      onset: String,           // "sudden", "gradual"
      triggers: [String],      // Factors that worsen
      relievers: [String],     // Factors that improve
      location: String         // Specific location
    }
  ],
  
  // AI Assessment (Embedded Object)
  ai_assessment: {
    urgency_level: String,     // "routine" | "urgent" | "emergency"
    urgency_score: Number,     // 0-100
    
    // Possible Diagnoses (Embedded Array)
    diagnoses: [
      {
        condition: String,
        icd10_code: String,
        confidence: Number,    // 0-1
        reasoning: String,
        supporting_symptoms: [String],
        recommended_tests: [String]
      }
    ],
    
    // Recommendations (Embedded Array)
    recommendations: [String],
    
    // Red Flags Detected (Embedded Array)
    red_flags: [String],
    
    // Suggested Action
    suggested_action: String,  // "self_care" | "schedule_appointment" | "urgent_care" | "emergency"
    specialty_recommended: String,
    
    // AI Model Info
    model_version: String,
    processed_at: ISODate,
    processing_time_ms: Number
  },
  
  // Status
  status: String,              // "in_progress" | "completed" | "abandoned"
  
  // Follow-up Actions
  appointment_booked: Boolean,
  appointment_id: ObjectId,    // Reference if booked
  
  // Timestamps
  created_at: ISODate,
  updated_at: ISODate,
  completed_at: ISODate
}
```

**Constraints:**
- `session_id`: Required, unique, indexed
- `patient_id`: Required, indexed
- `conversation`: Array required, min 1 message
- `symptoms.severity`: Range 1-10
- `ai_assessment.urgency_level`: Enum ["routine", "urgent", "emergency"]
- `ai_assessment.urgency_score`: Range 0-100
- `ai_assessment.diagnoses.confidence`: Range 0-1
- `status`: Enum ["in_progress", "completed", "abandoned"]

**Embedded vs Referenced:**

**Why Embed Everything:**
- `conversation`: High-value data, accessed as complete session
- `symptoms`: Specific to this session, not reused
- `ai_assessment`: Generated once, accessed together
- All data forms cohesive session record
- No need to query parts independently
- Better read performance for session replay

**Why Reference:**
- `appointment_id`: If action taken, link to external entity

---

### 4.6 Collection: `medical_documents`

**Purpose:** Medical report metadata and AI analysis results

**Schema Definition:**

```javascript
{
  _id: ObjectId,
  document_id: String,         // UUID, unique, indexed
  
  // Ownership
  patient_id: ObjectId,        // Reference to users, indexed
  uploaded_by: ObjectId,       // user_id (patient or doctor)
  
  // Document Details
  document_type: String,       // "lab_report" | "prescription" | "xray" | "ct_scan" | "mri" | "other"
  title: String,
  description: String,
  
  // File Information
  file_name: String,
  file_size: Number,           // Bytes
  file_type: String,           // MIME type
  file_url: String,            // Cloud storage URL (S3/GCS)
  thumbnail_url: String,       // For images
  
  // Document Date
  document_date: ISODate,      // Date on the document
  
  // Associated Entities (References)
  doctor_id: ObjectId,         // If from a doctor
  appointment_id: ObjectId,    // If from consultation
  hospital_name: String,       // Where document originated
  
  // OCR Extraction (Embedded Object)
  ocr_data: {
    raw_text: String,          // Extracted text
    confidence: Number,        // 0-1
    language: String,
    processed_at: ISODate,
    processing_time_ms: Number
  },
  
  // AI Analysis (Embedded Object)
  ai_analysis: {
    // For Lab Reports
    lab_results: [
      {
        parameter: String,     // "Hemoglobin", "Glucose", etc.
        value: Number,
        unit: String,
        reference_range: String,
        is_abnormal: Boolean,
        abnormality_type: String, // "high" | "low" | "critical"
        interpretation: String
      }
    ],
    
    // For Imaging (X-ray, CT, MRI)
    imaging_findings: {
      body_part: String,
      modality: String,        // "X-ray", "CT", "MRI"
      findings: [String],
      abnormalities_detected: [String],
      impression: String
    },
    
    // For Prescriptions
    medications_extracted: [
      {
        drug_name: String,
        dosage: String,
        frequency: String,
        duration: String,
        instructions: String
      }
    ],
    
    // AI Processing Info
    model_version: String,
    processed_at: ISODate,
    confidence: Number         // Overall confidence
  },
  
  // Sharing & Permissions (Embedded Array)
  shared_with: [
    {
      user_id: ObjectId,       // Doctor/user it's shared with
      shared_at: ISODate,
      shared_by: ObjectId,
      access_level: String,    // "view" | "download"
      expires_at: ISODate,
      revoked: Boolean
    }
  ],
  
  // Tags & Categories
  tags: [String],              // User-defined tags
  category: String,            // "reports", "prescriptions", "imaging"
  
  // Privacy & Security
  is_sensitive: Boolean,
  encryption_key_id: String,   // If encrypted
  
  // Timestamps
  uploaded_at: ISODate,
  created_at: ISODate,
  updated_at: ISODate,
  deleted_at: ISODate          // Soft delete
}
```

**Constraints:**
- `document_id`: Required, unique, indexed
- `patient_id`: Required, indexed
- `document_type`: Required, enum
- `file_size`: Max 10 MB (10485760 bytes)
- `file_type`: Enum ["application/pdf", "image/jpeg", "image/png", "application/dicom"]
- `file_url`: Required, valid URL
- `ocr_data.confidence`: Range 0-1
- `ai_analysis.lab_results.value`: Number
- `shared_with.access_level`: Enum ["view", "download"]

**Embedded vs Referenced:**

**Why Embed:**
- `ocr_data`: Generated once, integral to document
- `ai_analysis`: Complex but accessed together with document
- `shared_with`: Access log, moderate size, accessed with document

**Why Not Store File:**
- Files stored in cloud storage (S3/GCS)
- Only metadata and URLs in MongoDB
- Better for large files and bandwidth


---

### 4.7 Collection: `prescriptions`

**Purpose:** Doctor-issued prescriptions

**Schema Definition:**

```javascript
{
  _id: ObjectId,
  prescription_number: String,  // Human-readable, unique, indexed
  
  // Participants (References)
  patient_id: ObjectId,        // Reference to users, indexed
  doctor_id: ObjectId,         // Reference to users, indexed
  appointment_id: ObjectId,    // Reference to appointments
  
  // Prescription Details
  prescribed_date: ISODate,
  valid_until: ISODate,        // Expiry date
  
  // Medications (Embedded Array)
  medications: [
    {
      drug_name: String,
      generic_name: String,
      dosage: String,          // "500mg"
      frequency: String,       // "Twice daily"
      duration_days: Number,
      quantity: Number,        // Total pills/units
      instructions: String,    // "Take with food"
      route: String,           // "oral", "topical", etc.
      form: String             // "tablet", "capsule", "syrup"
    }
  ],
  
  // Additional Instructions
  diagnosis: String,
  general_instructions: String,
  precautions: String,
  diet_restrictions: String,
  
  // Follow-up
  follow_up_required: Boolean,
  follow_up_date: ISODate,
  follow_up_notes: String,
  
  // Status
  status: String,              // "draft" | "signed" | "sent" | "filled" | "cancelled"
  
  // Digital Signature
  signed: Boolean,
  signed_at: ISODate,
  signature_hash: String,      // Cryptographic hash
  
  // Pharmacy Details
  pharmacy_name: String,
  pharmacy_filled: Boolean,
  filled_at: ISODate,
  
  // Timestamps
  created_at: ISODate,
  updated_at: ISODate
}
```

**Constraints:**
- `prescription_number`: Unique, format "RX-YYYYMMDD-XXXX"
- `patient_id`: Required, indexed
- `doctor_id`: Required, indexed
- `prescribed_date`: Required, indexed
- `valid_until`: Future date, typically 30-90 days
- `medications`: Array required, min 1 item
- `status`: Enum ["draft", "signed", "sent", "filled", "cancelled"]
- `signed`: Default false

---

### 4.8 Collection: `medications`

**Purpose:** Patient medication schedules and reminders

**Schema Definition:**

```javascript
{
  _id: ObjectId,
  patient_id: ObjectId,        // Reference to users, indexed
  
  // Medication Details
  medicine_name: String,
  generic_name: String,
  dosage: String,
  form: String,                // "tablet", "capsule", "syrup"
  
  // Schedule (Embedded Object)
  schedule: {
    frequency: String,         // "daily", "specific_days", "as_needed"
    times_per_day: Number,
    
    // Time Slots (Embedded Array)
    time_slots: [
      {
        time: String,          // "08:00", "20:00"
        with_meal: String      // "before" | "after" | "with" | "anytime"
      }
    ],
    
    // For specific days
    days_of_week: [Number],    // [1,3,5] for Mon, Wed, Fri
    
    // Duration
    start_date: ISODate,
    end_date: ISODate,         // null for ongoing
    is_ongoing: Boolean
  },
  
  // Instructions
  instructions: String,
  special_instructions: String,
  
  // Stock Management
  initial_quantity: Number,
  current_quantity: Number,
  refill_reminder_at: Number,  // Quantity threshold
  last_refilled_date: ISODate,
  
  // Adherence Tracking (Embedded Array)
  adherence_log: [
    {
      scheduled_time: ISODate,
      taken: Boolean,
      taken_at: ISODate,
      skipped: Boolean,
      skip_reason: String,
      noted_by: String         // "user" | "caregiver"
    }
  ],
  
  // Reminder Preferences
  reminder_enabled: Boolean,
  reminder_advance_minutes: Number, // How early to remind
  reminder_channels: [String], // ["push", "sms", "email"]
  
  // Source
  prescribed_by: ObjectId,     // Doctor user_id, optional
  prescription_id: ObjectId,   // Reference, optional
  
  // Status
  is_active: Boolean,
  paused: Boolean,
  pause_reason: String,
  
  // Timestamps
  created_at: ISODate,
  updated_at: ISODate,
  completed_at: ISODate
}
```

**Constraints:**
- `patient_id`: Required, indexed
- `medicine_name`: Required
- `schedule.frequency`: Enum ["daily", "specific_days", "as_needed"]
- `schedule.time_slots`: Array required if not "as_needed"
- `initial_quantity`: Positive number
- `current_quantity`: Non-negative, <= initial_quantity
- `is_active`: Default true
- `reminder_enabled`: Default true

---

### 4.9 Collection: `health_records`

**Purpose:** Vital signs and health measurements

**Schema Definition:**

```javascript
{
  _id: ObjectId,
  patient_id: ObjectId,        // Reference to users, indexed
  
  // Record Type
  record_type: String,         // "vitals" | "lab_test" | "diagnosis" | "note"
  
  // Record Date & Time
  recorded_at: ISODate,        // When measurement taken
  
  // Vital Signs (for record_type: "vitals")
  vitals: {
    // Cardiovascular
    blood_pressure_systolic: Number,
    blood_pressure_diastolic: Number,
    heart_rate: Number,        // BPM
    
    // Respiratory
    respiratory_rate: Number,  // Breaths per minute
    oxygen_saturation: Number, // SpO2 percentage
    
    // Body Temperature
    temperature: Number,       // Celsius
    temperature_location: String, // "oral", "armpit", "ear"
    
    // Body Metrics
    weight: Number,            // Kg
    height: Number,            // Cm
    bmi: Number,               // Calculated
    
    // Other
    blood_glucose: Number      // mg/dL
  },
  
  // Lab Test Results (for record_type: "lab_test")
  lab_test: {
    test_name: String,
    lab_name: String,
    ordered_by: ObjectId,      // Doctor user_id
    
    // Results (Embedded Array)
    results: [
      {
        parameter: String,
        value: Number,
        unit: String,
        reference_range: String,
        is_abnormal: Boolean
      }
    ],
    
    report_document_id: ObjectId // Reference to medical_documents
  },
  
  // Diagnosis (for record_type: "diagnosis")
  diagnosis: {
    condition: String,
    icd10_code: String,
    diagnosed_by: ObjectId,    // Doctor user_id
    severity: String,          // "mild" | "moderate" | "severe"
    notes: String
  },
  
  // General Note (for record_type: "note")
  note: {
    title: String,
    content: String,
    category: String           // "symptom", "medication", "lifestyle"
  },
  
  // Source & Recording
  recorded_by: ObjectId,       // user_id who recorded
  source: String,              // "manual" | "device" | "doctor" | "lab"
  device_name: String,         // If from device
  
  // Associated Entities
  appointment_id: ObjectId,    // If recorded during appointment
  
  // Timestamps
  created_at: ISODate,
  updated_at: ISODate
}
```

**Constraints:**
- `patient_id`: Required, indexed
- `record_type`: Required, enum
- `recorded_at`: Required, indexed (for time-series queries)
- `vitals.blood_pressure_systolic`: Range 60-250
- `vitals.blood_pressure_diastolic`: Range 40-150
- `vitals.heart_rate`: Range 30-220
- `vitals.temperature`: Range 32-43 (Celsius)
- `vitals.oxygen_saturation`: Range 0-100
- `source`: Enum ["manual", "device", "doctor", "lab"]

---

### 4.10 Collection: `ai_conversations`

**Purpose:** Complete AI chat history

**Schema Definition:**

```javascript
{
  _id: ObjectId,
  conversation_id: String,     // UUID, unique, indexed
  user_id: ObjectId,           // Reference to users, indexed
  
  // Conversation Type
  type: String,                // "symptom_check" | "health_advice" | "general"
  
  // Messages (Embedded Array)
  messages: [
    {
      message_id: String,      // UUID for message
      timestamp: ISODate,
      role: String,            // "user" | "assistant"
      content: String,
      
      // AI Metadata
      model: String,           // "gpt-4", "gpt-3.5-turbo"
      tokens_used: Number,
      latency_ms: Number,
      
      // Message Type
      message_type: String,    // "text" | "image" | "document"
      attachments: [
        {
          file_url: String,
          file_type: String,
          file_name: String
        }
      ]
    }
  ],
  
  // Session Context (Embedded Object)
  context: {
    patient_age: Number,
    patient_gender: String,
    chronic_conditions: [String],
    current_medications: [String],
    known_allergies: [String]
  },
  
  // Conversation Summary
  summary: String,             // AI-generated summary
  key_points: [String],
  
  // Linked Entities
  symptom_report_id: ObjectId, // If converted to symptom report
  appointment_id: ObjectId,    // If appointment booked
  
  // Status
  status: String,              // "active" | "completed" | "archived"
  
  // Timestamps
  started_at: ISODate,
  last_message_at: ISODate,
  ended_at: ISODate,
  created_at: ISODate,
  updated_at: ISODate
}
```

**Constraints:**
- `conversation_id`: Required, unique, indexed
- `user_id`: Required, indexed
- `type`: Enum ["symptom_check", "health_advice", "general"]
- `messages`: Array required
- `messages.role`: Enum ["user", "assistant"]
- `messages.message_type`: Enum ["text", "image", "document"]
- `status`: Enum ["active", "completed", "archived"]

---

### 4.11 Collection: `notifications`

**Purpose:** User notifications and alerts

**Schema Definition:**

```javascript
{
  _id: ObjectId,
  user_id: ObjectId,           // Reference to users, indexed
  
  // Notification Details
  type: String,                // "appointment" | "medication" | "lab_result" | "message" | "alert" | "reminder"
  category: String,            // "info" | "warning" | "success" | "error"
  
  // Content
  title: String,
  message: String,
  
  // Priority
  priority: String,            // "low" | "medium" | "high" | "urgent"
  
  // Status
  is_read: Boolean,
  read_at: ISODate,
  
  // Action Link
  action_url: String,          // Deep link in app
  action_text: String,         // "View Appointment", "Take Medicine"
  
  // Related Entities (References)
  related_entity: {
    entity_type: String,       // "appointment", "medication", "document"
    entity_id: ObjectId
  },
  
  // Delivery
  channels: [String],          // ["push", "email", "sms"]
  delivery_status: {
    push_sent: Boolean,
    push_sent_at: ISODate,
    email_sent: Boolean,
    email_sent_at: ISODate,
    sms_sent: Boolean,
    sms_sent_at: ISODate
  },
  
  // Scheduling
  scheduled_for: ISODate,      // For scheduled notifications
  expires_at: ISODate,         // Auto-delete after
  
  // Timestamps
  created_at: ISODate,
  updated_at: ISODate
}
```

**Constraints:**
- `user_id`: Required, indexed
- `type`: Required, enum
- `category`: Required, enum
- `priority`: Enum ["low", "medium", "high", "urgent"]
- `is_read`: Default false, indexed
- `channels`: Array, subset of ["push", "email", "sms"]
- `created_at`: Indexed for sorting

---

### 4.12 Collection: `hospitals`

**Purpose:** Hospital and clinic information

**Schema Definition:**

```javascript
{
  _id: ObjectId,
  hospital_id: String,         // Unique identifier
  
  // Basic Information
  name: String,                // Official name
  type: String,                // "hospital" | "clinic" | "diagnostic_center"
  
  // Contact Information
  phone: String,
  email: String,
  website: String,
  
  // Address (Embedded Object)
  address: {
    street: String,
    city: String,
    state: String,
    country: String,
    postal_code: String,
    
    // Geolocation for maps
    location: {
      type: "Point",
      coordinates: [Number, Number] // [longitude, latitude]
    }
  },
  
  // Services Offered (Embedded Array)
  services: [String],          // ["Emergency", "ICU", "Cardiology"]
  
  // Specialties Available (Embedded Array)
  specialties: [String],
  
  // Facilities (Embedded Object)
  facilities: {
    emergency_services: Boolean,
    icu_beds: Number,
    general_beds: Number,
    operation_theaters: Number,
    pharmacy: Boolean,
    laboratory: Boolean,
    ambulance_service: Boolean,
    parking_available: Boolean
  },
  
  // Operating Hours (Embedded Array)
  operating_hours: [
    {
      day: String,             // "monday", "tuesday", etc.
      open_time: String,       // "00:00" for 24/7
      close_time: String,      // "23:59" for 24/7
      is_24_7: Boolean
    }
  ],
  
  // Insurance
  insurance_accepted: [String],
  
  // Ratings & Reviews
  rating: Number,              // Average 0-5
  review_count: Number,
  
  // Verification
  is_verified: Boolean,
  verified_at: ISODate,
  
  // Status
  is_active: Boolean,
  
  // Timestamps
  created_at: ISODate,
  updated_at: ISODate
}
```

**Constraints:**
- `hospital_id`: Unique, indexed
- `name`: Required, indexed
- `type`: Enum ["hospital", "clinic", "diagnostic_center"]
- `address.location.type`: Always "Point"
- `address.location.coordinates`: [longitude, latitude] format
- `rating`: Range 0-5
- `is_verified`: Default false
- `is_active`: Default true

---

### 4.13 Collection: `analytics_events`

**Purpose:** User activity and behavior tracking

**Schema Definition:**

```javascript
{
  _id: ObjectId,
  user_id: ObjectId,           // Reference to users, indexed
  
  // Event Details
  event_type: String,          // "page_view" | "button_click" | "feature_use" | "search"
  event_name: String,          // Specific event identifier
  
  // Event Data (Flexible Schema)
  event_data: Object,          // Dynamic based on event type
  
  // Session Info
  session_id: String,
  
  // Device & Platform
  device: {
    type: String,              // "mobile" | "tablet" | "desktop"
    os: String,
    browser: String,
    app_version: String
  },
  
  // Location
  ip_address: String,
  country: String,
  city: String,
  
  // Timestamp
  timestamp: ISODate,
  
  // Created timestamp
  created_at: ISODate
}
```

**Constraints:**
- `user_id`: Indexed (can be null for anonymous)
- `event_type`: Required, indexed
- `timestamp`: Required, indexed (time-series)
- `session_id`: Indexed

---

### 4.14 Collection: `admin_audit_logs`

**Purpose:** Admin action logging for compliance

**Schema Definition:**

```javascript
{
  _id: ObjectId,
  admin_id: ObjectId,          // Reference to users (admin)
  
  // Action Details
  action: String,              // "user_created" | "user_suspended" | "doctor_verified"
  action_category: String,     // "user_management" | "content_moderation" | "system_config"
  
  // Target
  target_type: String,         // "user" | "doctor" | "appointment"
  target_id: ObjectId,
  
  // Changes Made (for updates)
  changes: {
    before: Object,            // Previous state
    after: Object              // New state
  },
  
  // Request Details
  ip_address: String,
  user_agent: String,
  
  // Result
  success: Boolean,
  error_message: String,       // If failed
  
  // Timestamp
  timestamp: ISODate,
  created_at: ISODate
}
```

**Constraints:**
- `admin_id`: Required, indexed
- `action`: Required, indexed
- `timestamp`: Required, indexed
- `target_id`: Indexed

---

## 5. Validation Rules

### 5.1 MongoDB Schema Validation

**Implementation:** JSON Schema validation at collection level

**Example for `users` collection:**

```javascript
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "password_hash", "role", "first_name", "last_name"],
      properties: {
        email: {
          bsonType: "string",
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
          description: "must be a valid email and is required"
        },
        role: {
          enum: ["patient", "doctor", "admin"],
          description: "must be one of the enum values"
        },
        phone: {
          bsonType: ["string", "null"],
          pattern: "^\\+?[1-9]\\d{1,14}$",
          description: "must be a valid phone number"
        },
        is_active: {
          bsonType: "bool",
          description: "must be a boolean"
        }
      }
    }
  }
})
```

### 5.2 Application-Level Validation

**Using Pydantic in FastAPI:**

**User Email:**
- Format: Valid email regex
- Unique: Check before insert
- Lowercase: Convert to lowercase

**Password:**
- Minimum length: 8 characters
- Complexity: At least one uppercase, lowercase, number, special char
- Hashed: bcrypt with salt rounds 12

**Dates:**
- Future dates: appointment_date, prescription_valid_until
- Past dates: date_of_birth
- Range: recorded_at within reasonable bounds

**Phone Numbers:**
- Format: E.164 international format
- Validation: libphonenumber library

**Enums:**
- Strict validation against allowed values
- Case-insensitive comparison

**Numeric Ranges:**
- Vital signs: Physiological ranges
- Ratings: 0-5
- Severity: 1-10
- Age: 0-150

---

## 6. Indexing Strategy

### 6.1 Index Types

**Single Field Indexes:**
```javascript
// users
db.users.createIndex({ email: 1 }, { unique: true })
db.users.createIndex({ role: 1 })
db.users.createIndex({ created_at: -1 })

// patient_profiles
db.patient_profiles.createIndex({ user_id: 1 }, { unique: true })

// doctor_profiles
db.doctor_profiles.createIndex({ user_id: 1 }, { unique: true })
db.doctor_profiles.createIndex({ license_number: 1 }, { unique: true })
db.doctor_profiles.createIndex({ specialization: 1 })
db.doctor_profiles.createIndex({ is_verified: 1 })

// appointments
db.appointments.createIndex({ appointment_number: 1 }, { unique: true })
db.appointments.createIndex({ patient_id: 1 })
db.appointments.createIndex({ doctor_id: 1 })
db.appointments.createIndex({ appointment_date: 1 })
db.appointments.createIndex({ status: 1 })

// symptom_reports
db.symptom_reports.createIndex({ session_id: 1 }, { unique: true })
db.symptom_reports.createIndex({ patient_id: 1 })
db.symptom_reports.createIndex({ created_at: -1 })

// medical_documents
db.medical_documents.createIndex({ document_id: 1 }, { unique: true })
db.medical_documents.createIndex({ patient_id: 1 })
db.medical_documents.createIndex({ document_type: 1 })
db.medical_documents.createIndex({ uploaded_at: -1 })

// prescriptions
db.prescriptions.createIndex({ prescription_number: 1 }, { unique: true })
db.prescriptions.createIndex({ patient_id: 1 })
db.prescriptions.createIndex({ doctor_id: 1 })
db.prescriptions.createIndex({ prescribed_date: -1 })

// medications
db.medications.createIndex({ patient_id: 1 })
db.medications.createIndex({ is_active: 1 })

// health_records
db.health_records.createIndex({ patient_id: 1 })
db.health_records.createIndex({ recorded_at: -1 })
db.health_records.createIndex({ record_type: 1 })

// ai_conversations
db.ai_conversations.createIndex({ conversation_id: 1 }, { unique: true })
db.ai_conversations.createIndex({ user_id: 1 })
db.ai_conversations.createIndex({ status: 1 })

// notifications
db.notifications.createIndex({ user_id: 1 })
db.notifications.createIndex({ is_read: 1 })
db.notifications.createIndex({ created_at: -1 })

// hospitals
db.hospitals.createIndex({ hospital_id: 1 }, { unique: true })
db.hospitals.createIndex({ name: 1 })

// analytics_events
db.analytics_events.createIndex({ user_id: 1 })
db.analytics_events.createIndex({ event_type: 1 })
db.analytics_events.createIndex({ timestamp: -1 })

// admin_audit_logs
db.admin_audit_logs.createIndex({ admin_id: 1 })
db.admin_audit_logs.createIndex({ action: 1 })
db.admin_audit_logs.createIndex({ timestamp: -1 })
```


**Compound Indexes:**
```javascript
// appointments - Query by doctor, date, and status together
db.appointments.createIndex({ doctor_id: 1, appointment_date: 1, status: 1 })

// appointments - Query by patient and date range
db.appointments.createIndex({ patient_id: 1, appointment_date: -1 })

// appointments - Query upcoming appointments
db.appointments.createIndex({ appointment_date: 1, status: 1 })

// doctor_profiles - Search by specialization and verified status
db.doctor_profiles.createIndex({ specialization: 1, is_verified: 1, is_accepting_patients: 1 })

// medical_documents - Patient's documents by type and date
db.medical_documents.createIndex({ patient_id: 1, document_type: 1, uploaded_at: -1 })

// health_records - Patient's vital history
db.health_records.createIndex({ patient_id: 1, record_type: 1, recorded_at: -1 })

// medications - Active medications for patient
db.medications.createIndex({ patient_id: 1, is_active: 1, "schedule.start_date": 1 })

// notifications - Unread notifications for user
db.notifications.createIndex({ user_id: 1, is_read: 1, created_at: -1 })

// symptom_reports - Patient's recent sessions
db.symptom_reports.createIndex({ patient_id: 1, status: 1, created_at: -1 })

// ai_conversations - Active conversations
db.ai_conversations.createIndex({ user_id: 1, status: 1, last_message_at: -1 })

// analytics_events - User activity timeline
db.analytics_events.createIndex({ user_id: 1, timestamp: -1 })

// admin_audit_logs - Audit trail by action category
db.admin_audit_logs.createIndex({ action_category: 1, timestamp: -1 })
```

**Text Indexes:**
```javascript
// users - Search by name
db.users.createIndex({ 
  first_name: "text", 
  last_name: "text",
  email: "text"
}, { 
  name: "user_search_index",
  weights: {
    first_name: 10,
    last_name: 10,
    email: 5
  }
})

// doctor_profiles - Search doctors by name and specialty
db.doctor_profiles.createIndex({
  specialization: "text",
  sub_specializations: "text",
  bio: "text"
}, {
  name: "doctor_search_index",
  weights: {
    specialization: 15,
    sub_specializations: 10,
    bio: 5
  }
})

// hospitals - Search by name, services, specialties
db.hospitals.createIndex({
  name: "text",
  services: "text",
  specialties: "text",
  "address.city": "text"
}, {
  name: "hospital_search_index",
  weights: {
    name: 15,
    services: 10,
    specialties: 10,
    "address.city": 5
  }
})

// medical_documents - Search in OCR text
db.medical_documents.createIndex({
  title: "text",
  description: "text",
  "ocr_data.raw_text": "text"
}, {
  name: "document_search_index",
  weights: {
    title: 15,
    description: 10,
    "ocr_data.raw_text": 5
  }
})

// symptom_reports - Search symptoms
db.symptom_reports.createIndex({
  "symptoms.symptom": "text",
  "symptoms.body_part": "text",
  "ai_assessment.diagnoses.condition": "text"
}, {
  name: "symptom_search_index"
})
```

**Geospatial Indexes:**
```javascript
// hospitals - Location-based search for hospital finder
db.hospitals.createIndex({ "address.location": "2dsphere" })

// Usage: Find hospitals within radius
// db.hospitals.find({
//   "address.location": {
//     $near: {
//       $geometry: { type: "Point", coordinates: [longitude, latitude] },
//       $maxDistance: 5000  // 5km radius
//     }
//   }
// })
```

**TTL Indexes (Time-To-Live):**
```javascript
// notifications - Auto-delete read notifications after 90 days
db.notifications.createIndex(
  { created_at: 1 }, 
  { 
    expireAfterSeconds: 7776000,  // 90 days
    partialFilterExpression: { is_read: true }
  }
)

// analytics_events - Auto-delete events after 180 days
db.analytics_events.createIndex(
  { created_at: 1 },
  { expireAfterSeconds: 15552000 }  // 180 days
)

// users - Auto-delete unverified accounts after 30 days
db.users.createIndex(
  { created_at: 1 },
  {
    expireAfterSeconds: 2592000,  // 30 days
    partialFilterExpression: { is_email_verified: false }
  }
)

// ai_conversations - Auto-archive old archived conversations after 1 year
db.ai_conversations.createIndex(
  { ended_at: 1 },
  {
    expireAfterSeconds: 31536000,  // 365 days
    partialFilterExpression: { status: "archived" }
  }
)
```

### 6.2 Index Performance Considerations

**Index Selectivity:**
- High selectivity: `email`, `license_number`, unique identifiers
- Medium selectivity: `status`, `role`, `type`
- Low selectivity: `is_active`, `is_verified` (use compound indexes)

**Index Size Management:**
- Monitor index sizes: Aim for <20% of collection size
- Use partial indexes for conditional queries
- Drop unused indexes regularly

**Query Optimization:**
- Use `explain()` to analyze query plans
- Ensure queries use indexes (IXSCAN not COLLSCAN)
- Covered queries when possible (projection matches index)

**Write Performance:**
- Balance read optimization with write overhead
- Each index slows inserts/updates by ~10%
- Maximum 64 indexes per collection (keep under 10-12)

**Index Maintenance:**
- Rebuild indexes monthly during low-traffic periods
- Monitor index fragmentation
- Use background index builds

---

## 7. Embedded vs Referenced Documents

### 7.1 Design Decision Framework

**When to Embed:**
1. **One-to-Few relationship** (< 100 subdocuments)
2. **Data accessed together** (read pattern matches)
3. **Atomic updates needed** (update parent and child together)
4. **No independent querying** (subdocument only accessed via parent)
5. **Bounded growth** (won't exceed 16MB document limit)

**When to Reference:**
1. **One-to-Many** (> 100 related documents)
2. **One-to-Squillions** (unbounded growth)
3. **Independent access** (queried separately)
4. **Shared data** (many-to-many relationships)
5. **Large subdocuments** (risk hitting 16MB limit)
6. **Frequent updates** to child without parent

### 7.2 Collection-Specific Justifications

#### **7.2.1 `users` Collection**

**Embedded:**
- **Basic profile fields** (name, phone, DOB)
  - **Why:** Always accessed together during authentication
  - **Size:** ~200 bytes, fixed
  - **Access:** Read on every login/session
  
- **Account status flags** (is_active, is_verified)
  - **Why:** Critical for authentication flow
  - **Size:** Minimal (boolean flags)
  - **Updates:** Infrequent, atomic with user record


- **Security fields** (password reset tokens, MFA)
  - **Why:** Part of auth workflow, temporary data
  - **Size:** ~200 bytes
  - **Updates:** Together with user security state

**Referenced:**
- **Medical profiles** → `patient_profiles`, `doctor_profiles`
  - **Why:** Large (10-15KB), specialized data
  - **Access:** Only when viewing profile details
  - **Growth:** Unbounded (allergies, conditions grow)
  - **Separation:** Role-specific (not all users are patients/doctors)

#### **7.2.2 `patient_profiles` Collection**

**Embedded:**
- **Medical history arrays** (allergies, chronic_conditions, past_surgeries, family_history)
  - **Why:** Always viewed together on patient chart
  - **Size:** Moderate (~50-200 items total, 5-10KB)
  - **Growth:** Bounded (unlikely > 100 allergies or conditions)
  - **Atomicity:** Update entire medical history atomically
  - **Query pattern:** "Show me patient's full medical profile"
  
- **Emergency contact** (single object)
  - **Why:** Critical info, accessed with profile
  - **Size:** ~200 bytes
  - **Updates:** Infrequent, atomic
  
- **Insurance info** (single object)
  - **Why:** Billing context, accessed with profile
  - **Size:** ~300 bytes
  - **Updates:** Periodic (annually)

**Referenced:**
- **preferred_hospital** → `hospitals`
  - **Why:** Shared entity, hospital info updated independently
  - **Size:** Hospital data is large (2-5KB)
  - **Consistency:** Single source of truth
  - **Reuse:** Same hospital referenced by many patients

#### **7.2.3 `doctor_profiles` Collection**

**Embedded:**
- **Qualifications array** (degrees, institutions)
  - **Why:** Fixed list (3-10 degrees), displayed on profile
  - **Size:** Small (~1KB)
  - **Updates:** Rare (degree earned)
  
- **Availability schedule** (weekly time slots)
  - **Why:** Core booking feature, checked frequently
  - **Size:** Fixed (7 days × 3-5 slots = ~1-2KB)
  - **Updates:** Weekly adjustments, update atomically
  - **Performance:** Fast reads for appointment booking
  
- **Awards array**
  - **Why:** Display content, small list
  - **Size:** <1KB typically
  - **Growth:** Slow, bounded

**Referenced:**
- **Hospitals** → `hospitals._id`
  - **Why:** Shared data (100+ doctors per hospital)
  - **Deduplication:** Prevent storing hospital address 100 times
  - **Updates:** Hospital info changes independently
  - **Many-to-many:** Doctor works at multiple hospitals

#### **7.2.4 `appointments` Collection**

**Embedded:**
- **Consultation details** (notes, diagnosis, vitals)
  - **Why:** Created once, never updated after completion
  - **Size:** ~2-3KB
  - **Access:** Displayed on appointment detail view
  - **Atomicity:** Entire consultation recorded together


- **Video call details** (room_id, URLs)
  - **Why:** Specific to this appointment, not reused
  - **Size:** ~500 bytes
  - **Lifecycle:** Created with appointment, not updated
  
- **Payment details** (amount, transaction_id)
  - **Why:** Financial audit trail, keep with appointment
  - **Size:** ~300 bytes
  - **Immutable:** Payment completed, never modified
  
- **Cancellation details** (if cancelled)
  - **Why:** Event specific to this appointment
  - **Size:** ~200 bytes
  - **One-time:** Cancelled once, never changed

**Referenced:**
- **patient_id, doctor_id** → `users._id`
  - **Why:** Core entities used everywhere
  - **Queries:** "Find all appointments for patient", "Doctor's schedule"
  - **Updates:** User info changes independently
  
- **prescription_id** → `prescriptions._id`
  - **Why:** Prescription may be updated independently
  - **Size:** Prescription can be large (multiple medications)
  - **Access:** Prescription viewed/printed separately
  
- **symptom_report_id** → `symptom_reports._id`
  - **Why:** Large document (10-15KB conversation history)
  - **Access:** Optional reference, not always needed

#### **7.2.5 `symptom_reports` Collection**

**Embedded:**
- **Conversation history** (messages array)
  - **Why:** Session replay requires complete conversation
  - **Size:** 20-50 messages (~10KB)
  - **Growth:** Bounded by session (max 100 messages)
  - **Access pattern:** "Show entire symptom checker session"
  - **Immutable:** Conversation history never edited
  
- **Symptoms array** (extracted symptoms)
  - **Why:** Specific to this session
  - **Size:** 5-15 symptoms (~2KB)
  - **Access:** Always viewed with AI assessment
  
- **AI assessment** (diagnoses, recommendations)
  - **Why:** Core output of session
  - **Size:** ~3-4KB
  - **Atomicity:** Generated together, stored together
  - **Access:** Displayed as complete report

**Referenced:**
- **appointment_id** → `appointments._id`
  - **Why:** Optional follow-up action
  - **Independence:** Appointment may not exist yet

#### **7.2.6 `medical_documents` Collection**

**Embedded:**
- **OCR data** (extracted text)
  - **Why:** Specific to this document, generated once
  - **Size:** ~2-5KB for typical report
  - **Immutable:** OCR processed once, never re-run
  - **Access:** Displayed with document
  
- **AI analysis** (lab_results, imaging_findings)
  - **Why:** Analysis specific to this document
  - **Size:** ~2-4KB
  - **Generated:** Once after upload
  - **Access:** Key feature - "Show me AI interpretation"
  
- **Shared_with array** (permissions)
  - **Why:** Document-specific access control
  - **Size:** Typically < 10 entries (~500 bytes)
  - **Updates:** Occasional sharing, atomic with document

**Not Stored (Cloud Storage):**
- **Actual file bytes**
  - **Why:** Binary files (1-10MB) exceed document limit
  - **Solution:** Store in S3/GCS, reference via `file_url`
  - **Performance:** CDN delivery for images/PDFs

#### **7.2.7 `prescriptions` Collection**

**Embedded:**
- **Medications array** (drugs, dosages, instructions)
  - **Why:** Core prescription content
  - **Size:** 1-10 medications (~2KB)
  - **Atomicity:** Entire prescription issued together
  - **Immutability:** Once signed, never edited (create new prescription)
  - **Legal:** Complete prescription must be intact for audit


**Referenced:**
- **patient_id, doctor_id, appointment_id**
  - **Why:** Links to core entities
  - **Queries:** "Patient's prescription history", "Doctor's prescriptions"

#### **7.2.8 `medications` Collection**

**Embedded:**
- **Schedule details** (frequency, time_slots, days)
  - **Why:** Core medication reminder logic
  - **Size:** ~500 bytes
  - **Updates:** Occasionally adjusted, update atomically
  
- **Adherence_log array** (taken/skipped history)
  - **Why:** Tracking specific to this medication
  - **Size:** 30-90 entries per month (~3-5KB)
  - **Growth:** Can trim old entries (keep last 90 days)
  - **Access:** "Show adherence for this medication"

**Referenced:**
- **patient_id** → `users._id`
  - **Queries:** "All active medications for patient"
  
- **prescription_id** → `prescriptions._id`
  - **Why:** Optional source tracking
  - **Independence:** Med may be manually added

**Design Note:**
- Separate collection (not embedded in patient_profiles) because:
  - Unbounded growth (patient may have 50+ medications over time)
  - Independent CRUD (add/update/delete individual medications)
  - Reminder system needs to query active medications independently

#### **7.2.9 `health_records` Collection**

**Embedded:**
- **Vitals object** (blood pressure, heart rate, etc.)
  - **Why:** Recorded together during measurement
  - **Size:** ~300 bytes
  - **Atomicity:** Complete vital sign set
  
- **Lab_test results array**
  - **Why:** Test results come as batch
  - **Size:** 10-30 parameters (~1-2KB)
  - **Access:** View complete lab report

**Referenced:**
- **patient_id** → `users._id`
  - **Queries:** "Patient's vital history", time-series analysis
  
- **appointment_id, recorded_by**
  - **Context:** Track where/who recorded

**Design Note:**
- Separate collection (not embedded in patient_profiles) because:
  - Very high volume (daily recordings)
  - Time-series data (need to query date ranges)
  - Analytics queries (trend analysis)
  - Would quickly exceed 16MB if embedded

#### **7.2.10 `ai_conversations` Collection**

**Embedded:**
- **Messages array** (complete chat history)
  - **Why:** Conversation replay requires all messages
  - **Size:** 20-100 messages (~10-15KB)
  - **Growth:** Bounded per conversation
  - **Access:** "Show chat history"
  
- **Context object** (patient background)
  - **Why:** Snapshot for this conversation
  - **Size:** ~500 bytes
  - **Immutable:** Context captured at conversation start

**Referenced:**
- **user_id** → `users._id`
  - **Queries:** "User's conversation history"

**Design Note:**
- Similar to symptom_reports but separate because:
  - Different use case (general chat vs symptom checking)
  - Different access patterns
  - Cleaner separation of concerns

#### **7.2.11 `notifications` Collection**

**Embedded:**
- **Delivery_status** (push/email/sms sent flags)
  - **Why:** Notification-specific delivery tracking
  - **Size:** ~150 bytes
  - **Updates:** Set once per channel

**Referenced:**
- **user_id** → `users._id`
  - **Queries:** "User's notifications", "Unread count"
  
- **related_entity** (entity_type, entity_id)
  - **Deep links:** Navigate to appointment/document

**Design Note:**
- Separate collection (not embedded in users) because:
  - Very high volume (100+ per user per month)
  - TTL cleanup (auto-delete old notifications)
  - Independent querying ("Show unread notifications")

#### **7.2.12 `hospitals` Collection**

**Embedded:**
- **Address object** (including geolocation)
  - **Why:** Single address per hospital
  - **Size:** ~400 bytes
  - **Geospatial:** GeoJSON point for maps
  
- **Facilities object** (ICU beds, pharmacy, etc.)
  - **Why:** Hospital characteristics
  - **Size:** ~300 bytes
  - **Updates:** Infrequent
  
- **Operating_hours array** (7 days)
  - **Why:** Fixed size (7 days)
  - **Size:** ~500 bytes
  - **Access:** Displayed on hospital profile

**Not Embedded:**
- **Doctor listings**
  - **Why:** Many-to-many (doctor works at multiple hospitals)
  - **Solution:** `doctor_profiles` references `hospital_id`
  - **Query:** "Doctors at this hospital" via index on doctor_profiles

---

## 8. Example JSON Documents

### 8.1 Complete Example: `users`

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "email": "john.smith@email.com",
  "password_hash": "$2b$12$KIXqMxJ5Y8Z9yGQxe7NqWe8vK9mJ.rL2pX4tN6sQ8wE2yU5oP3vHm",
  "role": "patient",
  "first_name": "John",
  "last_name": "Smith",
  "phone": "+14155552671",
  "date_of_birth": "1985-06-15T00:00:00.000Z",
  "gender": "male",
  "profile_picture_url": "https://storage.medinova.com/profiles/507f1f77bcf86cd799439011.jpg",
  "is_active": true,
  "is_email_verified": true,
  "is_phone_verified": true,
  "email_verification_token": null,
  "email_verification_expires": null,
  "password_reset_token": null,
  "password_reset_expires": null,
  "mfa_enabled": false,
  "mfa_secret": null,
  "failed_login_attempts": 0,
  "account_locked_until": null,
  "created_at": "2026-01-15T08:30:00.000Z",
  "updated_at": "2026-07-01T14:22:30.000Z",
  "last_login_at": "2026-07-03T09:15:00.000Z",
  "deleted_at": null
}
```


### 8.2 Complete Example: `patient_profiles`

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439012"),
  "user_id": ObjectId("507f1f77bcf86cd799439011"),
  "blood_group": "A+",
  "height_cm": 175.5,
  "weight_kg": 78.2,
  "bmi": 25.4,
  "allergies": [
    {
      "allergen": "Penicillin",
      "type": "drug",
      "severity": "severe",
      "reaction": "Anaphylaxis, difficulty breathing",
      "diagnosed_date": "2010-03-20T00:00:00.000Z",
      "notes": "Carry EpiPen at all times"
    },
    {
      "allergen": "Peanuts",
      "type": "food",
      "severity": "moderate",
      "reaction": "Hives, swelling",
      "diagnosed_date": "2005-08-10T00:00:00.000Z",
      "notes": "Avoid all peanut products"
    }
  ],
  "chronic_conditions": [
    {
      "condition": "Type 2 Diabetes Mellitus",
      "icd10_code": "E11.9",
      "diagnosed_date": "2020-05-12T00:00:00.000Z",
      "status": "controlled",
      "medications": ["Metformin 500mg", "Glipizide 5mg"],
      "notes": "Diet controlled, HbA1c 6.2%"
    },
    {
      "condition": "Hypertension",
      "icd10_code": "I10",
      "diagnosed_date": "2019-11-05T00:00:00.000Z",
      "status": "active",
      "medications": ["Lisinopril 10mg"],
      "notes": "Monitor blood pressure daily"
    }
  ],
  "past_surgeries": [
    {
      "surgery_name": "Appendectomy",
      "date": "2015-07-22T00:00:00.000Z",
      "hospital": "City General Hospital",
      "surgeon": "Dr. Robert Williams",
      "complications": "None",
      "notes": "Laparoscopic procedure, routine recovery"
    }
  ],
  "family_history": [
    {
      "condition": "Coronary Artery Disease",
      "relationship": "father",
      "age_of_onset": 58,
      "notes": "Heart attack at age 58, bypass surgery"
    },
    {
      "condition": "Breast Cancer",
      "relationship": "mother",
      "age_of_onset": 52,
      "notes": "Stage 2, treated successfully"
    }
  ],
  "emergency_contact": {
    "name": "Sarah Smith",
    "relationship": "spouse",
    "phone": "+14155552672",
    "email": "sarah.smith@email.com",
    "address": "123 Oak Street, San Francisco, CA 94102"
  },
  "insurance": {
    "provider": "Blue Cross Blue Shield",
    "policy_number": "BCBS123456789",
    "group_number": "GRP-987654",
    "expiry_date": "2027-12-31T00:00:00.000Z",
    "coverage_type": "PPO"
  },
  "preferences": {
    "preferred_hospital": ObjectId("507f1f77bcf86cd799439020"),
    "preferred_pharmacy": "CVS Pharmacy - Downtown",
    "language": "English",
    "communication_preference": "both"
  },
  "created_at": "2026-01-15T08:35:00.000Z",
  "updated_at": "2026-06-20T11:30:00.000Z",
  "last_health_check": "2026-06-15T10:00:00.000Z"
}
```

### 8.3 Complete Example: `doctor_profiles`

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439013"),
  "user_id": ObjectId("507f1f77bcf86cd799439014"),
  "license_number": "MD-CA-123456",
  "license_state": "California",
  "license_country": "United States",
  "license_expiry": "2028-12-31T00:00:00.000Z",
  "license_document_url": "https://storage.medinova.com/licenses/MD-CA-123456.pdf",
  "specialization": "Cardiology",
  "sub_specializations": ["Interventional Cardiology", "Cardiac Imaging"],
  "qualifications": [
    {
      "degree": "MBBS",
      "institution": "Stanford University School of Medicine",
      "year": 2010,
      "country": "United States"
    },
    {
      "degree": "MD - Cardiology",
      "institution": "Johns Hopkins Hospital",
      "year": 2014,
      "country": "United States"
    },
    {
      "degree": "Fellowship - Interventional Cardiology",
      "institution": "Cleveland Clinic",
      "year": 2016,
      "country": "United States"
    }
  ],
  "years_of_experience": 12,
  "total_consultations": 2847,
  "consultation_fee": 150,
  "consultation_duration": 30,
  "accepts_insurance": true,
  "languages_spoken": ["English", "Spanish"],
  "bio": "Board-certified cardiologist with over 12 years of experience in interventional cardiology. Specializes in complex coronary interventions, structural heart disease, and preventive cardiology. Committed to providing personalized, evidence-based care.",
  "primary_hospital_id": ObjectId("507f1f77bcf86cd799439020"),
  "affiliated_hospitals": [
    {
      "hospital_id": ObjectId("507f1f77bcf86cd799439020"),
      "position": "Senior Consultant",
      "department": "Cardiology",
      "since": "2016-08-01T00:00:00.000Z"
    },
    {
      "hospital_id": ObjectId("507f1f77bcf86cd799439021"),
      "position": "Visiting Consultant",
      "department": "Cardiovascular Surgery",
      "since": "2019-03-15T00:00:00.000Z"
    }
  ],
  "availability": [
    {
      "day": "monday",
      "is_available": true,
      "time_slots": [
        { "start_time": "09:00", "end_time": "13:00", "slot_duration": 30 },
        { "start_time": "14:00", "end_time": "17:00", "slot_duration": 30 }
      ]
    },
    {
      "day": "tuesday",
      "is_available": true,
      "time_slots": [
        { "start_time": "09:00", "end_time": "13:00", "slot_duration": 30 }
      ]
    },
    {
      "day": "wednesday",
      "is_available": true,
      "time_slots": [
        { "start_time": "09:00", "end_time": "17:00", "slot_duration": 30 }
      ]
    },
    {
      "day": "thursday",
      "is_available": false,
      "time_slots": []
    },
    {
      "day": "friday",
      "is_available": true,
      "time_slots": [
        { "start_time": "09:00", "end_time": "13:00", "slot_duration": 30 }
      ]
    },
    {
      "day": "saturday",
      "is_available": false,
      "time_slots": []
    },
    {
      "day": "sunday",
      "is_available": false,
      "time_slots": []
    }
  ],
  "rating": 4.8,
  "review_count": 423,
  "is_verified": true,
  "verified_at": "2016-09-10T10:00:00.000Z",
  "verified_by": ObjectId("507f1f77bcf86cd799439100"),
  "is_accepting_patients": true,
  "awards": [
    {
      "title": "Top Doctor Award",
      "organization": "California Medical Association",
      "year": 2022,
      "description": "Recognized for excellence in patient care"
    }
  ],
  "created_at": "2016-08-01T08:00:00.000Z",
  "updated_at": "2026-07-01T09:30:00.000Z",
  "last_active_at": "2026-07-03T08:45:00.000Z"
}
```


### 8.4 Complete Example: `appointments`

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439030"),
  "appointment_number": "APT-20260703-1247",
  "patient_id": ObjectId("507f1f77bcf86cd799439011"),
  "doctor_id": ObjectId("507f1f77bcf86cd799439014"),
  "appointment_date": "2026-07-10T14:00:00.000Z",
  "duration_minutes": 30,
  "type": "video",
  "status": "scheduled",
  "reason": "Follow-up consultation for blood pressure management",
  "symptoms": ["Occasional headaches", "Fatigue"],
  "symptom_report_id": null,
  "consultation": null,
  "prescription_id": null,
  "video_call": {
    "room_id": "medinova-room-1247",
    "join_url_patient": "https://video.medinova.com/join/patient/abc123xyz",
    "join_url_doctor": "https://video.medinova.com/join/doctor/def456uvw",
    "recording_url": null,
    "duration_seconds": null
  },
  "payment": {
    "amount": 150,
    "currency": "USD",
    "status": "paid",
    "payment_method": "credit_card",
    "transaction_id": "txn_1234567890abcdef",
    "paid_at": "2026-07-03T10:30:00.000Z"
  },
  "cancellation": null,
  "reminders_sent": [
    {
      "type": "24h",
      "sent_at": "2026-07-09T14:00:00.000Z",
      "channel": "email"
    }
  ],
  "created_at": "2026-07-03T10:25:00.000Z",
  "updated_at": "2026-07-09T14:00:30.000Z",
  "completed_at": null
}
```

### 8.5 Complete Example: `symptom_reports`

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439040"),
  "session_id": "sym-sess-a1b2c3d4-e5f6-7890",
  "patient_id": ObjectId("507f1f77bcf86cd799439011"),
  "conversation": [
    {
      "timestamp": "2026-07-03T09:00:00.000Z",
      "speaker": "ai",
      "message": "Hello! I'm your AI health assistant. How can I help you today?",
      "intent": "greeting",
      "confidence": 1.0
    },
    {
      "timestamp": "2026-07-03T09:00:15.000Z",
      "speaker": "patient",
      "message": "I've been having chest pain for the last 2 days",
      "intent": "symptom_report",
      "confidence": 0.95
    },
    {
      "timestamp": "2026-07-03T09:00:20.000Z",
      "speaker": "ai",
      "message": "I understand you're experiencing chest pain. Can you describe the type of pain? Is it sharp, dull, burning, or pressure-like?",
      "intent": "symptom_clarification",
      "confidence": 0.92
    },
    {
      "timestamp": "2026-07-03T09:00:35.000Z",
      "speaker": "patient",
      "message": "It's more like a pressure feeling, especially when I'm active",
      "intent": "symptom_detail",
      "confidence": 0.89
    }
  ],
  "symptoms": [
    {
      "symptom": "Chest pain",
      "body_part": "chest",
      "severity": 7,
      "duration": "2 days",
      "frequency": "intermittent",
      "onset": "gradual",
      "triggers": ["physical activity", "climbing stairs"],
      "relievers": ["rest"],
      "location": "center of chest"
    },
    {
      "symptom": "Shortness of breath",
      "body_part": "chest",
      "severity": 5,
      "duration": "2 days",
      "frequency": "intermittent",
      "onset": "gradual",
      "triggers": ["physical activity"],
      "relievers": ["rest"],
      "location": null
    }
  ],
  "ai_assessment": {
    "urgency_level": "urgent",
    "urgency_score": 75,
    "diagnoses": [
      {
        "condition": "Angina Pectoris (Stable)",
        "icd10_code": "I20.9",
        "confidence": 0.72,
        "reasoning": "Chest pressure triggered by exertion and relieved by rest is characteristic of stable angina",
        "supporting_symptoms": ["Chest pain", "Exertional dyspnea"],
        "recommended_tests": ["ECG", "Cardiac enzyme test", "Stress test"]
      },
      {
        "condition": "Acute Coronary Syndrome",
        "icd10_code": "I24.9",
        "confidence": 0.18,
        "reasoning": "Cannot rule out ACS given chest pain characteristics",
        "supporting_symptoms": ["Chest pain"],
        "recommended_tests": ["ECG", "Troponin", "Coronary angiography"]
      }
    ],
    "recommendations": [
      "Seek immediate medical attention - visit ER or urgent care",
      "Do not drive yourself - call emergency services or have someone drive you",
      "Avoid physical exertion until evaluated by a cardiologist",
      "Have someone stay with you"
    ],
    "red_flags": [
      "Exertional chest pain suggesting cardiac origin",
      "Risk factors present (hypertension, diabetes)"
    ],
    "suggested_action": "urgent_care",
    "specialty_recommended": "Cardiology",
    "model_version": "medinova-symptom-ai-v2.3",
    "processed_at": "2026-07-03T09:05:00.000Z",
    "processing_time_ms": 1247
  },
  "status": "completed",
  "appointment_booked": true,
  "appointment_id": ObjectId("507f1f77bcf86cd799439030"),
  "created_at": "2026-07-03T09:00:00.000Z",
  "updated_at": "2026-07-03T09:10:00.000Z",
  "completed_at": "2026-07-03T09:05:30.000Z"
}
```

### 8.6 Complete Example: `medical_documents`

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439050"),
  "document_id": "doc-uuid-9876543210abcdef",
  "patient_id": ObjectId("507f1f77bcf86cd799439011"),
  "uploaded_by": ObjectId("507f1f77bcf86cd799439011"),
  "document_type": "lab_report",
  "title": "Complete Blood Count Test",
  "description": "Routine CBC test results",
  "file_name": "CBC_Test_2026-06-15.pdf",
  "file_size": 245760,
  "file_type": "application/pdf",
  "file_url": "https://storage.medinova.com/documents/507f1f77bcf86cd799439050.pdf",
  "thumbnail_url": "https://storage.medinova.com/thumbnails/507f1f77bcf86cd799439050.jpg",
  "document_date": "2026-06-15T00:00:00.000Z",
  "doctor_id": null,
  "appointment_id": null,
  "hospital_name": "Quest Diagnostics",
  "ocr_data": {
    "raw_text": "COMPLETE BLOOD COUNT\\nPatient: John Smith\\nDate: 06/15/2026\\n\\nParameter | Result | Unit | Reference Range\\nHemoglobin | 14.2 | g/dL | 13.5-17.5\\nRBC Count | 4.8 | million/μL | 4.5-5.5\\nWBC Count | 7.2 | thousand/μL | 4.5-11.0\\nPlatelet Count | 245 | thousand/μL | 150-400",
    "confidence": 0.94,
    "language": "en",
    "processed_at": "2026-06-20T10:15:00.000Z",
    "processing_time_ms": 3420
  },
  "ai_analysis": {
    "lab_results": [
      {
        "parameter": "Hemoglobin",
        "value": 14.2,
        "unit": "g/dL",
        "reference_range": "13.5-17.5",
        "is_abnormal": false,
        "abnormality_type": null,
        "interpretation": "Normal hemoglobin levels"
      },
      {
        "parameter": "RBC Count",
        "value": 4.8,
        "unit": "million/μL",
        "reference_range": "4.5-5.5",
        "is_abnormal": false,
        "abnormality_type": null,
        "interpretation": "Normal red blood cell count"
      },
      {
        "parameter": "WBC Count",
        "value": 7.2,
        "unit": "thousand/μL",
        "reference_range": "4.5-11.0",
        "is_abnormal": false,
        "abnormality_type": null,
        "interpretation": "Normal white blood cell count"
      },
      {
        "parameter": "Platelet Count",
        "value": 245,
        "unit": "thousand/μL",
        "reference_range": "150-400",
        "is_abnormal": false,
        "abnormality_type": null,
        "interpretation": "Normal platelet count"
      }
    ],
    "imaging_findings": null,
    "medications_extracted": null,
    "model_version": "medinova-ocr-ai-v1.8",
    "processed_at": "2026-06-20T10:15:30.000Z",
    "confidence": 0.91
  },
  "shared_with": [],
  "tags": ["blood_test", "routine_checkup", "2026"],
  "category": "reports",
  "is_sensitive": false,
  "encryption_key_id": null,
  "uploaded_at": "2026-06-20T10:00:00.000Z",
  "created_at": "2026-06-20T10:00:00.000Z",
  "updated_at": "2026-06-20T10:15:30.000Z",
  "deleted_at": null
}
```


### 8.7 Complete Example: `prescriptions`

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439060"),
  "prescription_number": "RX-20260710-0842",
  "patient_id": ObjectId("507f1f77bcf86cd799439011"),
  "doctor_id": ObjectId("507f1f77bcf86cd799439014"),
  "appointment_id": ObjectId("507f1f77bcf86cd799439030"),
  "prescribed_date": "2026-07-10T14:30:00.000Z",
  "valid_until": "2026-08-10T14:30:00.000Z",
  "medications": [
    {
      "drug_name": "Lisinopril",
      "generic_name": "Lisinopril",
      "dosage": "10mg",
      "frequency": "Once daily",
      "duration_days": 30,
      "quantity": 30,
      "instructions": "Take in the morning with water",
      "route": "oral",
      "form": "tablet"
    },
    {
      "drug_name": "Metformin",
      "generic_name": "Metformin Hydrochloride",
      "dosage": "500mg",
      "frequency": "Twice daily",
      "duration_days": 30,
      "quantity": 60,
      "instructions": "Take with meals to reduce stomach upset",
      "route": "oral",
      "form": "tablet"
    },
    {
      "drug_name": "Aspirin",
      "generic_name": "Acetylsalicylic Acid",
      "dosage": "81mg",
      "frequency": "Once daily",
      "duration_days": 30,
      "quantity": 30,
      "instructions": "Take after dinner",
      "route": "oral",
      "form": "tablet"
    }
  ],
  "diagnosis": "Hypertension with Type 2 Diabetes Mellitus",
  "general_instructions": "Continue current medication regimen. Monitor blood pressure daily and blood glucose twice daily. Report any unusual symptoms immediately.",
  "precautions": "Avoid alcohol consumption. Stay hydrated. Do not stop medications without consulting doctor.",
  "diet_restrictions": "Low sodium diet (< 2000mg/day). Avoid sugary foods and beverages. Maintain consistent carbohydrate intake.",
  "follow_up_required": true,
  "follow_up_date": "2026-08-10T14:00:00.000Z",
  "follow_up_notes": "Check blood pressure control and review lab results",
  "status": "signed",
  "signed": true,
  "signed_at": "2026-07-10T14:32:00.000Z",
  "signature_hash": "8f4e33f3dc3e414ff94e5fb6905cba8c",
  "pharmacy_name": null,
  "pharmacy_filled": false,
  "filled_at": null,
  "created_at": "2026-07-10T14:30:00.000Z",
  "updated_at": "2026-07-10T14:32:00.000Z"
}
```

### 8.8 Complete Example: `medications`

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439070"),
  "patient_id": ObjectId("507f1f77bcf86cd799439011"),
  "medicine_name": "Lisinopril",
  "generic_name": "Lisinopril",
  "dosage": "10mg",
  "form": "tablet",
  "schedule": {
    "frequency": "daily",
    "times_per_day": 1,
    "time_slots": [
      {
        "time": "08:00",
        "with_meal": "before"
      }
    ],
    "days_of_week": null,
    "start_date": "2026-07-10T00:00:00.000Z",
    "end_date": "2026-08-10T00:00:00.000Z",
    "is_ongoing": false
  },
  "instructions": "Take in the morning with water",
  "special_instructions": "Monitor blood pressure 30 minutes after taking",
  "initial_quantity": 30,
  "current_quantity": 23,
  "refill_reminder_at": 5,
  "last_refilled_date": "2026-07-10T00:00:00.000Z",
  "adherence_log": [
    {
      "scheduled_time": "2026-07-10T08:00:00.000Z",
      "taken": true,
      "taken_at": "2026-07-10T08:05:00.000Z",
      "skipped": false,
      "skip_reason": null,
      "noted_by": "user"
    },
    {
      "scheduled_time": "2026-07-11T08:00:00.000Z",
      "taken": true,
      "taken_at": "2026-07-11T08:10:00.000Z",
      "skipped": false,
      "skip_reason": null,
      "noted_by": "user"
    },
    {
      "scheduled_time": "2026-07-12T08:00:00.000Z",
      "taken": false,
      "taken_at": null,
      "skipped": true,
      "skip_reason": "Forgot to take",
      "noted_by": "user"
    }
  ],
  "reminder_enabled": true,
  "reminder_advance_minutes": 15,
  "reminder_channels": ["push", "email"],
  "prescribed_by": ObjectId("507f1f77bcf86cd799439014"),
  "prescription_id": ObjectId("507f1f77bcf86cd799439060"),
  "is_active": true,
  "paused": false,
  "pause_reason": null,
  "created_at": "2026-07-10T14:35:00.000Z",
  "updated_at": "2026-07-12T08:15:00.000Z",
  "completed_at": null
}
```

### 8.9 Complete Example: `health_records`

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439080"),
  "patient_id": ObjectId("507f1f77bcf86cd799439011"),
  "record_type": "vitals",
  "recorded_at": "2026-07-03T08:00:00.000Z",
  "vitals": {
    "blood_pressure_systolic": 128,
    "blood_pressure_diastolic": 82,
    "heart_rate": 72,
    "respiratory_rate": 16,
    "oxygen_saturation": 98,
    "temperature": 37.2,
    "temperature_location": "oral",
    "weight": 78.2,
    "height": 175.5,
    "bmi": 25.4,
    "blood_glucose": 105
  },
  "lab_test": null,
  "diagnosis": null,
  "note": null,
  "recorded_by": ObjectId("507f1f77bcf86cd799439011"),
  "source": "manual",
  "device_name": null,
  "appointment_id": null,
  "created_at": "2026-07-03T08:00:00.000Z",
  "updated_at": "2026-07-03T08:00:00.000Z"
}
```

### 8.10 Complete Example: `ai_conversations`

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439090"),
  "conversation_id": "conv-uuid-123abc456def",
  "user_id": ObjectId("507f1f77bcf86cd799439011"),
  "type": "health_advice",
  "messages": [
    {
      "message_id": "msg-001",
      "timestamp": "2026-07-02T15:30:00.000Z",
      "role": "user",
      "content": "What are the best exercises for managing diabetes?",
      "model": null,
      "tokens_used": null,
      "latency_ms": null,
      "message_type": "text",
      "attachments": []
    },
    {
      "message_id": "msg-002",
      "timestamp": "2026-07-02T15:30:03.000Z",
      "role": "assistant",
      "content": "For managing Type 2 Diabetes, I recommend the following exercises:\n\n1. **Aerobic Exercise** (30 minutes, 5 days/week):\n   - Brisk walking\n   - Swimming\n   - Cycling\n   - Dancing\n\n2. **Resistance Training** (2-3 days/week):\n   - Light weights\n   - Resistance bands\n   - Bodyweight exercises\n\n3. **Flexibility & Balance**:\n   - Yoga\n   - Tai Chi\n   - Stretching\n\n**Important Tips:**\n- Check blood glucose before and after exercise\n- Stay hydrated\n- Start slowly and increase intensity gradually\n- Exercise at the same time each day\n\nAlways consult with your doctor before starting a new exercise program.",
      "model": "gpt-4",
      "tokens_used": 287,
      "latency_ms": 2840,
      "message_type": "text",
      "attachments": []
    }
  ],
  "context": {
    "patient_age": 41,
    "patient_gender": "male",
    "chronic_conditions": ["Type 2 Diabetes Mellitus", "Hypertension"],
    "current_medications": ["Metformin", "Lisinopril"],
    "known_allergies": ["Penicillin", "Peanuts"]
  },
  "summary": "Patient seeking exercise recommendations for diabetes management. Provided comprehensive exercise plan including aerobic, resistance, and flexibility training with safety precautions.",
  "key_points": [
    "Recommended 30 minutes aerobic exercise 5 days/week",
    "Suggested resistance training 2-3 days/week",
    "Emphasized importance of blood glucose monitoring during exercise",
    "Advised consulting doctor before starting new program"
  ],
  "symptom_report_id": null,
  "appointment_id": null,
  "status": "completed",
  "started_at": "2026-07-02T15:30:00.000Z",
  "last_message_at": "2026-07-02T15:30:03.000Z",
  "ended_at": "2026-07-02T15:35:00.000Z",
  "created_at": "2026-07-02T15:30:00.000Z",
  "updated_at": "2026-07-02T15:35:00.000Z"
}
```


### 8.11 Complete Example: `notifications`

```json
{
  "_id": ObjectId("507f1f77bcf86cd7994390a0"),
  "user_id": ObjectId("507f1f77bcf86cd799439011"),
  "type": "medication",
  "category": "info",
  "title": "Time to Take Your Medicine",
  "message": "It's time to take Lisinopril 10mg. Take with water before breakfast.",
  "priority": "high",
  "is_read": false,
  "read_at": null,
  "action_url": "/medications/507f1f77bcf86cd799439070",
  "action_text": "Mark as Taken",
  "related_entity": {
    "entity_type": "medication",
    "entity_id": ObjectId("507f1f77bcf86cd799439070")
  },
  "channels": ["push", "sms"],
  "delivery_status": {
    "push_sent": true,
    "push_sent_at": "2026-07-03T07:45:00.000Z",
    "email_sent": false,
    "email_sent_at": null,
    "sms_sent": true,
    "sms_sent_at": "2026-07-03T07:45:00.000Z"
  },
  "scheduled_for": "2026-07-03T07:45:00.000Z",
  "expires_at": "2026-07-03T09:00:00.000Z",
  "created_at": "2026-07-03T07:45:00.000Z",
  "updated_at": "2026-07-03T07:45:00.000Z"
}
```

### 8.12 Complete Example: `hospitals`

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439020"),
  "hospital_id": "hosp-uuid-sf-general-001",
  "name": "San Francisco General Hospital",
  "type": "hospital",
  "phone": "+14152062000",
  "email": "info@sfgeneral.org",
  "website": "https://www.sfgeneral.org",
  "address": {
    "street": "1001 Potrero Avenue",
    "city": "San Francisco",
    "state": "California",
    "country": "United States",
    "postal_code": "94110",
    "location": {
      "type": "Point",
      "coordinates": [-122.4044, 37.7562]
    }
  },
  "services": [
    "Emergency Services",
    "ICU",
    "Cardiology",
    "Neurology",
    "Orthopedics",
    "Radiology",
    "Laboratory",
    "Pharmacy"
  ],
  "specialties": [
    "Cardiology",
    "Neurology",
    "Oncology",
    "Pediatrics",
    "Emergency Medicine",
    "Trauma Care"
  ],
  "facilities": {
    "emergency_services": true,
    "icu_beds": 45,
    "general_beds": 284,
    "operation_theaters": 12,
    "pharmacy": true,
    "laboratory": true,
    "ambulance_service": true,
    "parking_available": true
  },
  "operating_hours": [
    {
      "day": "monday",
      "open_time": "00:00",
      "close_time": "23:59",
      "is_24_7": true
    },
    {
      "day": "tuesday",
      "open_time": "00:00",
      "close_time": "23:59",
      "is_24_7": true
    },
    {
      "day": "wednesday",
      "open_time": "00:00",
      "close_time": "23:59",
      "is_24_7": true
    },
    {
      "day": "thursday",
      "open_time": "00:00",
      "close_time": "23:59",
      "is_24_7": true
    },
    {
      "day": "friday",
      "open_time": "00:00",
      "close_time": "23:59",
      "is_24_7": true
    },
    {
      "day": "saturday",
      "open_time": "00:00",
      "close_time": "23:59",
      "is_24_7": true
    },
    {
      "day": "sunday",
      "open_time": "00:00",
      "close_time": "23:59",
      "is_24_7": true
    }
  ],
  "insurance_accepted": [
    "Blue Cross Blue Shield",
    "Aetna",
    "Cigna",
    "UnitedHealthcare",
    "Medicare",
    "Medicaid"
  ],
  "rating": 4.5,
  "review_count": 1247,
  "is_verified": true,
  "verified_at": "2020-01-15T00:00:00.000Z",
  "is_active": true,
  "created_at": "2020-01-15T00:00:00.000Z",
  "updated_at": "2026-06-01T10:00:00.000Z"
}
```

### 8.13 Complete Example: `analytics_events`

```json
{
  "_id": ObjectId("507f1f77bcf86cd7994390b0"),
  "user_id": ObjectId("507f1f77bcf86cd799439011"),
  "event_type": "feature_use",
  "event_name": "symptom_checker_started",
  "event_data": {
    "session_id": "sym-sess-a1b2c3d4-e5f6-7890",
    "entry_point": "dashboard_quick_action",
    "user_role": "patient"
  },
  "session_id": "sess-webapp-xyz789",
  "device": {
    "type": "desktop",
    "os": "Windows 11",
    "browser": "Chrome 126",
    "app_version": "2.1.0"
  },
  "ip_address": "192.168.1.100",
  "country": "United States",
  "city": "San Francisco",
  "timestamp": "2026-07-03T09:00:00.000Z",
  "created_at": "2026-07-03T09:00:00.000Z"
}
```

### 8.14 Complete Example: `admin_audit_logs`

```json
{
  "_id": ObjectId("507f1f77bcf86cd7994390c0"),
  "admin_id": ObjectId("507f1f77bcf86cd799439100"),
  "action": "doctor_verified",
  "action_category": "user_management",
  "target_type": "doctor",
  "target_id": ObjectId("507f1f77bcf86cd799439014"),
  "changes": {
    "before": {
      "is_verified": false,
      "verified_at": null,
      "verified_by": null
    },
    "after": {
      "is_verified": true,
      "verified_at": "2016-09-10T10:00:00.000Z",
      "verified_by": ObjectId("507f1f77bcf86cd799439100")
    }
  },
  "ip_address": "10.0.0.50",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "success": true,
  "error_message": null,
  "timestamp": "2016-09-10T10:00:00.000Z",
  "created_at": "2016-09-10T10:00:00.000Z"
}
```

---

## 9. Data Optimization Strategy

### 9.1 Document Size Optimization

**Target Document Sizes:**
- Small: < 1 KB (notifications, analytics_events)
- Medium: 1-10 KB (users, appointments, prescriptions)
- Large: 10-100 KB (patient_profiles, doctor_profiles, symptom_reports)
- Extra Large: 100KB-1MB (ai_conversations with long history)

**Optimization Techniques:**

**1. Field Name Abbreviation (for high-volume collections):**
```javascript
// Instead of:
{ "blood_pressure_systolic": 120 }

// Consider (only for analytics_events):
{ "bp_sys": 120 }
```
- Saves ~20 bytes per document
- For 1M documents = 20MB saved
- Only use for extremely high-volume collections

**2. Null vs Undefined vs Omit:**
```javascript
// Worst (stores null):
{ "optional_field": null }  // +20 bytes

// Better (omit field):
{ }  // +0 bytes

// MongoDB handles missing fields gracefully
```

**3. Array Trimming:**
```javascript
// medications.adherence_log - Keep only last 90 days
db.medications.updateMany({}, [
  {
    $set: {
      adherence_log: {
        $slice: ["$adherence_log", -90]
      }
    }
  }
])
```

**4. Archival Strategy:**
- Move completed conversations older than 6 months to `ai_conversations_archive`
- Archive appointments > 1 year to `appointments_archive`
- Keep hot data < 10% of total data size

### 9.2 Query Optimization

**1. Projection - Fetch Only Needed Fields:**
```javascript
// Bad - Fetches entire 15KB document:
db.patient_profiles.find({ user_id: userId })

// Good - Fetches only needed data:
db.patient_profiles.find(
  { user_id: userId },
  { blood_group: 1, allergies: 1, chronic_conditions: 1 }
)
```

**2. Covered Queries:**
```javascript
// Query + Projection covered by index:
db.users.createIndex({ email: 1, role: 1, is_active: 1 })

db.users.find(
  { email: "user@email.com" },
  { role: 1, is_active: 1, _id: 0 }
)
// IXSCAN only, no document fetch
```

**3. Aggregation Pipeline Optimization:**
```javascript
// Bad - Match after lookup:
db.appointments.aggregate([
  { $lookup: { ... } },
  { $match: { status: "scheduled" } }  // Late filtering
])

// Good - Filter early:
db.appointments.aggregate([
  { $match: { status: "scheduled" } },  // Early filtering
  { $lookup: { ... } }
])
```

### 9.3 Connection Pooling

**FastAPI MongoDB Settings:**
```python
# Optimal settings for MongoDB Atlas
client = AsyncIOMotorClient(
    connection_string,
    maxPoolSize=50,           # Max connections
    minPoolSize=10,           # Keep warm connections
    maxIdleTimeMS=30000,      # 30 seconds
    waitQueueTimeoutMS=5000,  # 5 seconds
    serverSelectionTimeoutMS=5000
)
```


### 9.4 Write Optimization

**1. Bulk Operations:**
```javascript
// Bad - 100 individual writes:
for (let i = 0; i < 100; i++) {
  await db.notifications.insertOne(notifications[i])
}

// Good - Single bulk write:
await db.notifications.insertMany(notifications, { ordered: false })
```

**2. Update Operators (avoid full document replacement):**
```javascript
// Bad - Full document update:
const user = await db.users.findOne({ _id: userId })
user.last_login_at = new Date()
await db.users.replaceOne({ _id: userId }, user)

// Good - Field update only:
await db.users.updateOne(
  { _id: userId },
  { $set: { last_login_at: new Date() } }
)
```

**3. Write Concern:**
```javascript
// For critical data (prescriptions, payments):
await db.prescriptions.insertOne(doc, { writeConcern: { w: "majority" } })

// For analytics (acceptable data loss):
await db.analytics_events.insertOne(doc, { writeConcern: { w: 1 } })
```

### 9.5 Read Optimization

**1. Read Preference:**
```javascript
// Critical reads (appointments, prescriptions):
readPreference: "primary"

// Analytics, reports (can use secondaries):
readPreference: "secondaryPreferred"
```

**2. Cursor Batching:**
```javascript
// Fetch in batches instead of loading all:
const cursor = db.health_records.find({ patient_id: userId })
  .sort({ recorded_at: -1 })
  .batchSize(100)
```

**3. Caching Strategy:**
```python
# Cache doctor profiles (rarely change):
@cache(ttl=3600)  # 1 hour
async def get_doctor_profile(doctor_id):
    return await db.doctor_profiles.find_one({"_id": doctor_id})

# Cache hospital data (rarely change):
@cache(ttl=7200)  # 2 hours
async def get_hospital(hospital_id):
    return await db.hospitals.find_one({"_id": hospital_id})

# Don't cache appointments (frequently change):
async def get_appointments(patient_id):
    return await db.appointments.find({"patient_id": patient_id})
```

### 9.6 Storage Optimization

**1. Document Compression:**
- MongoDB WiredTiger default: Snappy compression
- ~60-70% compression ratio
- Enable at collection level:
```javascript
db.createCollection("analytics_events", {
  storageEngine: {
    wiredTiger: {
      configString: "block_compressor=zstd"  // Better compression
    }
  }
})
```

**2. Index Compression:**
- Prefix compression for string indexes
- Reduces index size by ~50%
- Automatic in MongoDB 3.0+

**3. File Storage Externalization:**
- Store files > 100KB in cloud storage (S3/GCS)
- Store only metadata + URL in MongoDB
- Reduces database size, improves query performance

**4. TTL Optimization:**
- Auto-delete old notifications (90 days)
- Archive old analytics events (180 days)
- Keeps working set small

---

## 10. Scalability Considerations

### 10.1 Vertical Scaling (MongoDB Atlas Tiers)

**Development Phase:**
- **Tier:** M10 (2GB RAM, 10GB Storage)
- **Users:** Up to 1,000 concurrent
- **Cost:** ~$57/month

**Production Launch:**
- **Tier:** M30 (8GB RAM, 100GB Storage)
- **Users:** Up to 10,000 concurrent
- **Cost:** ~$380/month

**Growth Phase (Year 2):**
- **Tier:** M50 (16GB RAM, 500GB Storage)
- **Users:** Up to 50,000 concurrent
- **Cost:** ~$760/month

### 10.2 Horizontal Scaling (Sharding)

**When to Shard:**
- Database size > 500GB
- Single collection > 100GB
- Query throughput > 10,000 ops/sec

**Sharding Strategy:**

**1. Collections to Shard:**

**`appointments` - Shard by patient_id:**
```javascript
sh.shardCollection("medinova_db.appointments", { patient_id: "hashed" })
```
- **Why:** Evenly distributes patient appointments
- **Query pattern:** Most queries filter by patient_id
- **Growth:** High write volume

**`health_records` - Shard by patient_id + recorded_at:**
```javascript
sh.shardCollection(
  "medinova_db.health_records",
  { patient_id: 1, recorded_at: 1 }
)
```
- **Why:** Time-series data, range queries by date
- **Locality:** Patient's data stays together
- **Growth:** Very high volume (daily recordings)

**`symptom_reports` - Shard by patient_id:**
```javascript
sh.shardCollection("medinova_db.symptom_reports", { patient_id: "hashed" })
```
- **Why:** Distribute AI workload
- **Growth:** Highest write volume collection

**`analytics_events` - Shard by user_id:**
```javascript
sh.shardCollection("medinova_db.analytics_events", { user_id: "hashed" })
```
- **Why:** Event tracking, very high volume
- **Benefit:** Distribute across shards evenly

**2. Collections NOT to Shard:**
- `users` - Small, frequent access, use replica reads
- `doctor_profiles` - Small collection (< 10K documents)
- `hospitals` - Very small (< 1K documents)
- `prescriptions` - Moderate size, manageable

### 10.3 Replica Set Configuration

**Standard Configuration:**
```javascript
{
  "_id": "medinova-rs",
  "members": [
    { "_id": 0, "host": "primary:27017", "priority": 2 },
    { "_id": 1, "host": "secondary1:27017", "priority": 1 },
    { "_id": 2, "host": "secondary2:27017", "priority": 1 }
  ]
}
```

**Read Distribution:**
- **Primary:** Critical writes, real-time reads (appointments, prescriptions)
- **Secondaries:** Analytics queries, reports, backups
- **Arbiter:** Only if cost-constrained (not recommended)

### 10.4 Data Growth Projections

**Year 1 (10,000 users):**
- Users: 10,000 × 5KB = 50 MB
- Patient Profiles: 6,000 × 15KB = 90 MB
- Appointments: 50,000 × 8KB = 400 MB
- Symptom Reports: 30,000 × 10KB = 300 MB
- Medical Documents: 20,000 × 3KB = 60 MB
- Health Records: 1M × 2KB = 2 GB
- AI Conversations: 40,000 × 12KB = 480 MB
- Notifications: 500K × 1KB = 500 MB
- Analytics: 2M × 2KB = 4 GB
- **Total:** ~8 GB

**Year 3 (100,000 users):**
- Linear scaling × 10 = ~80 GB
- With indexes = ~120 GB

**Year 5 (500,000 users):**
- Linear scaling × 50 = ~400 GB
- With indexes + overhead = ~600 GB

### 10.5 Performance Targets

**Read Performance:**
- Simple queries: < 10ms (p95)
- Complex aggregations: < 100ms (p95)
- Full-text search: < 50ms (p95)

**Write Performance:**
- Single document insert: < 5ms (p95)
- Bulk inserts (100 docs): < 50ms (p95)
- Updates: < 10ms (p95)

**Monitoring:**
```javascript
// Slow query logging (MongoDB Atlas):
db.setProfilingLevel(1, { slowms: 100 })

// Monitor with Atlas Performance Advisor
// Alert on:
// - Query time > 100ms
// - Index scan ratio < 0.9
// - Connection pool exhaustion
```

### 10.6 Capacity Planning

**Working Set Size:**
- Target: 50% of RAM
- MongoDB working set = frequently accessed data + indexes
- For M30 (8GB RAM): Keep working set < 4GB

**Index Size Management:**
- Monitor: Index size should be < 20% of data size
- Rule: Total indexes fit in RAM for optimal performance
- Strategy: Drop unused indexes quarterly

**Connection Scaling:**
- Formula: connections = (users × 0.1) + background_jobs
- Example: 10K users = 1,000 connections + 50 jobs = 1,050 connections
- MongoDB default: 65,536 max connections

---

## 11. Security Considerations

### 11.1 Authentication & Authorization

**MongoDB Authentication:**
```javascript
// Enable authentication (MongoDB Atlas default)
use admin
db.createUser({
  user: "medinova_app",
  pwd: "<strong_password>",
  roles: [
    { role: "readWrite", db: "medinova_db" }
  ]
})
```

**Role-Based Access Control (RBAC):**
```javascript
// Application user (FastAPI backend):
{ role: "readWrite", db: "medinova_db" }

// Analytics user (read-only):
{ role: "read", db: "medinova_db" }

// Admin user (full access):
{ role: "dbOwner", db: "medinova_db" }

// Backup user:
{ role: "backup", db: "admin" }
```

### 11.2 Data Encryption

**Encryption at Rest:**
- **MongoDB Atlas:** Automatic encryption (AES-256)
- **Cloud Provider:** AWS KMS / GCP Cloud KMS
- **Key Rotation:** Every 90 days

**Encryption in Transit:**
- **TLS/SSL:** Enforce TLS 1.2+ for all connections
- **Certificate Validation:** Verify server certificate

```python
# FastAPI connection with TLS:
client = AsyncIOMotorClient(
    connection_string,
    tls=True,
    tlsCAFile="/path/to/ca.pem"
)
```

**Field-Level Encryption:**
```javascript
// Encrypt sensitive fields in application:
// - users.mfa_secret
// - patient_profiles.insurance.policy_number
// - medical_documents (if storing diagnosis)

// Use MongoDB Client-Side Field Level Encryption (CSFLE)
```

### 11.3 Data Privacy (HIPAA Compliance)

**PHI (Protected Health Information) Fields:**
- `users`: first_name, last_name, email, phone, date_of_birth
- `patient_profiles`: All medical history, emergency contact
- `medical_documents`: All content
- `health_records`: All vitals and test results
- `prescriptions`: All data

**Privacy Controls:**

**1. Access Logging:**
```javascript
// Log all PHI access in admin_audit_logs:
{
  admin_id: userId,
  action: "phi_accessed",
  target_type: "patient_profile",
  target_id: patientId,
  ip_address: requestIP,
  timestamp: new Date()
}
```

**2. Data Masking:**
```python
# Mask PHI in logs and responses:
def mask_email(email):
    name, domain = email.split('@')
    return f"{name[0]}***@{domain}"

# "john.smith@email.com" → "j***@email.com"
```

**3. Consent Management:**
```javascript
// Add to patient_profiles:
{
  consent: {
    data_sharing: boolean,
    marketing: boolean,
    research: boolean,
    given_at: ISODate,
    ip_address: String
  }
}
```

### 11.4 Input Validation & Injection Prevention

**NoSQL Injection Prevention:**
```python
# Bad - Vulnerable to injection:
query = { "email": request.email }  # If email = {"$ne": null}

# Good - Validate and sanitize:
from pydantic import EmailStr

class UserLogin(BaseModel):
    email: EmailStr  # Validates email format
    password: str

# Pydantic ensures email is string, not object
```

**Query Parameterization:**
```python
# Always use typed parameters:
user_id = ObjectId(user_id_string)  # Validates ObjectId format
db.users.find_one({"_id": user_id})  # Safe
```


### 11.5 Backup & Disaster Recovery

**Backup Strategy:**

**1. MongoDB Atlas Automated Backups:**
- **Frequency:** Continuous (point-in-time recovery)
- **Retention:** 7 days (configurable up to 365 days)
- **Type:** Full snapshot + oplog

**2. Backup Schedule:**
- **Continuous:** Oplog-based incremental
- **Daily:** Full snapshot at 2:00 AM UTC
- **Weekly:** Full backup retention for 4 weeks
- **Monthly:** Archive backup for 1 year

**3. Recovery Time Objectives (RTO):**
- **Critical data:** < 15 minutes
- **Standard data:** < 1 hour
- **Archived data:** < 4 hours

**4. Recovery Point Objectives (RPO):**
- **Production:** < 5 minutes (continuous backup)
- **Development:** 24 hours

**Disaster Recovery Plan:**

**Scenario 1: Single Document Corruption**
```javascript
// Restore from backup using point-in-time recovery:
// Atlas → Backup → Restore to point in time
// Then replace corrupted document
```

**Scenario 2: Collection Corruption**
```javascript
// Restore specific collection:
// 1. Export from backup
// 2. Drop corrupted collection
// 3. Import from backup
mongorestore --db medinova_db --collection users backup/users.bson
```

**Scenario 3: Complete Database Loss**
```javascript
// Restore entire cluster:
// Atlas → Automated restore to new cluster
// Update connection strings in application
// Estimated downtime: 15-30 minutes
```

### 11.6 Network Security

**IP Whitelist:**
```javascript
// MongoDB Atlas Network Access:
// - Application servers: 10.0.1.0/24
// - Admin access: <admin_ip>/32
// - Deny all other IPs
```

**VPC Peering (Production):**
```javascript
// Connect MongoDB Atlas to application VPC:
// - Private IP communication
// - No public internet exposure
// - Lower latency
```

**Firewall Rules:**
```javascript
// Allow only port 27017 from application subnet
// Block all other ports
// Enable DDoS protection
```

### 11.7 Audit Logging

**Enable MongoDB Audit Logs:**
```javascript
// Track all database operations:
{
  atype: "authenticate",
  ts: ISODate("2026-07-03T10:00:00.000Z"),
  local: { ip: "10.0.1.50", port: 27017 },
  remote: { ip: "10.0.2.100", port: 52431 },
  users: [{ user: "medinova_app", db: "medinova_db" }],
  result: 0  // Success
}
```

**Audit Events to Track:**
- Authentication attempts (success/failure)
- Admin operations (user creation, role changes)
- PHI access (patient record views)
- Data exports
- Schema changes
- Failed authorization attempts

**Retention:**
- Hot logs: 90 days (MongoDB Atlas)
- Archive logs: 7 years (HIPAA requirement)

### 11.8 Data Retention & Deletion

**Retention Policies:**

| Collection | Hot Storage | Archive | Delete After |
|------------|-------------|---------|--------------|
| users | Active + 2 years after deletion | 5 years | 7 years |
| patient_profiles | Active | Permanent | Never (unless requested) |
| appointments | 2 years | 5 years | 7 years |
| prescriptions | Active | Permanent | Never (legal requirement) |
| medical_documents | Active | Permanent | Never (unless requested) |
| health_records | 2 years | 5 years | 7 years |
| notifications | 90 days | N/A | 90 days (TTL) |
| analytics_events | 180 days | 2 years | 2 years |
| ai_conversations | 1 year | 3 years | 3 years |

**Right to Deletion (GDPR/CCPA):**
```python
async def delete_user_data(user_id: ObjectId):
    """
    Delete all user data upon request.
    Retain only what's legally required (prescriptions for 7 years).
    """
    # Soft delete user
    await db.users.update_one(
        {"_id": user_id},
        {
            "$set": {
                "deleted_at": datetime.utcnow(),
                "email": f"deleted_{user_id}@deleted.com",
                "first_name": "Deleted",
                "last_name": "User",
                "phone": None,
                "profile_picture_url": None
            }
        }
    )
    
    # Delete patient profile (except legally required parts)
    await db.patient_profiles.delete_one({"user_id": user_id})
    
    # Anonymize prescriptions (keep for legal, remove PII)
    await db.prescriptions.update_many(
        {"patient_id": user_id},
        {"$set": {"patient_name_deleted": True}}
    )
    
    # Delete conversations, symptom reports, etc.
    await db.ai_conversations.delete_many({"user_id": user_id})
    await db.symptom_reports.delete_many({"patient_id": user_id})
```

---

## 12. Entity Relationship Diagram

### 12.1 ER Diagram Explanation

**Core Entities:**

```
┌─────────────────────────────────────────────────────────────────┐
│                         USERS (Central)                         │
│  - Authentication & Basic Profile                               │
│  - _id, email, password_hash, role, name, phone                │
└──────────────────────┬──────────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌───────────────┐ ┌──────────────┐ ┌──────────────┐
│ PATIENT       │ │ DOCTOR       │ │ ADMIN        │
│ PROFILES      │ │ PROFILES     │ │ (role only)  │
│ - Medical     │ │ - Credentials│ └──────────────┘
│   History     │ │ - Schedule   │
│ - Allergies   │ │ - Hospitals  │
│ - Insurance   │ │ - Rating     │
└───────┬───────┘ └──────┬───────┘
        │                │
        └────────┬───────┘
                 │
                 ▼
        ┌─────────────────┐
        │  APPOINTMENTS   │
        │  - Date & Time  │
        │  - Status       │
        │  - Consultation │
        │  - Payment      │
        └────────┬────────┘
                 │
                 ├──────────────┐
                 ▼              ▼
        ┌─────────────┐  ┌─────────────┐
        │PRESCRIPTIONS│  │VIDEO CALL   │
        │- Medications│  │(embedded)   │
        │- Signature  │  └─────────────┘
        └─────────────┘
```

**Supporting Entities:**

```
┌──────────────┐        ┌─────────────────┐
│   SYMPTOM    │───────>│  APPOINTMENTS   │
│   REPORTS    │        │  (optional ref) │
│- AI Analysis │        └─────────────────┘
│- Conversation│
│- Urgency     │
└──────────────┘

┌──────────────┐        ┌─────────────────┐
│   MEDICAL    │        │  HEALTH         │
│  DOCUMENTS   │        │  RECORDS        │
│- OCR Data    │        │- Vitals         │
│- AI Analysis │        │- Lab Tests      │
│- File URL    │        │- Time Series    │
└──────────────┘        └─────────────────┘

┌──────────────┐        ┌─────────────────┐
│  MEDICATIONS │        │  AI             │
│- Schedule    │        │  CONVERSATIONS  │
│- Reminders   │        │- Messages       │
│- Adherence   │        │- Context        │
└──────────────┘        └─────────────────┘

┌──────────────┐        ┌─────────────────┐
│ HOSPITALS    │<───────│  DOCTOR         │
│- Location    │        │  PROFILES       │
│- Services    │        │  (references)   │
│- GeoJSON     │        └─────────────────┘
└──────────────┘

┌──────────────┐        ┌─────────────────┐
│NOTIFICATIONS │        │  ANALYTICS      │
│- Multi-      │        │  EVENTS         │
│  channel     │        │- Tracking       │
│- TTL         │        │- Session        │
└──────────────┘        └─────────────────┘
```

### 12.2 Relationship Cardinalities

**One-to-One (1:1):**
- `users` ↔ `patient_profiles` (patient_id references user_id)
- `users` ↔ `doctor_profiles` (doctor_id references user_id)
- `appointments` ↔ `prescriptions` (one prescription per appointment)

**One-to-Many (1:n):**
- `users` → `appointments` (user can have many appointments)
- `users` → `symptom_reports` (user can have many sessions)
- `users` → `medical_documents` (user uploads many documents)
- `users` → `health_records` (user records many vitals)
- `users` → `ai_conversations` (user has many conversations)
- `users` → `notifications` (user receives many notifications)
- `patient_profiles` → `medications` (patient takes many medications)
- `doctor_profiles` → `prescriptions` (doctor writes many prescriptions)
- `hospitals` → `doctor_profiles` (hospital has many doctors)

**Many-to-Many (m:n) - Resolved:**
- `patients` ↔ `doctors` (resolved through `appointments`)
  - A patient can see multiple doctors
  - A doctor can treat multiple patients
  - `appointments` acts as junction collection

### 12.3 Referential Integrity

**Foreign Key Relationships (Application-Enforced):**

```python
# MongoDB doesn't enforce FK constraints - application must validate

class AppointmentCreate(BaseModel):
    patient_id: ObjectId
    doctor_id: ObjectId
    
    @validator('patient_id')
    def validate_patient(cls, v):
        # Check patient exists and has role="patient"
        patient = db.users.find_one({"_id": v, "role": "patient"})
        if not patient:
            raise ValueError("Invalid patient_id")
        return v
    
    @validator('doctor_id')
    def validate_doctor(cls, v):
        # Check doctor exists, verified, and accepting patients
        doctor = db.doctor_profiles.find_one({
            "user_id": v,
            "is_verified": True,
            "is_accepting_patients": True
        })
        if not doctor:
            raise ValueError("Invalid or unavailable doctor")
        return v
```

**Cascade Delete Strategy:**

```python
async def delete_patient(user_id: ObjectId):
    """
    Cascade delete patient data (GDPR Right to Deletion)
    """
    # 1. Delete patient profile
    await db.patient_profiles.delete_one({"user_id": user_id})
    
    # 2. Anonymize (don't delete) appointments - doctor needs record
    await db.appointments.update_many(
        {"patient_id": user_id},
        {"$set": {"patient_anonymized": True}}
    )
    
    # 3. Delete symptom reports
    await db.symptom_reports.delete_many({"patient_id": user_id})
    
    # 4. Delete medical documents
    docs = await db.medical_documents.find({"patient_id": user_id})
    for doc in docs:
        # Delete from cloud storage
        await delete_from_s3(doc['file_url'])
    await db.medical_documents.delete_many({"patient_id": user_id})
    
    # 5. Keep prescriptions (legal requirement) but anonymize
    await db.prescriptions.update_many(
        {"patient_id": user_id},
        {"$set": {"patient_deleted": True}}
    )
    
    # 6. Delete health records
    await db.health_records.delete_many({"patient_id": user_id})
    
    # 7. Delete medications
    await db.medications.delete_many({"patient_id": user_id})
    
    # 8. Delete AI conversations
    await db.ai_conversations.delete_many({"user_id": user_id})
    
    # 9. Delete notifications
    await db.notifications.delete_many({"user_id": user_id})
    
    # 10. Soft delete user
    await db.users.update_one(
        {"_id": user_id},
        {
            "$set": {
                "deleted_at": datetime.utcnow(),
                "email": f"deleted_{user_id}@deleted.com"
            }
        }
    )
```

### 12.4 Data Flow Diagram

**Patient Journey - Data Creation Flow:**

```
1. USER REGISTRATION
   users (insert) → patient_profiles (insert)

2. SYMPTOM CHECKER
   ai_conversations (insert) → symptom_reports (insert)
   → notifications (insert: "Urgent - See doctor")

3. BOOK APPOINTMENT
   appointments (insert) → notifications (insert: confirmation)
   → notifications (insert: reminder 24h before)

4. CONSULTATION
   appointments (update: add consultation notes)
   → prescriptions (insert)
   → notifications (insert: "Prescription ready")

5. MEDICATION SETUP
   prescriptions → medications (insert with schedule)
   → notifications (insert: daily reminders)

6. UPLOAD REPORT
   medical_documents (insert) → OCR processing
   → medical_documents (update: add ai_analysis)
   → health_records (insert: extracted vitals)
   → notifications (insert: "Report analyzed")

7. TRACK VITALS
   health_records (insert: daily measurements)

8. ANALYTICS
   Every action → analytics_events (insert)
```

---

## 13. Collection to Module Mapping

### 13.1 Backend Module Structure

```
app/
├── modules/
│   ├── authentication/
│   │   ├── routes.py          # Login, register, password reset
│   │   └── collections: users
│   │
│   ├── patients/
│   │   ├── routes.py          # Patient profile management
│   │   └── collections: patient_profiles, health_records
│   │
│   ├── doctors/
│   │   ├── routes.py          # Doctor profile, schedule
│   │   └── collections: doctor_profiles, hospitals
│   │
│   ├── appointments/
│   │   ├── routes.py          # Booking, consultation
│   │   └── collections: appointments, prescriptions
│   │
│   ├── symptom_checker/
│   │   ├── routes.py          # AI symptom analysis
│   │   └── collections: symptom_reports, ai_conversations
│   │
│   ├── medical_documents/
│   │   ├── routes.py          # Upload, OCR, AI analysis
│   │   └── collections: medical_documents
│   │
│   ├── medications/
│   │   ├── routes.py          # Medication tracking, reminders
│   │   └── collections: medications, notifications
│   │
│   ├── hospital_finder/
│   │   ├── routes.py          # Geospatial search
│   │   └── collections: hospitals
│   │
│   ├── notifications/
│   │   ├── routes.py          # Notification delivery
│   │   └── collections: notifications
│   │
│   ├── analytics/
│   │   ├── routes.py          # Event tracking, dashboards
│   │   └── collections: analytics_events, health_records
│   │
│   └── admin/
│       ├── routes.py          # Admin operations
│       └── collections: users, doctor_profiles, admin_audit_logs
```


### 13.2 Detailed Module-Collection Mapping

#### **Module 1: Authentication**

**Primary Collections:**
- `users`

**Operations:**
- `POST /api/auth/register` → Insert into `users`
- `POST /api/auth/login` → Find in `users`, update `last_login_at`
- `POST /api/auth/forgot-password` → Update `password_reset_token` in `users`
- `POST /api/auth/reset-password` → Update `password_hash`, clear token in `users`
- `POST /api/auth/verify-email` → Update `is_email_verified` in `users`
- `POST /api/auth/logout` → No database operation (JWT invalidation)

**Key Queries:**
```python
# Login
user = await db.users.find_one({"email": email, "is_active": True})

# Password reset
await db.users.update_one(
    {"email": email},
    {"$set": {
        "password_reset_token": token,
        "password_reset_expires": expiry
    }}
)
```

---

#### **Module 2: Patient Management**

**Primary Collections:**
- `patient_profiles`
- `health_records`

**Operations:**
- `GET /api/patients/profile` → Find in `patient_profiles`
- `PUT /api/patients/profile` → Update `patient_profiles`
- `POST /api/patients/health-records` → Insert into `health_records`
- `GET /api/patients/health-records` → Find in `health_records` (time-series)
- `GET /api/patients/health-analytics` → Aggregate from `health_records`

**Key Queries:**
```python
# Get patient profile
profile = await db.patient_profiles.find_one({"user_id": user_id})

# Add allergy
await db.patient_profiles.update_one(
    {"user_id": user_id},
    {"$push": {"allergies": new_allergy}}
)

# Get vitals trend (last 30 days)
vitals = await db.health_records.find({
    "patient_id": user_id,
    "record_type": "vitals",
    "recorded_at": {"$gte": thirty_days_ago}
}).sort("recorded_at", -1)
```

---

#### **Module 3: Doctor Management**

**Primary Collections:**
- `doctor_profiles`
- `hospitals`

**Operations:**
- `GET /api/doctors/profile` → Find in `doctor_profiles`
- `PUT /api/doctors/profile` → Update `doctor_profiles`
- `GET /api/doctors/search` → Text search in `doctor_profiles`
- `GET /api/doctors/schedule` → Get `availability` from `doctor_profiles`
- `PUT /api/doctors/schedule` → Update `availability` in `doctor_profiles`

**Key Queries:**
```python
# Search doctors by specialty
doctors = await db.doctor_profiles.find({
    "specialization": {"$regex": specialty, "$options": "i"},
    "is_verified": True,
    "is_accepting_patients": True
}).limit(20)

# Get doctor with hospital details
pipeline = [
    {"$match": {"user_id": doctor_id}},
    {"$lookup": {
        "from": "hospitals",
        "localField": "primary_hospital_id",
        "foreignField": "_id",
        "as": "hospital"
    }}
]
result = await db.doctor_profiles.aggregate(pipeline)
```

---

#### **Module 4: Appointment Booking**

**Primary Collections:**
- `appointments`
- `prescriptions`
- `notifications`

**Operations:**
- `POST /api/appointments/book` → Insert into `appointments`, `notifications`
- `GET /api/appointments/patient/:id` → Find in `appointments`
- `GET /api/appointments/doctor/:id` → Find in `appointments`
- `PUT /api/appointments/:id/complete` → Update `appointments`, insert `prescriptions`
- `PUT /api/appointments/:id/cancel` → Update `appointments`, `notifications`

**Key Queries:**
```python
# Book appointment
appointment = await db.appointments.insert_one({
    "patient_id": patient_id,
    "doctor_id": doctor_id,
    "appointment_date": appointment_date,
    "status": "scheduled",
    ...
})

# Send notification
await db.notifications.insert_one({
    "user_id": patient_id,
    "type": "appointment",
    "message": f"Appointment booked for {appointment_date}",
    ...
})

# Get doctor's schedule for today
appointments = await db.appointments.find({
    "doctor_id": doctor_id,
    "appointment_date": {
        "$gte": start_of_day,
        "$lt": end_of_day
    },
    "status": {"$in": ["scheduled", "confirmed"]}
}).sort("appointment_date", 1)
```

---

#### **Module 5: AI Symptom Checker**

**Primary Collections:**
- `symptom_reports`
- `ai_conversations`
- `appointments` (optional link)

**Operations:**
- `POST /api/symptom-checker/start` → Insert into `symptom_reports`, `ai_conversations`
- `POST /api/symptom-checker/message` → Update `ai_conversations.messages`
- `POST /api/symptom-checker/complete` → Update `symptom_reports` with AI assessment
- `GET /api/symptom-checker/history` → Find in `symptom_reports`

**Key Queries:**
```python
# Start symptom checker session
session = await db.symptom_reports.insert_one({
    "session_id": uuid4(),
    "patient_id": user_id,
    "conversation": [],
    "status": "in_progress",
    ...
})

# Add message to conversation
await db.symptom_reports.update_one(
    {"session_id": session_id},
    {"$push": {
        "conversation": {
            "timestamp": datetime.utcnow(),
            "speaker": "patient",
            "message": message
        }
    }}
)

# Complete with AI assessment
await db.symptom_reports.update_one(
    {"session_id": session_id},
    {"$set": {
        "ai_assessment": ai_result,
        "status": "completed",
        "completed_at": datetime.utcnow()
    }}
)
```

---

#### **Module 6: Medical Report Upload**

**Primary Collections:**
- `medical_documents`
- `health_records` (if vitals extracted)

**Operations:**
- `POST /api/documents/upload` → Insert into `medical_documents`, trigger OCR/AI
- `GET /api/documents/patient/:id` → Find in `medical_documents`
- `GET /api/documents/:id` → Find one in `medical_documents`
- `DELETE /api/documents/:id` → Soft delete in `medical_documents`
- `POST /api/documents/:id/share` → Update `shared_with` in `medical_documents`

**Key Queries:**
```python
# Upload document
document = await db.medical_documents.insert_one({
    "document_id": uuid4(),
    "patient_id": user_id,
    "file_url": s3_url,
    "ocr_data": None,  # Process async
    "ai_analysis": None,
    ...
})

# Update with OCR results (background job)
await db.medical_documents.update_one(
    {"_id": document_id},
    {"$set": {
        "ocr_data": ocr_result,
        "ai_analysis": ai_analysis
    }}
)

# Extract vitals to health_records
if document_type == "lab_report":
    for result in ai_analysis['lab_results']:
        await db.health_records.insert_one({
            "patient_id": user_id,
            "record_type": "lab_test",
            "lab_test": result,
            "recorded_at": document_date,
            ...
        })
```

---

#### **Module 7: Medicine Reminder**

**Primary Collections:**
- `medications`
- `prescriptions` (read-only for importing)
- `notifications`

**Operations:**
- `POST /api/medications/add` → Insert into `medications`
- `GET /api/medications/patient/:id` → Find in `medications`
- `PUT /api/medications/:id` → Update `medications`
- `POST /api/medications/:id/log-adherence` → Push to `adherence_log`
- `DELETE /api/medications/:id` → Update `is_active` = false

**Key Queries:**
```python
# Add medication from prescription
for med in prescription['medications']:
    await db.medications.insert_one({
        "patient_id": patient_id,
        "medicine_name": med['drug_name'],
        "schedule": {
            "frequency": "daily",
            "times_per_day": 2,
            "time_slots": [
                {"time": "08:00", "with_meal": "before"},
                {"time": "20:00", "with_meal": "after"}
            ],
            ...
        },
        "prescription_id": prescription_id,
        "is_active": True,
        ...
    })

# Get medications due now (for reminder system)
now = datetime.utcnow()
current_time = now.strftime("%H:%M")

medications = await db.medications.find({
    "is_active": True,
    "reminder_enabled": True,
    "schedule.time_slots.time": {
        "$gte": (now - timedelta(minutes=15)).strftime("%H:%M"),
        "$lte": current_time
    }
})

# Log adherence
await db.medications.update_one(
    {"_id": medication_id},
    {"$push": {
        "adherence_log": {
            "scheduled_time": scheduled_time,
            "taken": True,
            "taken_at": datetime.utcnow(),
            ...
        }
    }}
)
```

---

#### **Module 8: Hospital Finder**

**Primary Collections:**
- `hospitals`

**Operations:**
- `GET /api/hospitals/nearby` → Geospatial query in `hospitals`
- `GET /api/hospitals/search` → Text search in `hospitals`
- `GET /api/hospitals/:id` → Find one in `hospitals`

**Key Queries:**
```python
# Find hospitals within 5km radius (Leaflet + OpenStreetMap)
hospitals = await db.hospitals.find({
    "address.location": {
        "$near": {
            "$geometry": {
                "type": "Point",
                "coordinates": [longitude, latitude]  # User's location
            },
            "$maxDistance": 5000  # 5km in meters
        }
    },
    "is_active": True
}).limit(20)

# Search by services
hospitals = await db.hospitals.find({
    "services": {"$in": ["Emergency", "Cardiology"]},
    "is_active": True
}).sort("rating", -1)
```

---

#### **Module 9: AI Chat (Health Advice)**

**Primary Collections:**
- `ai_conversations`

**Operations:**
- `POST /api/chat/start` → Insert into `ai_conversations`
- `POST /api/chat/message` → Update `messages` in `ai_conversations`
- `GET /api/chat/history` → Find in `ai_conversations`

**Key Queries:**
```python
# Start conversation
conversation = await db.ai_conversations.insert_one({
    "conversation_id": uuid4(),
    "user_id": user_id,
    "type": "health_advice",
    "messages": [],
    "context": {
        "patient_age": patient.age,
        "chronic_conditions": patient.chronic_conditions,
        ...
    },
    "status": "active",
    ...
})

# Add message
await db.ai_conversations.update_one(
    {"conversation_id": conversation_id},
    {
        "$push": {"messages": new_message},
        "$set": {"last_message_at": datetime.utcnow()}
    }
)
```

---

#### **Module 10: Notifications**

**Primary Collections:**
- `notifications`

**Operations:**
- `GET /api/notifications` → Find in `notifications`
- `PUT /api/notifications/:id/read` → Update `is_read` in `notifications`
- `GET /api/notifications/unread-count` → Count in `notifications`

**Key Queries:**
```python
# Get unread notifications
notifications = await db.notifications.find({
    "user_id": user_id,
    "is_read": False
}).sort("created_at", -1).limit(50)

# Mark as read
await db.notifications.update_one(
    {"_id": notification_id},
    {"$set": {
        "is_read": True,
        "read_at": datetime.utcnow()
    }}
)

# Unread count
count = await db.notifications.count_documents({
    "user_id": user_id,
    "is_read": False
})
```

---

#### **Module 11: Health Analytics**

**Primary Collections:**
- `health_records`
- `appointments`
- `medications`

**Operations:**
- `GET /api/analytics/vitals-trend` → Aggregate from `health_records`
- `GET /api/analytics/appointment-history` → Find in `appointments`
- `GET /api/analytics/medication-adherence` → Aggregate from `medications`

**Key Queries:**
```python
# Blood pressure trend (last 3 months)
pipeline = [
    {
        "$match": {
            "patient_id": user_id,
            "record_type": "vitals",
            "recorded_at": {"$gte": three_months_ago}
        }
    },
    {
        "$project": {
            "date": {"$dateToString": {
                "format": "%Y-%m-%d",
                "date": "$recorded_at"
            }},
            "systolic": "$vitals.blood_pressure_systolic",
            "diastolic": "$vitals.blood_pressure_diastolic"
        }
    },
    {"$sort": {"date": 1}}
]
trend = await db.health_records.aggregate(pipeline)

# Medication adherence rate
pipeline = [
    {
        "$match": {
            "patient_id": user_id,
            "is_active": True
        }
    },
    {
        "$project": {
            "medicine_name": 1,
            "total_doses": {"$size": "$adherence_log"},
            "taken_doses": {
                "$size": {
                    "$filter": {
                        "input": "$adherence_log",
                        "as": "log",
                        "cond": {"$eq": ["$$log.taken", True]}
                    }
                }
            }
        }
    },
    {
        "$project": {
            "medicine_name": 1,
            "adherence_rate": {
                "$multiply": [
                    {"$divide": ["$taken_doses", "$total_doses"]},
                    100
                ]
            }
        }
    }
]
adherence = await db.medications.aggregate(pipeline)
```

---

#### **Module 12: Admin Management**

**Primary Collections:**
- `users`
- `doctor_profiles`
- `admin_audit_logs`

**Operations:**
- `GET /api/admin/users` → Find in `users`
- `PUT /api/admin/users/:id/suspend` → Update `is_active` in `users`, log in `admin_audit_logs`
- `POST /api/admin/doctors/:id/verify` → Update `is_verified` in `doctor_profiles`, log
- `GET /api/admin/audit-logs` → Find in `admin_audit_logs`

**Key Queries:**
```python
# Verify doctor
await db.doctor_profiles.update_one(
    {"user_id": doctor_id},
    {"$set": {
        "is_verified": True,
        "verified_at": datetime.utcnow(),
        "verified_by": admin_id
    }}
)

# Log action
await db.admin_audit_logs.insert_one({
    "admin_id": admin_id,
    "action": "doctor_verified",
    "action_category": "user_management",
    "target_type": "doctor",
    "target_id": doctor_id,
    "changes": {
        "before": {"is_verified": False},
        "after": {"is_verified": True}
    },
    "timestamp": datetime.utcnow(),
    ...
})
```

---

## 14. Summary & Best Practices

### 14.1 Design Highlights

**✅ Strengths of This Design:**

1. **Hybrid Approach:** Strategic mix of embedding and referencing
2. **Performance Optimized:** Comprehensive indexing strategy
3. **Scalable:** Sharding ready for high-growth collections
4. **Secure:** Encryption, RBAC, audit logging
5. **HIPAA Compliant:** Data retention, access control, audit trails
6. **Developer Friendly:** Clear structure, well-documented

### 14.2 MongoDB Best Practices Applied

1. **Document Design:**
   - Keep frequently accessed data together (embed)
   - Reference large or frequently changing data
   - Avoid unbounded arrays

2. **Indexing:**
   - Index all query fields
   - Compound indexes for multi-field queries
   - Text indexes for search
   - Geospatial indexes for location

3. **Performance:**
   - Use projections to fetch only needed fields
   - Use aggregation pipeline efficiently
   - Leverage covered queries
   - Implement caching for static data

4. **Security:**
   - Encrypt sensitive data
   - Implement RBAC
   - Audit all PHI access
   - Regular backups

5. **Maintainability:**
   - Clear naming conventions
   - Schema validation
   - Documentation
   - Version control for schema changes

### 14.3 Implementation Checklist

**Phase 1: Setup (Week 1)**
- ☐ Create MongoDB Atlas cluster (M10 tier)
- ☐ Configure network access (IP whitelist)
- ☐ Create database users with appropriate roles
- ☐ Enable automated backups

**Phase 2: Schema Creation (Week 2)**
- ☐ Create all 14 collections
- ☐ Apply schema validation rules
- ☐ Create all indexes (single, compound, text, geospatial)
- ☐ Test index performance with sample data

**Phase 3: Integration (Weeks 3-4)**
- ☐ Connect FastAPI to MongoDB
- ☐ Implement Pydantic models for validation
- ☐ Create repository/service layer
- ☐ Implement CRUD operations for each module

**Phase 4: Security (Week 5)**
- ☐ Enable TLS/SSL encryption
- ☐ Implement field-level encryption for sensitive data
- ☐ Set up audit logging
- ☐ Configure TTL indexes

**Phase 5: Testing (Week 6)**
- ☐ Load testing (simulate 1,000 concurrent users)
- ☐ Query performance testing
- ☐ Backup/restore testing
- ☐ Security testing

**Phase 6: Optimization (Ongoing)**
- ☐ Monitor slow queries (Performance Advisor)
- ☐ Optimize based on actual usage patterns
- ☐ Review and drop unused indexes
- ☐ Implement archival strategy

---

## 15. Conclusion

This MongoDB database design for MediNova AI provides a **production-ready, scalable, and secure foundation** for a modern healthcare platform. The design:

- **Supports all 14 core modules** of the MediNova application
- **Optimizes for read-heavy workloads** (80% reads, 20% writes)
- **Scales horizontally** through sharding for high-growth collections
- **Ensures data security** with encryption, RBAC, and audit logging
- **Maintains HIPAA compliance** with proper data handling and retention
- **Provides excellent developer experience** with clear structure and documentation

The database is designed to handle:
- **10,000+ concurrent users** at launch
- **100,000+ users** by year 3
- **Millions of health records** with time-series optimization
- **Complex AI workloads** with efficient document storage
- **Real-time notifications** and reminders

**Technology Stack Integration:**
- **MongoDB Atlas:** Cloud database with automated management
- **FastAPI:** Async Python framework with native MongoDB support
- **React.js + Tailwind CSS:** Frontend consumes REST APIs
- **LangGraph + OpenAI:** AI agents store data in MongoDB
- **EasyOCR:** Processes documents, stores results in MongoDB

This design is ready for immediate implementation and will support MediNova AI's growth from prototype to production scale.

---

**Document Version:** 1.0  
**Last Updated:** July 3, 2026  
**Author:** Senior MongoDB Database Architect  
**Status:** Production Ready ✅
