# MediNova AI: Dashboard Page Designs
## Complete Dashboard and Feature Pages

---

**Project:** MediNova AI - Multi-Agent Healthcare Intelligence Platform  
**Design Style:** Healthcare Theme with Glassmorphism  
**Framework:** Tailwind CSS + React.js  
**Date:** July 2, 2026  

---

## Table of Contents

1. [Patient Dashboard](#1-patient-dashboard)
2. [Doctor Dashboard](#2-doctor-dashboard)
3. [Admin Dashboard](#3-admin-dashboard)
4. [Profile Page](#4-profile-page)
5. [Settings Page](#5-settings-page)
6. [Health Analytics](#6-health-analytics)
7. [Appointment Booking](#7-appointment-booking)
8. [Medicine Reminder](#8-medicine-reminder)
9. [Medical Report Upload](#9-medical-report-upload)
10. [Hospital Finder](#10-hospital-finder)
11. [AI Chat (Symptom Checker)](#11-ai-chat-symptom-checker)

---

## Dashboard Layout Foundation

### Common Layout Structure

**All dashboards use this base layout:**

```
┌─────────────────────────────────────────────────────────────┐
│  [Navbar - Top, Sticky]                                     │
├──────────┬──────────────────────────────────────────────────┤
│          │                                                  │
│ Sidebar  │  Main Content Area                               │
│ (Fixed)  │  (Scrollable)                                    │
│          │                                                  │
│  • Home  │  [Breadcrumbs]                                   │
│  • Chat  │                                                  │
│  • Appt  │  [Page Header]                                   │
│  • Docs  │                                                  │
│          │  [Content Cards/Sections]                        │
│          │                                                  │
│          │                                                  │
└──────────┴──────────────────────────────────────────────────┘
```

### Global Navigation Bar

**Position:** Fixed top, spans full width

**Structure:**
- Height: `h-16` (64px)
- Background: `bg-white/80 backdrop-blur-lg`
- Border: `border-b border-gray-200`
- Shadow: `shadow-sm`
- Z-index: `z-50`

**Layout:**
```
[☰ Menu] [Logo] MediNova AI     [Search]     [🔔] [👤 Profile] ▼
```

**Components:**

**Mobile Menu Toggle:**
- Display: `lg:hidden`
- Icon: Menu (hamburger)
- Style: `p-2 rounded-lg hover:bg-gray-100`
- Size: `w-6 h-6`

**Logo Section:**
- Display: `flex items-center gap-3`
- Icon: Medical heart, `w-8 h-8 text-primary-600`
- Text: "MediNova AI"
- Font: `font-bold text-lg text-gray-900`

**Search Bar (Desktop):**
- Display: `hidden md:block flex-1 max-w-xl mx-8`
- Container: `relative`
- Input:
  ```
  w-full pl-10 pr-4 py-2 rounded-xl border border-gray-300
  bg-gray-50 text-sm
  focus:bg-white focus:border-primary-500 focus:ring-2 focus:ring-primary-200
  ```
- Icon: Search icon, `absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400`
- Placeholder: "Search patients, appointments, records..."

**Right Section:**
- Display: `flex items-center gap-4`

**Notification Bell:**
- Icon: Bell, `w-6 h-6 text-gray-600`
- Container: `relative p-2 rounded-lg hover:bg-gray-100 cursor-pointer`
- Badge: `absolute -top-1 -right-1 w-5 h-5 bg-danger-500 rounded-full text-white text-xs flex items-center justify-center`
- Badge shows: Unread count

**Profile Dropdown:**
- Container: `flex items-center gap-3 cursor-pointer hover:bg-gray-50 rounded-xl p-2`
- Avatar: `w-10 h-10 rounded-full border-2 border-gray-200`
- Name: `text-sm font-medium text-gray-900` (Desktop only)
- Icon: ChevronDown, `w-4 h-4 text-gray-500`

### Global Sidebar

**Position:** Fixed left, full height

**Structure:**
- Width: `w-64` (256px) desktop, `w-20` collapsed
- Background: `bg-white`
- Border: `border-r border-gray-200`
- Shadow: `shadow-lg`
- Z-index: `z-40`

**Sidebar Header:**
- Padding: `p-6`
- Shows when expanded
- Logo + text centered

**Navigation Items:**

**Structure per item:**
```
[Icon]  Label           [Badge]
```

**Default Nav Link:**
- Style:
  ```
  flex items-center gap-3 px-4 py-3 mx-2 rounded-xl
  text-gray-700 font-medium text-sm
  hover:bg-primary-50 hover:text-primary-700
  transition-all duration-200
  ```
- Icon: `w-5 h-5`
- Badge: Optional, `ml-auto px-2 py-0.5 text-xs rounded-full`

**Active Nav Link:**
- Background: `bg-primary-100`
- Text: `text-primary-700`
- Border: `border-l-4 border-primary-600` (alternative style)
- Font: `font-semibold`

**Sidebar Sections:**
- Section title: `px-4 py-2 text-xs font-semibold text-gray-400 uppercase tracking-wider`
- Margin: `mt-6`

**Collapse Toggle:**
- Position: `absolute -right-3 top-6`
- Button: `w-6 h-6 rounded-full bg-white border-2 border-gray-300 shadow-md`
- Icon: ChevronLeft (expanded) / ChevronRight (collapsed)
- Hover: `hover:bg-gray-50`

---

## 1. Patient Dashboard

### 1.1 Page Overview

**Purpose:** Central hub for patients to manage health, appointments, and interact with AI

**Key Features:**
- Health summary cards
- Upcoming appointments
- Quick actions
- Recent activity
- Health metrics visualization

### 1.2 Page Layout

**Breadcrumbs:**
- Display: `mb-6`
- Structure: Home > Dashboard
- Style: `text-sm text-gray-500 flex items-center gap-2`

**Page Header:**
- Container: `mb-8`
- Layout: `flex items-center justify-between`

**Greeting:**
- Font: `text-3xl font-bold font-heading text-gray-900`
- Text: "Welcome back, [Patient Name]!"
- Subtext: Current date and time
- Subtext style: `text-base text-gray-500 mt-2`

**Quick Action Buttons:**
- Container: `flex gap-3`
- Primary button: "Talk to AI Doctor"
- Style: `px-6 py-2.5 bg-primary-600 text-white font-semibold rounded-xl shadow-lg hover:bg-primary-700`
- Secondary: "Book Appointment"
- Style: `px-6 py-2.5 bg-white border-2 border-gray-300 text-gray-700 font-semibold rounded-xl hover:bg-gray-50`

### 1.3 Dashboard Content

**Layout:** Grid system

```
┌─────────────────────────────────────────────────────────┐
│  [Health Summary Cards - 4 columns]                     │
├─────────────────────────┬───────────────────────────────┤
│                         │                               │
│  Upcoming Appointments  │  Recent Activity              │
│  (Left - 60%)           │  (Right - 40%)                │
│                         │                               │
├─────────────────────────┴───────────────────────────────┤
│  Health Metrics Chart                                   │
├─────────────────────────┬───────────────────────────────┤
│                         │                               │
│  Medication Reminders   │  Quick Access                 │
│                         │                               │
└─────────────────────────┴───────────────────────────────┘
```

### 1.4 Health Summary Cards

**Grid:** `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8`

**Card 1: Heart Rate**
- Icon: Heart icon, `w-12 h-12 text-danger-500`
- Value: "72 bpm"
- Label: "Heart Rate"
- Trend: ↑ 2% from last week
- Background: `bg-gradient-to-br from-danger-50 to-danger-100`

**Card 2: Blood Pressure**
- Icon: Activity icon, `w-12 h-12 text-primary-500`
- Value: "120/80 mmHg"
- Label: "Blood Pressure"
- Status: "Normal"
- Background: `bg-gradient-to-br from-primary-50 to-primary-100`

**Card 3: Oxygen Level**
- Icon: Wind icon, `w-12 h-12 text-info-500`
- Value: "98%"
- Label: "SpO2 Level"
- Status: "Good"
- Background: `bg-gradient-to-br from-info-50 to-info-100`

**Card 4: BMI**
- Icon: Scale icon, `w-12 h-12 text-success-500`
- Value: "23.5"
- Label: "BMI"
- Status: "Healthy"
- Background: `bg-gradient-to-br from-success-50 to-success-100`

**Card Structure:**
```
┌────────────────────────┐
│ [Icon]                 │
│                        │
│ 72 bpm                 │ (Large, bold)
│ Heart Rate             │ (Label)
│                        │
│ ↑ 2% from last week    │ (Trend)
└────────────────────────┘
```

**Card Style:**
- Padding: `p-6`
- Rounded: `rounded-2xl`
- Border: `border border-gray-100`
- Shadow: `shadow-lg`
- Hover: `hover:shadow-xl hover:scale-[1.02] transition-all duration-300`

**Value Style:**
- Font: `text-3xl font-bold text-gray-900 my-3`

**Trend Style:**
- Positive: `text-success-600 text-sm flex items-center gap-1`
- Negative: `text-danger-600 text-sm flex items-center gap-1`
- Icon: TrendingUp or TrendingDown


### 1.5 Upcoming Appointments Section

**Container:**
- Background: `bg-white`
- Rounded: `rounded-2xl`
- Border: `border border-gray-200`
- Shadow: `shadow-lg`
- Padding: `p-6`

**Section Header:**
- Layout: `flex items-center justify-between mb-6`
- Title: "Upcoming Appointments"
- Font: `text-xl font-semibold text-gray-900`
- "View All" link: `text-sm font-semibold text-primary-600 hover:text-primary-700`

**Appointment Card:**
```
┌──────────────────────────────────────┐
│ [Avatar] Dr. Sarah Johnson           │
│          Cardiologist                │
│                                      │
│ 📅 Tomorrow, 10:00 AM                │
│ 📍 City Hospital, Room 302           │
│ 🎥 Video Consultation                │
│                                      │
│ [Reschedule] [Join Call]            │
└──────────────────────────────────────┘
```

**Appointment Card Style:**
- Background: `bg-gray-50`
- Rounded: `rounded-xl`
- Padding: `p-4`
- Margin: `mb-4` (between cards)
- Hover: `hover:bg-primary-50 transition-colors`

**Doctor Info:**
- Layout: `flex items-center gap-3 mb-4`
- Avatar: `w-12 h-12 rounded-full`
- Name: `text-base font-semibold text-gray-900`
- Specialty: `text-sm text-gray-500`

**Appointment Details:**
- Each detail: Icon + text
- Layout: `space-y-2`
- Icon: `w-4 h-4 text-gray-400`
- Text: `text-sm text-gray-700`

**Action Buttons:**
- Container: `flex gap-3 mt-4`
- Reschedule: Ghost button
- Join Call: Primary button with video icon

**Empty State:**
- Icon: Calendar with X, `w-16 h-16 text-gray-300 mx-auto`
- Text: "No upcoming appointments"
- CTA: "Book an appointment" button

### 1.6 Recent Activity Section

**Container:**
- Background: `bg-white`
- Rounded: `rounded-2xl`
- Border: `border border-gray-200`
- Shadow: `shadow-lg`
- Padding: `p-6`

**Section Header:**
- Title: "Recent Activity"
- Font: `text-xl font-semibold text-gray-900 mb-6`

**Activity Timeline:**
```
○ Lab results uploaded
  2 hours ago

○ Prescription updated
  Yesterday

○ Appointment completed
  2 days ago

○ Health record added
  1 week ago
```

**Activity Item:**
- Layout: `flex gap-4 mb-6 last:mb-0`
- Timeline dot:
  - Size: `w-3 h-3`
  - Color varies: `bg-primary-500`, `bg-success-500`, `bg-info-500`
  - Rounded: `rounded-full`
  - Line: `border-l-2 border-gray-200` (connecting line)
- Icon container: `w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center`
- Icon: Relevant icon, `w-5 h-5 text-gray-600`
- Content:
  - Title: `text-sm font-medium text-gray-900`
  - Time: `text-xs text-gray-500 mt-1`

### 1.7 Health Metrics Chart

**Container:**
- Background: `bg-white`
- Rounded: `rounded-2xl`
- Border: `border border-gray-200`
- Shadow: `shadow-lg`
- Padding: `p-6`
- Margin: `mb-8`

**Section Header:**
- Layout: `flex items-center justify-between mb-6`
- Title: "Health Trends"
- Font: `text-xl font-semibold text-gray-900`
- Timeframe selector:
  - Pills: "Week", "Month", "Year"
  - Style: `px-4 py-2 rounded-lg text-sm font-medium`
  - Active: `bg-primary-100 text-primary-700`
  - Inactive: `text-gray-600 hover:bg-gray-100`

**Chart Area:**
- Type: Line chart showing multiple metrics
- Height: `h-64`
- Metrics: Heart rate, blood pressure, weight
- Legend at bottom
- Responsive and interactive
- Gradient fills under lines
- Tooltips on hover

**Chart Placeholder:**
- Description: Multi-line chart visualization
- X-axis: Time (days/months)
- Y-axis: Metric values
- Colors: primary-500, success-500, danger-500

### 1.8 Medication Reminders Widget

**Container:**
- Background: `bg-gradient-to-br from-accent-50 to-accent-100`
- Rounded: `rounded-2xl`
- Border: `border border-accent-200`
- Shadow: `shadow-lg`
- Padding: `p-6`

**Header:**
- Icon: Pill icon, `w-8 h-8 text-accent-600`
- Title: "Today's Medications"
- Font: `text-lg font-semibold text-gray-900 mb-4`

**Medication List:**
```
[✓] Aspirin 100mg
    After breakfast • 8:00 AM

[ ] Metformin 500mg
    After lunch • 1:00 PM

[ ] Vitamin D
    After dinner • 8:00 PM
```

**Medication Item:**
- Checkbox: `w-5 h-5 rounded text-success-600`
- Name: `text-sm font-medium text-gray-900`
- Details: `text-xs text-gray-600 mt-1`
- Completed: Checked, strikethrough text
- Pending: Unchecked, normal text

**Add Reminder Button:**
- Style: `text-sm font-semibold text-accent-600 hover:text-accent-700 mt-4 flex items-center gap-2`
- Icon: Plus icon

### 1.9 Quick Access Section

**Container:**
- Background: `bg-white`
- Rounded: `rounded-2xl`
- Border: `border border-gray-200`
- Shadow: `shadow-lg`
- Padding: `p-6`

**Title:**
- Font: `text-lg font-semibold text-gray-900 mb-4`
- Text: "Quick Actions"

**Action Grid:**
- Layout: `grid grid-cols-2 gap-3`

**Action Button:**
```
┌─────────────┐
│   [Icon]    │
│             │
│   Label     │
└─────────────┘
```

**Actions:**
1. **AI Chat**
   - Icon: MessageCircle, `text-primary-600`
   - Label: "Talk to AI"
   
2. **Upload Report**
   - Icon: Upload, `text-success-600`
   - Label: "Upload Report"
   
3. **Find Doctor**
   - Icon: Search, `text-info-600`
   - Label: "Find Doctor"
   
4. **My Records**
   - Icon: FileText, `text-warning-600`
   - Label: "Health Records"

**Button Style:**
- Background: `bg-gray-50`
- Hover: `hover:bg-primary-50 hover:shadow-md`
- Padding: `p-4`
- Rounded: `rounded-xl`
- Text: `text-sm font-medium text-gray-700 text-center`
- Icon: `w-8 h-8 mx-auto mb-2`
- Transition: `transition-all duration-200`

---

## 2. Doctor Dashboard

### 2.1 Page Overview

**Purpose:** Help doctors manage patients, appointments, and consultations efficiently

**Key Features:**
- Today's schedule
- Patient queue
- Quick stats
- Recent consultations
- Pending tasks

### 2.2 Page Layout

**Header:**
- Greeting: "Good morning, Dr. [Name]"
- Date: Current date
- Quick stats summary

**Layout Grid:**
```
┌─────────────────────────────────────────────────────────┐
│  [Stats Cards - 4 columns]                             │
├───────────────────────┬─────────────────────────────────┤
│                       │                                 │
│  Today's Schedule     │  Patient Queue                  │
│  (Timeline)           │  (Waiting list)                 │
│                       │                                 │
├───────────────────────┴─────────────────────────────────┤
│  Recent Consultations                                   │
├───────────────────────┬─────────────────────────────────┤
│                       │                                 │
│  Pending Tasks        │  Performance Stats              │
│                       │                                 │
└───────────────────────┴─────────────────────────────────┘
```

### 2.3 Stats Cards

**Grid:** `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8`

**Card 1: Today's Appointments**
- Icon: Calendar, `w-10 h-10 text-primary-500`
- Value: "8"
- Label: "Appointments Today"
- Subtext: "2 completed, 6 pending"
- Background: White with colored border-l-4

**Card 2: Patients**
- Icon: Users, `w-10 h-10 text-success-500`
- Value: "156"
- Label: "Total Patients"
- Trend: "+12 this month"

**Card 3: Consultations**
- Icon: Video, `w-10 h-10 text-info-500`
- Value: "24"
- Label: "This Week"
- Status: "3 scheduled today"

**Card 4: Rating**
- Icon: Star, `w-10 h-10 text-warning-500`
- Value: "4.9"
- Label: "Patient Rating"
- Subtext: "Based on 89 reviews"

**Card Style:**
- Background: `bg-white`
- Border: `border-l-4` (colored by theme)
- Rounded: `rounded-xl`
- Shadow: `shadow-md`
- Padding: `p-6`
- Hover: `hover:shadow-lg transition-shadow`

### 2.4 Today's Schedule Section

**Container:**
- Background: `bg-white`
- Rounded: `rounded-2xl`
- Padding: `p-6`
- Shadow: `shadow-lg`

**Header:**
- Title: "Today's Schedule"
- Subtitle: "8 appointments scheduled"
- Filter: All / Completed / Pending tabs

**Timeline View:**
```
08:00 ─┬─ John Doe
       │  Follow-up consultation
       │  [Start] [View History]
       │
09:00 ─┼─ Sarah Smith
       │  Initial consultation
       │  [Start] [View History]
       │
10:00 ─┼─ [Empty slot]
       │
11:00 ─┼─ Michael Brown
       │  Lab results review
       │  [Start] [View History]
```

**Appointment Item:**
- Time indicator: `text-sm font-semibold text-gray-500`
- Patient name: `text-base font-semibold text-gray-900`
- Type: `text-sm text-gray-600`
- Status badge: Completed (green), In Progress (blue), Pending (gray)
- Action buttons: Start consultation, View history
- Divider line connecting appointments

**Current Time Marker:**
- Red line: `border-t-2 border-danger-500`
- Dot: `w-3 h-3 bg-danger-500 rounded-full`
- Label: "Current time"


### 2.5 Patient Queue Section

**Container:**
- Background: `bg-white`
- Rounded: `rounded-2xl`
- Padding: `p-6`
- Shadow: `shadow-lg`

**Header:**
- Title: "Patient Queue"
- Count badge: Number waiting
- Style: `bg-warning-100 text-warning-800 px-3 py-1 rounded-full text-sm font-semibold`

**Queue List:**
```
1. [Avatar] Emma Wilson
   Waiting for 15 min
   Symptoms: Fever, Cough
   [Call Next]

2. [Avatar] James Lee
   Waiting for 8 min
   Symptoms: Headache
   [Call Next]

3. [Avatar] Lisa Anderson
   Waiting for 3 min
   Symptoms: Back pain
   [Call Next]
```

**Patient Card:**
- Layout: `flex items-center justify-between p-4 bg-gray-50 rounded-xl mb-3`
- Queue number: `w-8 h-8 rounded-full bg-primary-100 text-primary-700 font-bold flex items-center justify-center`
- Avatar: `w-12 h-12 rounded-full`
- Patient info:
  - Name: `font-semibold text-gray-900`
  - Wait time: `text-sm text-warning-600`
  - Symptoms: `text-sm text-gray-600`
- Action: "Call Next" button, `px-4 py-2 bg-primary-600 text-white rounded-lg`

### 2.6 Recent Consultations Section

**Container:**
- Background: `bg-white`
- Rounded: `rounded-2xl`
- Padding: `p-6`
- Shadow: `shadow-lg`
- Full width: `col-span-full`

**Header:**
- Title: "Recent Consultations"
- Filter dropdown: Last 7 days / 30 days / All time

**Table View:**
```
┌────────┬────────────┬─────────────┬──────────┬──────────┐
│ Date   │ Patient    │ Type        │ Duration │ Actions  │
├────────┼────────────┼─────────────┼──────────┼──────────┤
│ Today  │ John Doe   │ Follow-up   │ 30 min   │ [View]   │
│ 9:00AM │ Age: 45    │ Video Call  │          │ [Notes]  │
├────────┼────────────┼─────────────┼──────────┼──────────┤
│ Today  │ Sarah S.   │ Initial     │ 45 min   │ [View]   │
│ 8:00AM │ Age: 32    │ In-person   │          │ [Notes]  │
└────────┴────────────┴─────────────┴──────────┴──────────┘
```

**Table Style:**
- Header: `bg-gray-100 text-gray-700 font-semibold text-sm`
- Rows: `hover:bg-gray-50 transition-colors`
- Cell padding: `px-6 py-4`
- Border: `border-b border-gray-200`

**Action Buttons:**
- View: Eye icon, opens patient details
- Notes: FileText icon, opens consultation notes
- Style: Icon buttons, `p-2 hover:bg-gray-100 rounded-lg`

### 2.7 Pending Tasks Widget

**Container:**
- Background: `bg-warning-50`
- Border: `border border-warning-200`
- Rounded: `rounded-2xl`
- Padding: `p-6`

**Header:**
- Icon: CheckSquare, `w-6 h-6 text-warning-600`
- Title: "Pending Tasks"
- Count: Badge with number

**Task List:**
```
[ ] Review lab results for John Doe
    Due: Today, 5:00 PM

[ ] Sign prescription for Sarah Smith
    Due: Today, 6:00 PM

[ ] Complete patient notes (3)
    Overdue by 2 hours
```

**Task Item:**
- Checkbox: `w-5 h-5 rounded text-warning-600`
- Title: `text-sm font-medium text-gray-900`
- Due time: `text-xs text-gray-600 mt-1`
- Overdue: `text-danger-600 font-semibold`
- Hover: `hover:bg-warning-100 cursor-pointer`

### 2.8 Performance Stats Widget

**Container:**
- Background: `bg-white`
- Rounded: `rounded-2xl`
- Padding: `p-6`
- Shadow: `shadow-lg`

**Title:**
- Text: "This Month's Performance"
- Font: `text-lg font-semibold text-gray-900 mb-6`

**Stat Items:**
```
Consultations Completed
●●●●●●●●○○ 82%
245 of 300 target

Patient Satisfaction
●●●●●●●●●○ 4.8/5.0
Based on 156 reviews

Avg. Consultation Time
25 minutes
Target: 30 minutes ✓
```

**Progress Bar:**
- Background: `bg-gray-200 h-2 rounded-full`
- Fill: `bg-success-500 h-2 rounded-full`
- Percentage: `text-sm font-semibold text-gray-700`

---

## 3. Admin Dashboard

### 3.1 Page Overview

**Purpose:** System monitoring, user management, and platform analytics

**Key Features:**
- Platform statistics
- User analytics
- System health
- Recent activities
- Revenue metrics

### 3.2 Page Layout

**Header:**
- Title: "Admin Dashboard"
- Date range selector
- Export button

**Layout Grid:**
```
┌─────────────────────────────────────────────────────────┐
│  [KPI Cards - 4 columns]                               │
├──────────────────────────┬──────────────────────────────┤
│                          │                              │
│  User Growth Chart       │  System Health               │
│                          │                              │
├──────────────────────────┴──────────────────────────────┤
│  Recent User Registrations                              │
├──────────────────────────┬──────────────────────────────┤
│                          │                              │
│  Revenue Overview        │  Top Doctors                 │
│                          │                              │
└──────────────────────────┴──────────────────────────────┘
```

### 3.3 KPI Cards

**Grid:** `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8`

**Card 1: Total Users**
- Value: "12,456"
- Label: "Total Users"
- Trend: "+342 this month (+2.8%)"
- Icon: Users
- Breakdown: "8,234 Patients | 1,222 Doctors"

**Card 2: Active Sessions**
- Value: "3,456"
- Label: "Active Now"
- Status: "Peak hours"
- Icon: Activity

**Card 3: Appointments**
- Value: "8,945"
- Label: "This Month"
- Trend: "+12% from last month"
- Icon: Calendar

**Card 4: Revenue**
- Value: "$45,678"
- Label: "Monthly Revenue"
- Trend: "+$5,234 (+12.9%)"
- Icon: DollarSign

**Card Design:**
- Glass effect: `bg-white/80 backdrop-blur-xl`
- Gradient overlay for each category
- Border: `border border-gray-200`
- Large value: `text-4xl font-bold`
- Trend with arrow icon and color

### 3.4 User Growth Chart

**Container:**
- Background: `bg-white`
- Rounded: `rounded-2xl`
- Padding: `p-6`
- Shadow: `shadow-lg`

**Header:**
- Title: "User Growth"
- Timeframe: Last 6 months
- Filters: Patients / Doctors / All

**Chart:**
- Type: Area chart
- Dual lines: Patients (primary-500) and Doctors (success-500)
- Height: `h-80`
- Gradient fills
- Interactive tooltips
- Legend at bottom

**Data Points:**
- X-axis: Months
- Y-axis: User count
- Milestone markers for significant events

### 3.5 System Health Monitor

**Container:**
- Background: `bg-white`
- Rounded: `rounded-2xl`
- Padding: `p-6`
- Shadow: `shadow-lg`

**Header:**
- Title: "System Health"
- Status badge: "All Systems Operational" (green)

**Health Metrics:**
```
API Response Time
●●●●●●●●●○ 95%
Average: 120ms

Database Performance
●●●●●●●●●● 100%
Query time: 45ms

Server Uptime
●●●●●●●●●● 99.9%
Last downtime: 15 days ago

Storage Usage
●●●●●●○○○○ 67%
423 GB of 630 GB used
```

**Metric Item:**
- Name: `font-medium text-gray-900`
- Progress bar with percentage
- Detail text: `text-sm text-gray-600`
- Status icon: Green (good), Yellow (warning), Red (critical)

**Alerts Section:**
- Background: `bg-warning-50 p-4 rounded-xl mt-4`
- Icon: AlertTriangle
- Text: "2 minor issues detected"
- Link: "View details →"

### 3.6 Recent User Registrations

**Container:**
- Background: `bg-white`
- Rounded: `rounded-2xl`
- Padding: `p-6`
- Shadow: `shadow-lg`
- Full width: `col-span-full`

**Header:**
- Title: "Recent Registrations"
- Filter: Today / This Week / This Month
- Search bar

**Table:**
```
┌────────┬─────────────┬─────────┬────────────┬────────┬──────────┐
│ User   │ Email       │ Role    │ Registered │ Status │ Actions  │
├────────┼─────────────┼─────────┼────────────┼────────┼──────────┤
│ [Pic]  │ john@...    │ Patient │ 2 min ago  │ Active │ [View]   │
│ John D │             │         │            │        │ [Edit]   │
├────────┼─────────────┼─────────┼────────────┼────────┼──────────┤
│ [Pic]  │ sarah@...   │ Doctor  │ 15 min ago │ Pending│ [Verify] │
│ Sarah S│             │         │            │Verify  │ [View]   │
└────────┴─────────────┴─────────┴────────────┴────────┴──────────┘
```

**Table Features:**
- Sortable columns
- Status badges with colors
- Avatar thumbnails
- Action dropdown menu
- Pagination at bottom

**Status Badges:**
- Active: `bg-success-100 text-success-800`
- Pending: `bg-warning-100 text-warning-800`
- Suspended: `bg-danger-100 text-danger-800`

### 3.7 Revenue Overview

**Container:**
- Background: `bg-gradient-to-br from-success-50 to-success-100`
- Rounded: `rounded-2xl`
- Padding: `p-6`
- Border: `border border-success-200`

**Header:**
- Icon: DollarSign, `w-8 h-8 text-success-600`
- Title: "Revenue This Month"
- Value: "$45,678"
- Font: `text-3xl font-bold text-gray-900`

**Breakdown:**
```
Consultations    $32,450   (71%)
●●●●●●●○○○

Subscriptions    $8,900    (19%)
●●○○○○○○○○

Other Services   $4,328    (10%)
●○○○○○○○○○
```

**Item Style:**
- Label: `text-sm font-medium text-gray-700`
- Value: `text-lg font-semibold text-gray-900`
- Percentage: `text-sm text-gray-600`
- Progress bar: Colored by category

**Comparison:**
- Text: "↑ 12.5% vs last month"
- Color: `text-success-600 font-semibold`

### 3.8 Top Doctors Leaderboard

**Container:**
- Background: `bg-white`
- Rounded: `rounded-2xl`
- Padding: `p-6`
- Shadow: `shadow-lg`

**Header:**
- Title: "Top Performing Doctors"
- Subtitle: "Based on ratings and consultations"
- Timeframe: This month

**Leaderboard:**
```
🥇 1. Dr. Sarah Johnson
      ⭐ 4.9 (156 reviews)
      245 consultations

🥈 2. Dr. Michael Chen
      ⭐ 4.8 (142 reviews)
      223 consultations

🥉 3. Dr. Emily Davis
      ⭐ 4.8 (138 reviews)
      218 consultations
```

**Doctor Item:**
- Rank: Medal emoji or number
- Avatar: `w-12 h-12 rounded-full`
- Name: `font-semibold text-gray-900`
- Rating: Stars + count
- Consultations: `text-sm text-gray-600`
- Border-l with rank color

---

## 4. Profile Page

### 4.1 Page Overview

**Purpose:** View and edit user profile information

**Variants:** Patient Profile, Doctor Profile

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│  [Cover Photo]                                          │
│                                                         │
│      [Profile Picture]                                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Profile Header Card]                                  │
│  Name, Role, Contact                                    │
│                                                         │
├──────────────────────┬──────────────────────────────────┤
│                      │                                  │
│  Personal Info       │  Additional Info                 │
│  (Editable)          │  (Role-specific)                 │
│                      │                                  │
└──────────────────────┴──────────────────────────────────┘
```

### 4.2 Cover & Profile Picture

**Cover Photo:**
- Height: `h-48`
- Background: Gradient or uploaded image
- Edit button: Top-right corner
- Default: `bg-gradient-to-r from-primary-500 to-primary-700`

**Profile Picture:**
- Size: `w-32 h-32`
- Position: Overlapping cover, centered
- Border: `border-4 border-white`
- Shadow: `shadow-xl`
- Rounded: `rounded-full`
- Edit overlay on hover
- Upload icon appears

### 4.3 Profile Header Card

**Container:**
- Background: `bg-white`
- Rounded: `rounded-2xl`
- Padding: `p-8`
- Shadow: `shadow-lg`
- Margin: `-mt-16` (overlaps cover)

**Layout:**
- Centered content
- Name at top
- Contact info below
- Action buttons at bottom

**Name & Title:**
- Name: `text-3xl font-bold text-gray-900 text-center mb-2`
- Role/Specialty: `text-lg text-gray-600 text-center mb-4`
- Verification badge: Blue check icon for verified

**Contact Grid:**
- Layout: `grid grid-cols-1 md:grid-cols-3 gap-4 mb-6`
- Each item:
  - Icon: Email, Phone, Location
  - Label: `text-sm text-gray-500`
  - Value: `text-base font-medium text-gray-900`

**Action Buttons:**
- Layout: `flex justify-center gap-4`
- Edit Profile: Primary button
- Share Profile: Secondary button
- More options: Three dots menu


### 4.4 Personal Information Section (Patient)

**Container:**
- Background: `bg-white`
- Rounded: `rounded-2xl`
- Padding: `p-6`
- Shadow: `shadow-lg`

**Header:**
- Title: "Personal Information"
- Edit button: Top-right

**Form Fields:**
```
Full Name        [John Michael Doe         ]
Date of Birth    [01/15/1985              ]
Gender           [○ Male ○ Female ○ Other ]
Blood Group      [O+                      ]
Height           [175 cm                  ]
Weight           [75 kg                   ]
Phone            [+1 (555) 123-4567       ]
Email            [john.doe@email.com      ]
Address          [123 Main St, City       ]
Emergency Contact
  Name           [Jane Doe                ]
  Relation       [Spouse                  ]
  Phone          [+1 (555) 987-6543       ]
```

**Field Style:**
- Label: `text-sm font-medium text-gray-700 mb-2`
- Input: Standard design system input
- Grid: 2 columns on desktop, 1 on mobile
- Required: Red asterisk

**Edit Mode:**
- All fields become editable
- Save/Cancel buttons appear
- Validation on save

### 4.5 Medical History Section (Patient)

**Container:**
- Background: `bg-white`
- Rounded: `rounded-2xl`
- Padding: `p-6`
- Shadow: `shadow-lg`

**Header:**
- Title: "Medical History"
- Add button: "+ Add Condition"

**Allergies:**
```
Allergies
[+] Add Allergy

● Penicillin (Drug)
  Severe reaction
  [Edit] [Remove]

● Peanuts (Food)
  Mild reaction
  [Edit] [Remove]
```

**Chronic Conditions:**
```
Chronic Conditions
[+] Add Condition

● Hypertension
  Diagnosed: 2020
  Status: Controlled
  [Edit] [Remove]

● Type 2 Diabetes
  Diagnosed: 2018
  Status: Under treatment
  [Edit] [Remove]
```

**Past Surgeries:**
```
Surgeries
[+] Add Surgery

● Appendectomy
  Date: March 2015
  Hospital: City Medical Center
  [View Details] [Remove]
```

**Item Style:**
- Bullet point with status color
- Name: `font-semibold text-gray-900`
- Details: `text-sm text-gray-600`
- Action links: `text-sm text-primary-600`

### 4.6 Professional Information (Doctor Profile)

**Container:**
- Background: `bg-white`
- Rounded: `rounded-2xl`
- Padding: `p-6`
- Shadow: `shadow-lg`

**Fields:**
```
License Number        [MD123456          ]
Specialization        [Cardiology         ]
Sub-specialization    [Interventional     ]
Years of Experience   [15 years          ]
Qualifications        
  • MBBS - Harvard Medical School (2006)
  • MD Cardiology - Johns Hopkins (2010)
  • Fellowship - Mayo Clinic (2012)

Languages Spoken
  ☑ English  ☑ Spanish  ☐ French

Consultation Fee      [$150              ]
Consultation Duration [30 minutes        ]

Hospital Affiliations
  • City Hospital (Primary)
  • Community Medical Center
  • Regional Healthcare

Awards & Recognition
  • Best Doctor Award 2023
  • Patient Choice Award 2022
```

### 4.7 Availability Schedule (Doctor)

**Container:**
- Background: `bg-white`
- Rounded: `rounded-2xl`
- Padding: `p-6`
- Shadow: `shadow-lg`

**Header:**
- Title: "Availability Schedule"
- Toggle: "Currently accepting patients" (on/off)

**Weekly Schedule:**
```
Monday      09:00 AM - 05:00 PM  [Edit]
Tuesday     09:00 AM - 05:00 PM  [Edit]
Wednesday   09:00 AM - 01:00 PM  [Edit]
Thursday    09:00 AM - 05:00 PM  [Edit]
Friday      09:00 AM - 05:00 PM  [Edit]
Saturday    10:00 AM - 02:00 PM  [Edit]
Sunday      Closed               [Edit]
```

**Time Slot Manager:**
- Click day to edit
- Add break times
- Set different time slots
- Mark days off
- Set vacation periods

---

## 5. Settings Page

### 5.1 Page Overview

**Purpose:** Configure account, privacy, notifications, and preferences

**Layout:** Tabbed navigation with sections

```
┌─────────────────────────────────────────────────────────┐
│  Settings                                               │
│                                                         │
│  [Account] [Privacy] [Notifications] [Security]        │
│  [Preferences] [Billing]                                │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │                                                  │  │
│  │  Selected Tab Content                            │  │
│  │                                                  │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 5.2 Tab Navigation

**Style:**
- Container: `border-b border-gray-200 mb-8`
- Layout: `flex gap-8 overflow-x-auto`
- Tab: `pb-4 px-1 text-base font-medium`
- Active: `border-b-2 border-primary-600 text-primary-600`
- Inactive: `text-gray-600 hover:text-gray-900`

### 5.3 Account Settings Tab

**Section: Profile Settings**

```
Profile Visibility
○ Public    Anyone can view my profile
● Private   Only connected users
○ Hidden    Invisible to others

Profile URL
medinova.ai/doctor/john-doe
[Copy Link]

Delete Account
[Delete My Account]
Warning: This action cannot be undone
```

**Section Style:**
- Card container: White background, rounded, shadow
- Section title: `text-lg font-semibold mb-4`
- Options: Radio buttons or toggles
- Danger zone: Red border, warning color

### 5.4 Privacy Settings Tab

```
┌──────────────────────────────────────┐
│ Data Sharing                         │
│                                      │
│ Share health data with doctors       │
│ [Toggle: ON]                         │
│                                      │
│ Allow AI analysis                    │
│ [Toggle: ON]                         │
│                                      │
│ Share anonymous data for research    │
│ [Toggle: OFF]                        │
│                                      │
│ ──────────────────────────────────── │
│                                      │
│ Medical Records Access               │
│                                      │
│ Who can view my records?             │
│ ● My doctors only                    │
│ ○ My doctors and specialists         │
│ ○ Healthcare network                 │
│                                      │
│ ──────────────────────────────────── │
│                                      │
│ Download My Data                     │
│ Request a copy of all your data      │
│ [Request Data Export]                │
│                                      │
└──────────────────────────────────────┘
```

**Toggle Switch:**
- On: `bg-primary-600`
- Off: `bg-gray-300`
- Circle: Slides left/right
- Label: Describes what toggle controls

### 5.5 Notification Settings Tab

```
┌──────────────────────────────────────┐
│ Push Notifications                   │
│                                      │
│ Appointment reminders    [Toggle: ON]│
│ Medication reminders     [Toggle: ON]│
│ Lab results ready        [Toggle: ON]│
│ New messages            [Toggle: ON]│
│ System updates          [Toggle: OFF]│
│ Marketing emails        [Toggle: OFF]│
│                                      │
│ ──────────────────────────────────── │
│                                      │
│ Email Notifications                  │
│                                      │
│ Daily health summary     [Toggle: ON]│
│ Weekly reports          [Toggle: ON]│
│ New features            [Toggle: OFF]│
│ Newsletters             [Toggle: OFF]│
│                                      │
│ ──────────────────────────────────── │
│                                      │
│ SMS Notifications                    │
│                                      │
│ Appointment confirmations[Toggle: ON]│
│ Emergency alerts        [Toggle: ON]│
│ Payment confirmations   [Toggle: ON]│
│                                      │
│ ──────────────────────────────────── │
│                                      │
│ Quiet Hours                          │
│ Mute notifications during:           │
│ From: [10:00 PM]  To: [07:00 AM]    │
│ [Toggle: ON]                         │
│                                      │
└──────────────────────────────────────┘
```

**Notification Item:**
- Layout: `flex justify-between items-center py-3`
- Label: `text-sm font-medium text-gray-700`
- Description: `text-xs text-gray-500`
- Toggle: Right-aligned

### 5.6 Security Settings Tab

```
┌──────────────────────────────────────┐
│ Password                             │
│                                      │
│ Last changed: 30 days ago            │
│ [Change Password]                    │
│                                      │
│ ──────────────────────────────────── │
│                                      │
│ Two-Factor Authentication            │
│                                      │
│ Status: ✓ Enabled                    │
│ Method: SMS to +1 (555) ***-**67    │
│ [Change Method] [Disable]            │
│                                      │
│ ──────────────────────────────────── │
│                                      │
│ Active Sessions                      │
│                                      │
│ ● Current Device                     │
│   Windows PC • Chrome                │
│   New York, USA • Just now           │
│                                      │
│ ○ iPhone 13                          │
│   Mobile App                         │
│   New York, USA • 2 hours ago        │
│   [Revoke]                           │
│                                      │
│ [Sign Out All Devices]               │
│                                      │
│ ──────────────────────────────────── │
│                                      │
│ Login History                        │
│ View your recent login activity      │
│ [View History]                       │
│                                      │
└──────────────────────────────────────┘
```

**Active Session:**
- Current: Green dot, can't revoke
- Other: Gray dot, can revoke
- Device icon + info
- Location + timestamp
- Revoke button

### 5.7 Preferences Tab

```
┌──────────────────────────────────────┐
│ Appearance                           │
│                                      │
│ Theme                                │
│ ○ Light  ● Auto  ○ Dark             │
│                                      │
│ ──────────────────────────────────── │
│                                      │
│ Language & Region                    │
│                                      │
│ Language: [English ▼]                │
│ Timezone: [EST (UTC-5) ▼]            │
│ Date Format: [MM/DD/YYYY ▼]          │
│ Time Format: ○ 12-hour ● 24-hour    │
│                                      │
│ ──────────────────────────────────── │
│                                      │
│ Accessibility                        │
│                                      │
│ Font Size                            │
│ ○ Small  ● Medium  ○ Large          │
│                                      │
│ High Contrast Mode   [Toggle: OFF]   │
│ Screen Reader Support[Toggle: OFF]   │
│                                      │
│ ──────────────────────────────────── │
│                                      │
│ Default Views                        │
│                                      │
│ Dashboard Layout                     │
│ [Compact ▼]                          │
│                                      │
│ Calendar View                        │
│ [Week ▼]                             │
│                                      │
└──────────────────────────────────────┘
```

### 5.8 Billing Tab (If applicable)

```
┌──────────────────────────────────────┐
│ Subscription Plan                    │
│                                      │
│ Current Plan: Premium                │
│ $29.99/month                         │
│ Renews on: December 15, 2026         │
│                                      │
│ [Upgrade Plan] [Cancel Subscription] │
│                                      │
│ ──────────────────────────────────── │
│                                      │
│ Payment Methods                      │
│                                      │
│ ● Visa ending in 4242                │
│   Expires 12/2027                    │
│   [Edit] [Remove]                    │
│                                      │
│ [+ Add Payment Method]               │
│                                      │
│ ──────────────────────────────────── │
│                                      │
│ Billing History                      │
│                                      │
│ Nov 15, 2026  $29.99  [Download]     │
│ Oct 15, 2026  $29.99  [Download]     │
│ Sep 15, 2026  $29.99  [Download]     │
│                                      │
│ [View All Invoices]                  │
│                                      │
└──────────────────────────────────────┘
```

---

## 6. Health Analytics

### 6.1 Page Overview

**Purpose:** Visualize health trends, metrics, and AI-powered insights

**Features:**
- Interactive charts
- Multiple health metrics
- Trend analysis
- AI recommendations
- Exportable reports

### 6.2 Page Header

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ Health Analytics                     [Export] [Settings]│
│                                                          │
│ [Week] [Month] [3 Months] [Year] [Custom]              │
└─────────────────────────────────────────────────────────┘
```

**Date Range Selector:**
- Pills design
- Active: `bg-primary-100 text-primary-700`
- Custom: Opens date picker

### 6.3 Overview Cards

**Grid:** `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8`

**Card: Avg Heart Rate**
```
┌────────────────────┐
│ [Heart Icon]       │
│                    │
│ 72 bpm             │
│ Average Heart Rate │
│                    │
│ Trend: [Mini Chart]│
│ ↓ 3% from last week│
└────────────────────┘
```

**Mini Chart:**
- Sparkline showing last 7 days
- Color: Success (improving) or warning (declining)
- Height: `h-8`

**Other Cards:**
- Blood Pressure (120/80)
- Steps (8,450 avg)
- Sleep (7.2 hrs avg)

### 6.4 Main Chart Section

**Container:**
- Background: `bg-white`
- Rounded: `rounded-2xl`
- Padding: `p-6`
- Shadow: `shadow-lg`
- Full width

**Chart Header:**
- Title: "Health Metrics Over Time"
- Metric selector: Checkboxes
  - ☑ Heart Rate
  - ☑ Blood Pressure
  - ☐ Weight
  - ☐ Blood Sugar
  - ☐ Oxygen Level

**Chart:**
- Type: Multi-line chart
- Height: `h-96`
- Interactive: Hover for values
- Zoom: Click and drag
- Legend: Bottom, color-coded
- Grid lines: Subtle
- Tooltips: Show date, value, metric

**Chart Controls:**
- Export: PNG, PDF, CSV
- Full screen: Expand button
- Share: Share button

### 6.5 Detailed Metrics Grid

**Layout:**
```
┌─────────────────────┬─────────────────────┐
│                     │                     │
│ Heart Rate Detail   │ Blood Pressure      │
│                     │                     │
├─────────────────────┼─────────────────────┤
│                     │                     │
│ Weight Tracking     │ Sleep Analysis      │
│                     │                     │
└─────────────────────┴─────────────────────┘
```

**Metric Detail Card:**
```
Heart Rate Analysis
────────────────────

Current:  72 bpm
Min:      65 bpm (Today 3:00 AM)
Max:      98 bpm (Today 2:00 PM)
Average:  74 bpm

[Line Chart - Last 24 Hours]

Insights:
• Heart rate variability is good
• Resting heart rate improved by 5%
• Peak heart rate during exercise normal

[View Full Report]
```

**Card Style:**
- Background: `bg-white`
- Border: `border-l-4` (colored by metric)
- Stats: Key-value pairs
- Chart: Small embedded chart
- Insights: Bullet list with AI icon


### 6.6 AI Insights Panel

**Container:**
- Background: `bg-gradient-to-br from-info-50 to-info-100`
- Rounded: `rounded-2xl`
- Padding: `p-6`
- Border: `border border-info-200`

**Header:**
- Icon: Brain/Sparkles icon, `w-8 h-8 text-info-600`
- Title: "AI Health Insights"
- Subtitle: "Based on your health data"

**Insight Items:**
```
✓ Your sleep quality has improved by 15%
  Keep maintaining your current sleep schedule

⚠ Blood pressure slightly elevated today
  Consider reducing salt intake

✓ Activity level is excellent this week
  You've achieved your step goal 6/7 days

📊 Heart rate variability trending upward
  This indicates better cardiovascular fitness
```

**Item Style:**
- Icon: Status-based (check, warning, chart)
- Title: `font-semibold text-gray-900`
- Description: `text-sm text-gray-600`
- Spacing: `mb-4`
- Background: `bg-white/50 p-3 rounded-lg`

### 6.7 Goals & Progress

**Container:**
- Background: `bg-white`
- Rounded: `rounded-2xl`
- Padding: `p-6`
- Shadow: `shadow-lg`

**Header:**
- Title: "Health Goals"
- Button: "+ Add Goal"

**Goal Cards:**
```
Weight Loss Goal
━━━━━━━━━━━━━━━━━━━━ 65%
Current: 78kg | Target: 75kg | 3kg to go
Target Date: December 31, 2026
On track to achieve ✓

Exercise Goal  
━━━━━━━━━━━━━━━━━━━━ 80%
4 of 5 days this week
Target: 5 days/week

Water Intake
━━━━━━━━━━━━━━━━━━━━ 90%
1.8L of 2L today
```

**Progress Bar:**
- Background: `bg-gray-200`
- Fill: Gradient based on progress
- Percentage shown
- Status text below

---

## 7. Appointment Booking

### 7.1 Page Overview

**Purpose:** Find doctors and book appointments

**Flow:**
1. Search/Filter doctors
2. View doctor profile
3. Select date & time
4. Confirm booking

### 7.2 Page Layout

```
┌─────────────────────────────────────────────────────────┐
│ Book Appointment                                        │
│                                                         │
│ [Search] [Specialization ▼] [Location ▼] [Date ▼]     │
├──────────────────────┬──────────────────────────────────┤
│                      │                                  │
│  Doctor List         │  Calendar / Details              │
│  (Scrollable)        │                                  │
│                      │                                  │
└──────────────────────┴──────────────────────────────────┘
```

### 7.3 Search & Filters

**Search Bar:**
- Placeholder: "Search by doctor name, specialization, or hospital"
- Icon: Search icon
- Width: Full width
- Suggestions dropdown on type

**Filter Pills:**
- Specialization dropdown
- Location dropdown
- Date picker
- Price range slider
- Rating filter (4+ stars)
- Availability: Today, Tomorrow, This Week

### 7.4 Doctor List

**Doctor Card:**
```
┌────────────────────────────────────┐
│ [Photo] Dr. Sarah Johnson          │
│         ⭐ 4.9 (156 reviews)        │
│         Cardiologist               │
│         15 years experience        │
│                                    │
│ 📍 City Hospital                   │
│ 💰 $150 per consultation           │
│ 🕐 Next available: Tomorrow 10 AM  │
│                                    │
│ [View Profile] [Book Now →]       │
└────────────────────────────────────┘
```

**Card Style:**
- Background: `bg-white`
- Border: `border border-gray-200`
- Rounded: `rounded-xl`
- Padding: `p-4`
- Hover: `hover:border-primary-500 hover:shadow-lg`
- Margin: `mb-4`

**Available Badge:**
- Text: "Available Now"
- Color: `bg-success-100 text-success-700`
- Position: Top-right corner

### 7.5 Doctor Detail Panel

**When doctor selected:**

**Profile Section:**
```
Dr. Sarah Johnson
Cardiologist, MD
⭐ 4.9 | 156 reviews | 245 consultations

[Message] [Video Call] [In-Person]

About:
Board-certified cardiologist with 15 years 
of experience specializing in interventional 
cardiology...

Specializations:
• Heart Disease
• Hypertension
• Arrhythmia

Education:
• MD - Harvard Medical School
• Residency - Johns Hopkins

Languages:
English, Spanish
```

### 7.6 Calendar View

**Month Calendar:**
```
    December 2026
Su Mo Tu We Th Fr Sa
          1  2  3  4
 5  6  7  8  9 10 11
12 13 14 15 16 17 18
19 20 21 22 23 24 25
26 27 28 29 30 31
```

**Date Indicators:**
- Available: Default style
- Partially booked: Orange dot
- Fully booked: Red, crossed out
- Selected: `bg-primary-600 text-white`
- Today: Blue border

**Time Slots:**
```
Morning
[09:00] [09:30] [10:00] [10:30]
[11:00] [11:30]

Afternoon
[14:00] [14:30] [15:00] [15:30]
[16:00] [16:30]

Evening
[18:00] [18:30]
```

**Slot Style:**
- Available: `bg-white border-2 border-gray-300`
- Selected: `bg-primary-600 text-white`
- Booked: `bg-gray-100 text-gray-400 cursor-not-allowed`
- Hover: `hover:border-primary-500`

### 7.7 Booking Confirmation

**Modal/Card:**
```
┌──────────────────────────────────┐
│ Confirm Appointment              │
│                                  │
│ Doctor: Dr. Sarah Johnson        │
│ Date: December 15, 2026          │
│ Time: 10:00 AM                   │
│ Type: Video Consultation         │
│ Duration: 30 minutes             │
│ Fee: $150                        │
│                                  │
│ Reason for visit (Optional)      │
│ [Text area]                      │
│                                  │
│ [Back] [Confirm Booking]         │
└──────────────────────────────────┘
```

**Success State:**
- Confetti animation
- Success message
- Appointment details
- Add to calendar button
- Payment option (if required)

---

## 8. Medicine Reminder

### 8.1 Page Overview

**Purpose:** Manage medication schedules and reminders

**Features:**
- Add medications
- Set schedules
- Track adherence
- Refill reminders
- Drug interaction warnings

### 8.2 Page Header

```
Medicine Reminders                [+ Add Medicine]

[All] [Today] [Upcoming] [Completed]
```

**Tab Filters:**
- Pills style navigation
- Show different views

### 8.3 Today's Medications

**Timeline View:**
```
Morning (3 medicines)

● 08:00 AM - Taken ✓
  Aspirin 100mg
  After breakfast

● 08:30 AM - Missed ⚠
  Metformin 500mg
  With food
  [Mark as Taken] [Skip] [Snooze 30min]

Afternoon (2 medicines)

○ 01:00 PM - Upcoming
  Vitamin D
  After lunch
  [Set Reminder]

Evening (1 medicine)

○ 08:00 PM - Scheduled
  Blood Pressure Med
  Before dinner
```

**Status Icons:**
- Taken: Check circle, green
- Missed: Alert triangle, red/orange
- Upcoming: Empty circle, blue
- Scheduled: Clock, gray

### 8.4 Medicine Card

**Detailed View:**
```
┌────────────────────────────────────┐
│ [Pill Icon] Aspirin 100mg          │
│                                    │
│ Schedule:                          │
│ Daily, 8:00 AM                     │
│ After breakfast                    │
│                                    │
│ Adherence: ●●●●●●●○○○ 75%         │
│ 21 of 28 days                      │
│                                    │
│ Stock: 15 tablets left             │
│ ⚠ Refill needed in 7 days          │
│                                    │
│ Next dose: Tomorrow 8:00 AM        │
│                                    │
│ [Edit] [Delete] [Refill]           │
└────────────────────────────────────┘
```

**Card Style:**
- Background: `bg-white`
- Border-left: Color-coded by category
- Rounded: `rounded-xl`
- Shadow: `shadow-md`
- Padding: `p-6`

### 8.5 Add Medicine Form

**Modal/Slide-over:**
```
Add New Medicine

Medicine Name *
[Search or enter name]

Dosage *
[Amount] [Unit ▼]
100      mg

Schedule *
○ Daily
○ Specific days
○ As needed

Time(s) *
[+ Add Time]
[08:00 AM] [×]
[08:00 PM] [×]

Instructions
○ Before meal
● After meal
○ With meal
○ Any time

Duration
From: [Start Date]
To:   [End Date] or ☑ Ongoing

Stock Tracking
Initial quantity: [30] tablets
Refill reminder: [7] days before

[Cancel] [Add Medicine]
```

### 8.6 Adherence Calendar

**Month View:**
```
    December 2026
Mo Tu We Th Fr Sa Su
       ✓  ✓  ✓  ✓
 ✓  ✓  ⚠  ✓  ✓  ✓  ✓
 ✓  ✓  ✓  •  •  •  •
```

**Legend:**
- ✓ All taken
- ⚠ Some missed
- ✗ All missed
- • Future dates

**Stats:**
- Overall adherence: 85%
- Streak: 12 days
- Missed: 3 in last month

### 8.7 Drug Interactions

**Alert Card:**
```
⚠ Drug Interaction Warning

Aspirin + Ibuprofen
Moderate Interaction

Taking these together may increase risk
of stomach bleeding.

Recommendation:
Take at least 2 hours apart

[Learn More] [Dismiss]
```

**Alert Style:**
- Background: `bg-warning-50`
- Border: `border-l-4 border-warning-500`
- Icon: Alert triangle
- Critical: Red color scheme
- Moderate: Orange
- Minor: Yellow

---

## 9. Medical Report Upload

### 9.1 Page Overview

**Purpose:** Upload and manage medical documents

**Supported:**
- Lab reports
- Prescriptions
- X-rays, CT scans, MRI
- Doctor notes
- Insurance documents

### 9.2 Page Layout

```
┌─────────────────────────────────────────────────────────┐
│ Medical Reports                     [Upload Document]   │
│                                                         │
│ [All] [Lab Reports] [Prescriptions] [Imaging] [Other]  │
├──────────────────────┬──────────────────────────────────┤
│                      │                                  │
│  Document List       │  Document Preview                │
│                      │                                  │
└──────────────────────┴──────────────────────────────────┘
```

### 9.3 Upload Area

**Drag & Drop Zone:**
```
┌────────────────────────────────────┐
│                                    │
│         [Upload Icon]              │
│                                    │
│  Drag and drop files here          │
│  or click to browse                │
│                                    │
│  Supported: PDF, JPG, PNG, DICOM   │
│  Max size: 10MB per file           │
│                                    │
└────────────────────────────────────┘
```

**Zone Style:**
- Border: `border-2 border-dashed border-gray-300`
- Background: `bg-gray-50`
- Hover: `hover:border-primary-500 hover:bg-primary-50`
- Padding: `p-12`
- Rounded: `rounded-xl`

**Upload Progress:**
```
Uploading lab_report.pdf
━━━━━━━━━━━━━━━━━━━━ 75%
Processing with AI...
```

### 9.4 Document List

**List View:**
```
┌────────────────────────────────────┐
│ 📄 Blood Test Report               │
│    December 10, 2026               │
│    Lab Report • 2.3 MB             │
│    [View] [Download] [Share] [×]   │
├────────────────────────────────────┤
│ 📷 Chest X-Ray                     │
│    December 5, 2026                │
│    Imaging • 5.1 MB                │
│    ✓ AI Analysis Available         │
│    [View] [Download] [Share] [×]   │
├────────────────────────────────────┤
│ 📝 Prescription                    │
│    December 1, 2026                │
│    Prescription • 1.2 MB           │
│    Dr. Sarah Johnson               │
│    [View] [Download] [Share] [×]   │
└────────────────────────────────────┘
```

**Document Card:**
- Icon: Based on type
- Name: `font-semibold text-gray-900`
- Date: `text-sm text-gray-500`
- Meta: Type, size, doctor
- Actions: Icon buttons
- AI badge: If analyzed

### 9.5 Document Preview

**PDF Viewer:**
- Embedded PDF viewer
- Zoom controls
- Page navigation
- Download button
- Print button
- Share button

**Image Viewer:**
- Full-size preview
- Zoom in/out
- Rotate
- Annotations support
- Comparison view (for before/after)

### 9.6 AI Analysis Results

**For Lab Reports:**
```
AI Analysis Results

Analyzed Parameters:
✓ Hemoglobin: 14.5 g/dL (Normal)
  Reference: 13.5-17.5 g/dL

⚠ Cholesterol: 240 mg/dL (High)
  Reference: <200 mg/dL
  Recommendation: Consult doctor

✓ Blood Glucose: 95 mg/dL (Normal)
  Reference: 70-100 mg/dL

Summary:
1 parameter requires attention.
Consider consulting your doctor.

[Download Report] [Share with Doctor]
```

**For X-Rays:**
```
AI Analysis

Image Quality: Good
Body Part: Chest

Findings:
• No acute abnormalities detected
• Cardiac silhouette within normal limits
• Lung fields clear

⚠ AI analysis is not a substitute for
  professional medical diagnosis

[View Detailed Analysis]
```

### 9.7 Share Document

**Share Modal:**
```
Share with Doctor

Select Doctor:
[Doctor Dropdown]

Add Note (Optional):
[Text area]

Expiry:
○ 24 hours
● 7 days
○ 30 days
○ No expiry

☑ Allow doctor to download

[Cancel] [Share]
```

**Share Link:**
- Generated secure link
- Copy button
- QR code option
- Access tracking

---

## 10. Hospital Finder

### 10.1 Page Overview

**Purpose:** Find nearby hospitals and healthcare facilities

**Features:**
- Map view
- List view
- Filters by specialty
- Directions
- Contact info

### 10.2 Page Layout

```
┌─────────────────────────────────────────────────────────┐
│ Find Hospitals                                          │
│                                                         │
│ [Search] [Filter] [My Location]        [Map] [List]    │
├──────────────────────┬──────────────────────────────────┤
│                      │                                  │
│  Hospital List       │  Map View                        │
│  (Scrollable)        │  (Interactive)                   │
│                      │                                  │
└──────────────────────┴──────────────────────────────────┘
```

### 10.3 Search & Filters

**Search Bar:**
- Placeholder: "Search hospitals, clinics, pharmacies..."
- Location input: Auto-detect or manual
- Radius: 5km, 10km, 25km, 50km

**Filters:**
```
Type:
☑ Hospital
☑ Clinic
☑ Pharmacy
☐ Lab
☐ Emergency

Specialty:
☐ Cardiology
☐ Orthopedics
☐ Pediatrics
☐ Emergency
☐ All

Services:
☐ 24/7 Emergency
☐ ICU
☐ Pharmacy
☐ Lab
☐ Ambulance

[Apply Filters]
```

### 10.4 Hospital Card (List View)

```
┌────────────────────────────────────┐
│ City General Hospital         ⭐ 4.7│
│ 📍 2.3 km away • Open 24/7         │
│                                    │
│ Specialties:                       │
│ • Emergency Care                   │
│ • Cardiology                       │
│ • Orthopedics                      │
│                                    │
│ 📞 +1 (555) 123-4567               │
│ 🚑 Emergency: Yes                  │
│ 🏥 ICU: Available                  │
│                                    │
│ [Directions] [Call] [Website]      │
└────────────────────────────────────┘
```

**Card Style:**
- Background: `bg-white`
- Border: `border border-gray-200`
- Rounded: `rounded-xl`
- Padding: `p-4`
- Shadow: `shadow-md`
- Hover: `hover:shadow-lg`

**Distance Badge:**
- Position: Top-right
- Color: Green (<5km), Yellow (5-10km), Gray (>10km)
- Shows: Distance from user

### 10.5 Map View

**Interactive Map:**
- Library: Leaflet + OpenStreetMap
- Markers: Hospital locations
- Clusters: When zoomed out
- User location: Blue dot
- Selected: Highlighted marker

**Map Markers:**
- Hospital: Red cross icon
- Clinic: Blue plus icon
- Pharmacy: Green pill icon
- Current location: Blue dot with pulse

**Info Window:**
```
City General Hospital
⭐ 4.7 | 2.3 km away

[View Details] [Directions]
```

### 10.6 Hospital Detail View

**When hospital selected:**
```
City General Hospital
⭐⭐⭐⭐⭐ 4.7 (234 reviews)

[Call] [Directions] [Website] [Share]

📍 Address:
123 Medical Center Dr
New York, NY 10001

📞 Contact:
Main: +1 (555) 123-4567
Emergency: 911

🕐 Hours:
24/7 Emergency Services
Outpatient: 8 AM - 8 PM

Specialties & Services:
• Emergency Care (24/7)
• Cardiology
• Orthopedics
• Pediatrics
• ICU (20 beds)
• Pharmacy
• Laboratory

Insurance Accepted:
Blue Cross, Aetna, Cigna, Medicare

Reviews:
⭐⭐⭐⭐⭐ "Excellent emergency care..."
⭐⭐⭐⭐ "Long wait times but good doctors..."

[Write a Review]
```

### 10.7 Directions

**Route Display:**
```
Route to City General Hospital
━━━━━━━━━━━━━━━━━━━━ 2.3 km

🚗 By Car: 8 minutes
🚶 Walking: 28 minutes
🚌 Public Transit: 15 minutes

Turn-by-turn directions:
1. Head north on Main St
2. Turn right onto 5th Ave
3. Destination on left

[Start Navigation] [Share Route]
```

---

## 11. AI Chat (Symptom Checker)

### 11.1 Page Overview

**Purpose:** Interactive AI-powered symptom analysis

**Features:**
- Natural language input
- Multi-turn conversation
- Symptom extraction
- Urgency assessment
- Doctor recommendations

### 11.2 Page Layout

```
┌─────────────────────────────────────────────────────────┐
│ AI Health Assistant                           [History] │
│                                                         │
│ ┌─────────────────────────────────────────────────────┐│
│ │                                                     ││
│ │  Chat Area                                          ││
│ │  (Scrollable conversation)                          ││
│ │                                                     ││
│ └─────────────────────────────────────────────────────┘│
│                                                         │
│ [Message Input] [Send]                                 │
└─────────────────────────────────────────────────────────┘
```

### 11.3 Welcome Screen

**Initial State:**
```
┌───────────────────────────────────────┐
│                                       │
│         [AI Robot Icon]               │
│                                       │
│   Hi! I'm your AI Health Assistant    │
│                                       │
│   How are you feeling today?          │
│   Tell me about your symptoms         │
│                                       │
│   Quick starts:                       │
│   • I have a headache                 │
│   • Fever and cough                   │
│   • Stomach pain                      │
│   • General checkup                   │
│                                       │
└───────────────────────────────────────┘
```

**Quick Start Buttons:**
- Style: `bg-gray-100 hover:bg-primary-50 px-4 py-2 rounded-xl`
- Click: Starts conversation with pre-filled message

### 11.4 Chat Messages

**User Message:**
```
┌────────────────────────┐
│ I have a headache and  │
│ feel dizzy             │
└────────────────────────┘
                   [Avatar]
```

**Style:**
- Alignment: Right
- Background: `bg-primary-600 text-white`
- Rounded: `rounded-2xl rounded-br-sm`
- Padding: `px-4 py-3`
- Max width: `max-w-lg`

**AI Message:**
```
[AI Icon]
┌────────────────────────────────┐
│ I understand you're experiencing│
│ headache and dizziness.        │
│                                │
│ To better help you, could you  │
│ tell me:                       │
│ • How long have you had these  │
│   symptoms?                    │
│ • Rate your headache severity  │
│   (1-10)                       │
│ • Any other symptoms?          │
└────────────────────────────────┘
```

**Style:**
- Alignment: Left
- Background: `bg-gray-100 text-gray-900`
- Rounded: `rounded-2xl rounded-bl-sm`
- Padding: `px-4 py-3`
- Max width: `max-w-2xl`
- Typing indicator: Animated dots while thinking

### 11.5 Symptom Summary Card

**After symptom extraction:**
```
┌──────────────────────────────────┐
│ Symptom Summary                  │
│                                  │
│ • Headache                       │
│   Severity: 7/10                 │
│   Duration: 2 days               │
│   Location: Frontal              │
│                                  │
│ • Dizziness                      │
│   Severity: 5/10                 │
│   Duration: 1 day                │
│   Occurs when: Standing up       │
│                                  │
│ Urgency Level: ⚠ Moderate        │
│                                  │
│ [Edit] [Continue]                │
└──────────────────────────────────┘
```

**Card Style:**
- Background: `bg-white`
- Border: `border-2 border-primary-200`
- Rounded: `rounded-xl`
- Shadow: `shadow-lg`
- Embedded in chat

### 11.6 AI Assessment Result

```
┌──────────────────────────────────┐
│ Assessment Complete              │
│                                  │
│ Based on your symptoms:          │
│                                  │
│ Possible Conditions:             │
│ 1. Tension Headache (75%)        │
│ 2. Migraine (45%)                │
│ 3. Dehydration (30%)             │
│                                  │
│ Recommendations:                 │
│ ✓ Rest in a dark, quiet room    │
│ ✓ Stay hydrated                  │
│ ✓ Take OTC pain reliever         │
│ ⚠ If symptoms worsen, seek care  │
│                                  │
│ [Find Doctor] [Get Prescription] │
└──────────────────────────────────┘
```

**Urgency Indicator:**
- Low: Green icon, "Monitor at home"
- Moderate: Yellow icon, "See doctor soon"
- High: Orange icon, "See doctor today"
- Emergency: Red icon, "Seek emergency care"

### 11.7 Follow-up Actions

**Action Buttons:**
```
What would you like to do?

[Book Appointment with Doctor]
[Find Nearby Hospital]
[Get Home Remedies]
[Talk to Human Agent]
[Start New Consultation]
```

**Button Style:**
- Full width in chat
- Icon + text
- Rounded: `rounded-xl`
- Shadow on hover

### 11.8 Chat Input

**Input Area:**
```
┌────────────────────────────────────────────┐
│ [📎] Type your message...          [Send] │
└────────────────────────────────────────────┘
```

**Features:**
 - Attachment button: Upload images
- Emoji picker
- Voice input option
- Auto-resize as user types
- Send on Enter
- Shift+Enter for new line

**Typing Indicator:**
```
AI is typing...
●●● (animated)
```

### 11.9 Disclaimer

**Bottom of Chat:**
```
⚠ Disclaimer
This AI assistant provides preliminary
information only and is not a substitute
for professional medical advice.
```

**Style:**
- Background: `bg-warning-50`
- Text: `text-xs text-gray-600`
- Padding: `p-3`
- Always visible

---

## Summary

**Completed Dashboard Designs:**
1. ✅ Patient Dashboard - Health overview, appointments, metrics
2. ✅ Doctor Dashboard - Schedule, patient queue, performance
3. ✅ Admin Dashboard - Platform analytics, user management
4. ✅ Profile Page - Personal and professional info
5. ✅ Settings Page - 6 tabs with all configurations
6. ✅ Health Analytics - Charts, trends, AI insights
7. ✅ Appointment Booking - Search, calendar, confirmation
8. ✅ Medicine Reminder - Schedule, tracking, adherence
9. ✅ Medical Report Upload - Upload, preview, AI analysis
10. ✅ Hospital Finder - Map view, list, directions
11. ✅ AI Chat - Symptom checker with conversation

**Design System Applied:**
- Glassmorphism effects
- Healthcare color palette
- Consistent spacing
- Responsive layouts
- Accessibility features
- Interactive components
- Real-time updates
- Status indicators

**Ready for Implementation** ✅

---

**End of Dashboard Designs Document**
