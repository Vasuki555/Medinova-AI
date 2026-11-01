# MediNova AI: Page Designs
## Authentication & Landing Pages

---

**Project:** MediNova AI - Multi-Agent Healthcare Intelligence Platform  
**Design Style:** Healthcare Theme with Glassmorphism  
**Framework:** Tailwind CSS + React.js  
**Date:** July 2, 2026  

---

## Table of Contents

1. [Landing Page](#1-landing-page)
2. [Login Page](#2-login-page)
3. [Register Page](#3-register-page)
4. [Forgot Password Page](#4-forgot-password-page)
5. [OTP Verification Page](#5-otp-verification-page)
6. [Reset Password Page](#6-reset-password-page)

---

## 1. Landing Page

### 1.1 Page Overview

**Purpose:** Introduce MediNova AI, showcase features, and drive user registrations

**Layout:** Full-page scrollable with multiple sections

**Color Scheme:**
- Background: Gradient from primary-50 to white with subtle medical illustrations
- Primary CTAs: primary-600 (Medical Blue)
- Accents: success-500 (Health Green) and accent-500 (Warm Coral)

### 1.2 Navigation Bar (Sticky)

**Position:** Fixed at top, sticky on scroll

**Structure:**
```
┌─────────────────────────────────────────────────────────────┐
│ [Logo] MediNova AI    Features  How It Works  About  Blog  │
│                                                              │
│                                     [Login] [Get Started →] │
└─────────────────────────────────────────────────────────────┘
```

**Details:**
- **Container:** 
  - Glass effect: `bg-white/80 backdrop-blur-lg`
  - Border: `border-b border-gray-200`
  - Shadow: `shadow-md`
  - Padding: `px-8 py-4`
  - Max width: `max-w-7xl mx-auto`

- **Logo Section:**
  - Icon: Medical heart with pulse line (primary-600)
  - Size: `w-10 h-10`
  - Text: "MediNova AI" 
  - Font: `font-heading text-xl font-bold text-gray-900`
  - Spacing: `flex items-center space-x-3`

- **Navigation Links:**
  - Font: `text-sm font-medium text-gray-700`
  - Hover: `hover:text-primary-600`
  - Spacing: `space-x-8`
  - Hidden on mobile: `hidden md:flex`

- **Login Button (Ghost):**
  - Style: `px-5 py-2 rounded-xl text-primary-600 font-semibold`
  - Hover: `hover:bg-primary-50`

- **Get Started Button (Primary):**
  - Style: `px-6 py-2.5 bg-primary-600 text-white rounded-xl font-semibold`
  - Shadow: `shadow-lg shadow-primary-500/20`
  - Hover: `hover:bg-primary-700 hover:scale-105`
  - Icon: Arrow right icon

- **Mobile Menu Button:**
  - Display: `md:hidden`
  - Icon: Menu icon `w-6 h-6`
  - Style: `p-2 rounded-lg hover:bg-gray-100`

### 1.3 Hero Section

**Layout:** Full viewport height with split design

**Structure:**
```
┌───────────────────────────────────────────────────────────────┐
│                                                               │
│    Your AI Health                    [3D Medical             │
│    Companion                          Illustration           │
│                                       - Doctor avatar         │
│    Get instant symptom analysis,      - Heart monitor        │
│    connect with doctors, and manage   - Medical charts       │
│    your health journey—all powered    - Floating UI cards]   │
│    by advanced AI agents.                                    │
│                                                               │
│    [Get Started Free →]  [Watch Demo ▶]                      │
│                                                               │
│    ✓ AI-Powered Diagnosis  ✓ 24/7 Support  ✓ Secure         │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

**Details:**

- **Background:**
  - Gradient: `bg-gradient-to-br from-primary-50 via-white to-success-50`
  - Pattern: Subtle medical icons pattern (pills, heartbeat, cross) with `opacity-5`
  - Height: `min-h-screen`
  - Padding: `px-8 py-20`

- **Content Container:**
  - Layout: `grid grid-cols-1 lg:grid-cols-2 gap-12 items-center`
  - Max width: `max-w-7xl mx-auto`

- **Left Column (Text Content):**

  **Main Heading:**
  - Text: "Your AI Health Companion"
  - Font: `font-heading text-5xl lg:text-6xl font-extrabold`
  - Color: `text-gray-900`
  - Line height: `leading-tight`
  - Margin: `mb-6`
  - Animation: Fade in from left

  **Subheading:**
  - Text: "Get instant symptom analysis..."
  - Font: `text-lg lg:text-xl font-normal`
  - Color: `text-gray-600`
  - Line height: `leading-relaxed`
  - Max width: `max-w-xl`
  - Margin: `mb-8`
  - Animation: Fade in with delay

  **CTA Buttons:**
  - Container: `flex flex-col sm:flex-row gap-4`
  
  **Primary Button (Get Started):**
  - Style: `px-8 py-4 bg-primary-600 text-white text-lg font-semibold rounded-xl`
  - Shadow: `shadow-xl shadow-primary-500/30`
  - Hover: `hover:bg-primary-700 hover:scale-105`
  - Icon: Arrow right icon
  - Animation: Pulse effect on load

  **Secondary Button (Watch Demo):**
  - Style: `px-8 py-4 bg-white border-2 border-gray-300 text-gray-700 text-lg font-semibold rounded-xl`
  - Hover: `hover:bg-gray-50`
  - Icon: Play icon
  - Opens: Video modal

  **Trust Indicators:**
  - Container: `flex items-center flex-wrap gap-6 mt-10`
  - Each item: Check icon + text
  - Icon: `w-5 h-5 text-success-600`
  - Text: `text-sm font-medium text-gray-700`
  - Items: "AI-Powered Diagnosis", "24/7 Support", "Bank-Level Security"

- **Right Column (Illustration):**
  - 3D isometric medical illustration
  - Floating elements with subtle animation
  - Elements: Doctor avatar, heart monitor, medical charts
  - Glass cards showing AI analysis results
  - Animation: Floating and rotating elements
  - Mobile: Center-aligned, smaller size

### 1.4 Stats Section

**Layout:** Full-width with 4 stat cards

**Structure:**
```
┌──────────────────────────────────────────────────────────┐
│    [10,000+]        [500+]         [98%]        [24/7]   │
│    Patients         Doctors        Satisfaction  Support │
│    Served           Network        Rate                   │
└──────────────────────────────────────────────────────────┘
```

**Details:**
- **Container:**
  - Background: `bg-white`
  - Border: `border-y border-gray-200`
  - Padding: `py-16 px-8`

- **Grid Layout:**
  - Layout: `grid grid-cols-2 lg:grid-cols-4 gap-8`
  - Max width: `max-w-7xl mx-auto`

- **Each Stat Card:**
  - Alignment: `text-center`
  
  **Number:**
  - Font: `text-4xl lg:text-5xl font-bold font-heading`
  - Color: `text-primary-600`
  - Margin: `mb-2`
  - Animation: Count up on scroll into view
  
  **Label:**
  - Font: `text-sm lg:text-base font-medium`
  - Color: `text-gray-600`
  
  **Sublabel:**
  - Font: `text-xs`
  - Color: `text-gray-500`
  - Margin: `mt-1`

### 1.5 Features Section

**Title:** "Intelligent Healthcare at Your Fingertips"

**Layout:** 3-column grid with feature cards

**Structure:**
```
┌─────────────────────────────────────────────────────────────┐
│         Intelligent Healthcare at Your Fingertips           │
│         Experience the future of medical care               │
│                                                             │
│  [Card 1]          [Card 2]           [Card 3]             │
│  AI Symptom        Expert              Smart               │
│  Checker           Consultation        Health Records       │
│                                                             │
│  [Card 4]          [Card 5]           [Card 6]             │
│  Medication        Appointment        Health               │
│  Management        Booking            Analytics            │
└─────────────────────────────────────────────────────────────┘
```

**Details:**

- **Section Container:**
  - Background: `bg-gray-50`
  - Padding: `py-20 px-8`

- **Section Header:**
  - Max width: `max-w-3xl mx-auto text-center mb-16`
  
  **Title:**
  - Font: `text-4xl font-bold font-heading`
  - Color: `text-gray-900`
  - Margin: `mb-4`
  
  **Subtitle:**
  - Font: `text-lg`
  - Color: `text-gray-600`
  - Max width: `max-w-2xl mx-auto`

- **Features Grid:**
  - Layout: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8`
  - Max width: `max-w-7xl mx-auto`

- **Feature Card (Glass Style):**
  - Background: `bg-white/70 backdrop-blur-xl`
  - Border: `border border-white/30`
  - Shadow: `shadow-xl`
  - Padding: `p-8`
  - Rounded: `rounded-2xl`
  - Hover: `hover:shadow-2xl hover:scale-[1.02]`
  - Transition: `transition-all duration-300`

  **Card Content:**
  
  **Icon Container:**
  - Size: `w-14 h-14`
  - Background: `bg-primary-100`
  - Rounded: `rounded-xl`
  - Display: `flex items-center justify-center`
  - Margin: `mb-6`
  - Icon: Lucide icon, `w-7 h-7 text-primary-600`
  
  **Title:**
  - Font: `text-xl font-semibold font-heading`
  - Color: `text-gray-900`
  - Margin: `mb-3`
  
  **Description:**
  - Font: `text-base`
  - Color: `text-gray-600`
  - Line height: `leading-relaxed`
  
  **Learn More Link:**
  - Font: `text-sm font-semibold`
  - Color: `text-primary-600`
  - Hover: `hover:text-primary-700`
  - Icon: Arrow right
  - Margin: `mt-4`

**Feature 1: AI Symptom Checker**
- Icon: Activity (heart pulse)
- Title: "AI Symptom Checker"
- Description: "Describe your symptoms and get instant AI-powered preliminary assessment with urgency level detection"

**Feature 2: Expert Consultation**
- Icon: Video camera
- Title: "Expert Consultation"
- Description: "Connect with verified doctors through video calls for professional medical advice and prescriptions"

**Feature 3: Smart Health Records**
- Icon: FileText
- Title: "Smart Health Records"
- Description: "Securely store and access all your medical records, test results, and prescriptions in one place"

**Feature 4: Medication Management**
- Icon: Pill
- Title: "Medication Management"
- Description: "Get reminders for medications, track adherence, and receive drug interaction warnings"

**Feature 5: Appointment Booking**
- Icon: Calendar
- Title: "Easy Appointment Booking"
- Description: "Find nearby doctors, check availability, and book appointments with just a few clicks"

**Feature 6: Health Analytics**
- Icon: TrendingUp
- Title: "Health Analytics"
- Description: "Track your health trends with AI-powered insights and personalized wellness recommendations"

### 1.6 How It Works Section

**Title:** "Get Started in 3 Simple Steps"

**Layout:** Horizontal timeline with 3 steps

**Structure:**
```
┌─────────────────────────────────────────────────────────────┐
│              Get Started in 3 Simple Steps                  │
│                                                             │
│   [1]────────────►[2]────────────►[3]                      │
│   Sign Up         Describe        Get Care                  │
│   Create account  symptoms        Connect with              │
│   in 2 minutes    with AI         doctors                   │
└─────────────────────────────────────────────────────────────┘
```

**Details:**

- **Section Container:**
  - Background: `bg-white`
  - Padding: `py-20 px-8`

- **Section Header:**
  - Title font: `text-4xl font-bold text-center`
  - Margin: `mb-16`

- **Timeline Container:**
  - Layout: `flex flex-col lg:flex-row items-center justify-center gap-8 lg:gap-0`
  - Max width: `max-w-6xl mx-auto`

- **Each Step:**
  - Container: `flex-1 text-center relative`
  
  **Step Number:**
  - Size: `w-16 h-16`
  - Background: `bg-gradient-to-br from-primary-500 to-primary-700`
  - Text: `text-2xl font-bold text-white`
  - Display: `flex items-center justify-center`
  - Rounded: `rounded-full`
  - Shadow: `shadow-xl shadow-primary-500/30`
  - Position: `mx-auto mb-6`
  
  **Illustration:**
  - Simple icon illustration related to step
  - Size: `w-32 h-32 mx-auto mb-4`
  
  **Title:**
  - Font: `text-xl font-semibold`
  - Color: `text-gray-900`
  - Margin: `mb-3`
  
  **Description:**
  - Font: `text-base`
  - Color: `text-gray-600`
  - Max width: `max-w-xs mx-auto`

  **Arrow (Between Steps):**
  - Display: Desktop only `hidden lg:block`
  - Icon: ChevronRight, `text-gray-300`
  - Size: `w-8 h-8`
  - Position: Absolute, between steps

**Step 1: Sign Up**
- Number: 1
- Title: "Create Your Account"
- Description: "Sign up in under 2 minutes with your email or social accounts"
- Icon: User plus icon

**Step 2: Describe Symptoms**
- Number: 2
- Title: "Talk to Our AI"
- Description: "Describe your symptoms naturally and receive instant preliminary assessment"
- Icon: MessageCircle icon

**Step 3: Get Care**
- Number: 3
- Title: "Connect with Doctors"
- Description: "Book appointments or get emergency guidance based on urgency level"
- Icon: Stethoscope icon

### 1.7 Testimonials Section

**Title:** "Trusted by Thousands"

**Layout:** Card slider with 3 testimonials visible

**Structure:**
```
┌─────────────────────────────────────────────────────────────┐
│                  Trusted by Thousands                       │
│                                                             │
│  [Testimonial 1]  [Testimonial 2]  [Testimonial 3]        │
│  ⭐⭐⭐⭐⭐       ⭐⭐⭐⭐⭐       ⭐⭐⭐⭐⭐            │
│  "Quote..."       "Quote..."       "Quote..."              │
│  - Name           - Name           - Name                  │
│                                                             │
│              ○ ○ ● ○ ○ (Pagination dots)                   │
└─────────────────────────────────────────────────────────────┘
```

**Details:**

- **Section Container:**
  - Background: `bg-gradient-to-br from-primary-50 to-success-50`
  - Padding: `py-20 px-8`

- **Section Header:**
  - Title: `text-4xl font-bold text-center mb-4`
  - Subtitle: `text-lg text-gray-600 text-center mb-16`

- **Testimonial Card:**
  - Background: `bg-white`
  - Padding: `p-8`
  - Rounded: `rounded-2xl`
  - Shadow: `shadow-xl`
  - Border: `border border-gray-100`
  
  **Star Rating:**
  - Display: `flex gap-1 mb-4`
  - Stars: 5 filled stars, `text-warning-500 w-5 h-5`
  
  **Quote:**
  - Font: `text-lg`
  - Color: `text-gray-700`
  - Line height: `leading-relaxed`
  - Margin: `mb-6`
  - Quotes: Large opening quote mark in primary-200
  
  **Avatar + Info:**
  - Layout: `flex items-center gap-4`
  - Avatar: `w-12 h-12 rounded-full`
  - Name: `text-base font-semibold text-gray-900`
  - Role: `text-sm text-gray-500`

- **Slider Controls:**
  - Dots: `flex justify-center gap-2 mt-8`
  - Active dot: `w-8 h-2 bg-primary-600 rounded-full`
  - Inactive: `w-2 h-2 bg-gray-300 rounded-full`

### 1.8 CTA Section (Final)

**Layout:** Centered call-to-action with gradient background

**Structure:**
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│         Ready to Transform Your Healthcare?                 │
│         Join thousands of satisfied patients today          │
│                                                             │
│              [Start Your Free Journey →]                    │
│                                                             │
│         No credit card required • Set up in 2 minutes       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```


**Details:**

- **Container:**
  - Background: `bg-gradient-to-br from-primary-600 to-primary-800`
  - Padding: `py-20 px-8`
  - Position: Relative with pattern overlay

- **Content:**
  - Max width: `max-w-4xl mx-auto text-center`
  
  **Heading:**
  - Font: `text-4xl lg:text-5xl font-bold`
  - Color: `text-white`
  - Margin: `mb-4`
  
  **Subheading:**
  - Font: `text-xl`
  - Color: `text-primary-100`
  - Margin: `mb-10`
  
  **CTA Button:**
  - Style: `px-10 py-4 bg-white text-primary-700 text-lg font-bold rounded-xl`
  - Shadow: `shadow-2xl`
  - Hover: `hover:bg-gray-50 hover:scale-105`
  - Icon: Arrow right
  
  **Disclaimer:**
  - Font: `text-sm`
  - Color: `text-primary-200`
  - Margin: `mt-6`
  - Icons: Check icons before each point

### 1.9 Footer

**Layout:** Multi-column footer with links and social

**Structure:**
```
┌─────────────────────────────────────────────────────────────┐
│  [Logo]          Product      Company       Resources       │
│  MediNova AI     Features     About Us      Blog            │
│                  Pricing      Careers       Help Center     │
│  Tagline         For Doctors  Contact       FAQs            │
│                                                              │
│  ───────────────────────────────────────────────────────    │
│                                                              │
│  © 2026 MediNova AI             [Social Icons]              │
│  Privacy • Terms • Cookies                                   │
└─────────────────────────────────────────────────────────────┘
```

**Details:**

- **Container:**
  - Background: `bg-gray-900`
  - Padding: `py-12 px-8`
  - Color: `text-gray-300`

- **Top Section:**
  - Layout: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8`
  - Max width: `max-w-7xl mx-auto`

- **Logo Column:**
  - Logo + text in white
  - Tagline: `text-sm text-gray-400 mt-4`

- **Link Columns:**
  - Column title: `text-white font-semibold mb-4`
  - Links: `text-gray-400 hover:text-white text-sm`
  - Spacing: `space-y-3`

- **Bottom Section:**
  - Border: `border-t border-gray-800 mt-12 pt-8`
  - Layout: `flex justify-between items-center`
  - Copyright: `text-sm text-gray-400`
  - Social icons: `flex gap-4`
  - Each icon: `w-10 h-10 rounded-full bg-gray-800 hover:bg-primary-600`

---

## 2. Login Page

### 2.1 Page Overview

**Purpose:** Allow existing users to authenticate and access their accounts

**Layout:** Split screen - left illustration, right form

**Authentication Methods:** Email/Password, Google, Continue as Guest (limited access)

### 2.2 Page Structure

**Layout Type:** 2-column grid (hidden on mobile, form-only on mobile)

**Structure:**
```
┌──────────────────────┬──────────────────────────────────┐
│                      │                                  │
│                      │         Welcome Back             │
│   [Illustration]     │                                  │
│   Medical themed     │   [Email Input]                  │
│   3D graphics with   │   [Password Input]               │
│   healthcare         │   [Remember Me] [Forgot?]        │
│   professionals      │                                  │
│                      │   [Sign In Button]               │
│   "Secure Health"    │                                  │
│   "24/7 Access"      │   ───── or ─────                 │
│                      │                                  │
│                      │   [Google Sign In]               │
│                      │   [Guest Access]                 │
│                      │                                  │
│                      │   Don't have account? Sign Up    │
└──────────────────────┴──────────────────────────────────┘
```

### 2.3 Left Panel (Illustration)

**Display:** `hidden lg:block` (Desktop only)

**Details:**

- **Container:**
  - Width: `lg:w-1/2`
  - Background: `bg-gradient-to-br from-primary-600 via-primary-700 to-primary-800`
  - Position: `relative overflow-hidden`
  - Pattern: Medical icon pattern overlay with `opacity-10`

- **Content:**
  - Padding: `p-12`
  - Display: `flex flex-col justify-center`
  - Height: `min-h-screen`

  **Logo:**
  - Position: Absolute top-left `top-8 left-8`
  - Color: `text-white`
  - Size: `text-xl font-bold`
  - Icon: Medical heart icon

  **Illustration:**
  - 3D isometric medical illustration
  - Elements: Doctor with tablet, patient consultation scene
  - Style: Modern, friendly, professional
  - Animation: Gentle floating animation

  **Heading:**
  - Font: `text-4xl font-bold text-white`
  - Margin: `mt-12 mb-6`
  - Text: "Secure Healthcare Access"

  **Feature List:**
  - Container: `space-y-4`
  - Each item: Check icon + text
  - Icon: `w-6 h-6 text-success-400`
  - Text: `text-white/90 text-lg`
  - Items:
    - "Bank-level encryption"
    - "HIPAA compliant"
    - "24/7 secure access"
    - "Multi-factor authentication"

### 2.4 Right Panel (Login Form)

**Display:** Always visible, centered on mobile

**Details:**

- **Container:**
  - Width: `w-full lg:w-1/2`
  - Background: `bg-white`
  - Display: `flex items-center justify-center`
  - Padding: `px-8 py-12`
  - Min height: `min-h-screen`

- **Form Container:**
  - Max width: `max-w-md w-full`

- **Back to Home Link (Mobile):**
  - Display: `lg:hidden`
  - Position: `absolute top-4 left-4`
  - Icon: ChevronLeft
  - Style: `text-gray-600 hover:text-primary-600`

- **Header Section:**
  
  **Logo (Mobile only):**
  - Display: `lg:hidden mb-8 text-center`
  - Icon + text
  
  **Heading:**
  - Font: `text-3xl lg:text-4xl font-bold font-heading`
  - Color: `text-gray-900`
  - Margin: `mb-2`
  - Text: "Welcome Back"
  
  **Subheading:**
  - Font: `text-base`
  - Color: `text-gray-600`
  - Margin: `mb-8`
  - Text: "Sign in to your MediNova account"

- **Form Fields:**

  **Email Input:**
  - Label: "Email Address"
  - Style: `text-sm font-medium text-gray-700 mb-2 block`
  - Input:
    ```
    w-full px-4 py-3 rounded-xl border-2 border-gray-300
    text-gray-900 placeholder-gray-400 bg-white
    focus:border-primary-500 focus:ring-4 focus:ring-primary-200
    focus:outline-none transition-all duration-200
    ```
  - Placeholder: "your.email@example.com"
  - Icon: Mail icon, `absolute left-4 top-1/2 -translate-y-1/2`
  - Input padding-left: `pl-12` (for icon)
  - Margin: `mb-5`

  **Password Input:**
  - Label: "Password"
  - Style: Same as email
  - Input: Same styling as email
  - Placeholder: "Enter your password"
  - Icon: Lock icon on left
  - Toggle icon: Eye/EyeOff icon on right
  - Toggle style: `absolute right-4 top-1/2 -translate-y-1/2 cursor-pointer text-gray-400 hover:text-gray-600`
  - Margin: `mb-4`

- **Options Row:**
  - Layout: `flex items-center justify-between mb-6`
  
  **Remember Me Checkbox:**
  - Layout: `flex items-center`
  - Checkbox: `w-4 h-4 rounded text-primary-600 focus:ring-primary-200`
  - Label: `ml-2 text-sm text-gray-700`
  
  **Forgot Password Link:**
  - Font: `text-sm font-semibold`
  - Color: `text-primary-600`
  - Hover: `hover:text-primary-700 hover:underline`

- **Sign In Button:**
  - Style:
    ```
    w-full px-6 py-3.5 bg-primary-600 text-white text-base font-semibold
    rounded-xl shadow-lg shadow-primary-500/30
    hover:bg-primary-700 hover:scale-[1.02]
    active:scale-[0.98] transition-all duration-200
    focus:ring-4 focus:ring-primary-200 focus:outline-none
    disabled:opacity-50 disabled:cursor-not-allowed
    ```
  - Text: "Sign In"
  - Icon: Arrow right icon (optional)
  - Margin: `mb-6`
  - Loading state: Spinner icon when processing

- **Divider:**
  - Layout: `relative mb-6`
  - Lines: `border-t border-gray-300`
  - Text: "or continue with"
  - Style: `absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white px-4 text-sm text-gray-500`

- **Social Sign In Buttons:**
  
  **Google Sign In:**
  - Style:
    ```
    w-full px-6 py-3 bg-white border-2 border-gray-300
    text-gray-700 text-base font-semibold rounded-xl
    hover:bg-gray-50 hover:border-gray-400
    transition-all duration-200
    flex items-center justify-center gap-3
    ```
  - Icon: Google logo (colored)
  - Text: "Sign in with Google"
  - Margin: `mb-3`

  **Guest Access Button:**
  - Style: Same as Google but with
  - Background: `bg-gray-50`
  - Border: `border-gray-200`
  - Icon: User icon
  - Text: "Continue as Guest"
  - Subtitle: `text-xs text-gray-500 mt-1` - "Limited features"

- **Sign Up Link:**
  - Margin: `mt-8`
  - Alignment: `text-center`
  - Text: `text-sm text-gray-600`
  - "Don't have an account? "
  - Link: `font-semibold text-primary-600 hover:text-primary-700 hover:underline`
  - Link text: "Sign Up"

### 2.5 Form States

**Default State:**
- All fields empty with placeholders
- Sign In button enabled

**Focused State:**
- Input border changes to primary-500
- Ring appears around focused input
- Label color changes to primary-600

**Error State:**
- Input border: `border-danger-500`
- Error message below input:
  - Icon: AlertCircle, `text-danger-500 w-4 h-4`
  - Text: `text-sm text-danger-600`
  - Example: "Invalid email address"

**Loading State:**
- Sign In button shows spinner
- Button text: "Signing in..."
- Button disabled
- All inputs disabled

**Success State:**
- Brief success message with check icon
- Redirect to dashboard with transition

---

## 3. Register Page

### 3.1 Page Overview

**Purpose:** Allow new users to create accounts

**Layout:** Similar to login page with split screen

**Form Type:** Multi-step or single-page (showing single-page design)

### 3.2 Page Structure

**Layout:** Same 2-column grid as login page

**Structure:**
```
┌──────────────────────┬──────────────────────────────────┐
│                      │                                  │
│   [Illustration]     │      Join MediNova AI            │
│   "Start your        │                                  │
│    health journey"   │   Select Account Type:           │
│                      │   ○ Patient    ○ Doctor          │
│   Benefits list:     │                                  │
│   • Free forever     │   [Full Name Input]              │
│   • No credit card   │   [Email Input]                  │
│   • 2-min setup      │   [Phone Input]                  │
│   • AI powered       │   [Password Input]               │
│                      │   [Confirm Password Input]       │
│                      │                                  │
│                      │   □ I agree to Terms             │
│                      │                                  │
│                      │   [Create Account Button]        │
│                      │                                  │
│                      │   Already have account? Sign In  │
└──────────────────────┴──────────────────────────────────┘
```

### 3.3 Left Panel (Illustration)

**Similar to Login Page but with different messaging:**

- **Background:** Same gradient `bg-gradient-to-br from-primary-600 to-primary-800`

- **Illustration:** 
  - Welcome/onboarding themed
  - Doctor welcoming patient
  - Health journey concept

- **Heading:**
  - Text: "Start Your Health Journey Today"
  - Font: `text-4xl font-bold text-white mb-6`

- **Benefits List:**
  - Container: `space-y-4`
  - Each item:
    - Icon: Check circle, `w-6 h-6 text-success-400`
    - Text: `text-white/90 text-lg`
  - Items:
    - "Free account forever"
    - "No credit card required"
    - "Set up in under 2 minutes"
    - "AI-powered health insights"
    - "Connect with verified doctors"

### 3.4 Right Panel (Registration Form)

**Container:** Same as login page

**Details:**

- **Header:**
  - Heading: "Join MediNova AI"
  - Font: `text-3xl lg:text-4xl font-bold font-heading text-gray-900 mb-2`
  - Subheading: "Create your account to get started"
  - Font: `text-base text-gray-600 mb-6`

- **Account Type Selection:**
  - Label: "I am a"
  - Style: `text-sm font-medium text-gray-700 mb-3 block`
  - Container: `flex gap-4 mb-6`
  
  **Radio Card (Patient):**
  - Style:
    ```
    flex-1 p-4 rounded-xl border-2 border-gray-300
    cursor-pointer transition-all duration-200
    hover:border-primary-300 hover:bg-primary-50
    ```
  - Selected: `border-primary-600 bg-primary-50`
  - Icon: User icon
  - Label: "Patient"
  - Description: `text-xs text-gray-500 mt-1`

  **Radio Card (Doctor):**
  - Same style as Patient
  - Icon: Stethoscope icon
  - Label: "Doctor"
  - Description: "Professional account"

- **Form Fields:**

  **Full Name Input:**
  - Label: "Full Name"
  - Input style: Same as login page
  - Placeholder: "John Doe"
  - Icon: User icon
  - Validation: Required, min 2 characters
  - Error message: "Please enter your full name"
  - Margin: `mb-5`

  **Email Input:**
  - Label: "Email Address"
  - Input style: Same as login
  - Placeholder: "your.email@example.com"
  - Icon: Mail icon
  - Validation: Required, valid email format
  - Error: "Please enter a valid email address"
  - Success indicator: Green check icon when valid
  - Margin: `mb-5`

  **Phone Number Input:**
  - Label: "Phone Number (Optional)"
  - Input style: Same as login
  - Placeholder: "+1 (555) 000-0000"
  - Icon: Phone icon
  - Country code selector: Dropdown on left side
  - Format: Auto-format as user types
  - Margin: `mb-5`

  **Password Input:**
  - Label: "Password"
  - Input style: Same as login
  - Placeholder: "Create a strong password"
  - Icon: Lock icon
  - Toggle: Eye/EyeOff icon
  - Validation rules shown below:
    - Container: `mt-2 space-y-1`
    - Each rule: Check/X icon + text
    - Rules:
      - At least 8 characters
      - Contains uppercase letter
      - Contains lowercase letter
      - Contains number
      - Contains special character
    - Valid rule: `text-success-600` with check icon
    - Invalid rule: `text-gray-400` with X icon
  - Margin: `mb-5`

  **Confirm Password Input:**
  - Label: "Confirm Password"
  - Input style: Same as password
  - Placeholder: "Re-enter your password"
  - Icon: Lock icon
  - Validation: Must match password
  - Error: "Passwords don't match"
  - Success: Green check icon when matches
  - Margin: `mb-5`

- **Terms & Conditions:**
  - Container: `mb-6`
  - Layout: `flex items-start gap-3`
  - Checkbox: `w-5 h-5 rounded text-primary-600 mt-0.5`
  - Label: `text-sm text-gray-700`
  - Text: "I agree to the "
  - Links: `text-primary-600 hover:underline font-semibold`
    - "Terms of Service"
    - "Privacy Policy"
  - Error state: Red border around checkbox + error message below

- **Create Account Button:**
  - Style: Same as Sign In button
  - Text: "Create Account"
  - Icon: Arrow right icon
  - Margin: `mb-6`
  - Loading state: "Creating your account..."

- **Divider:**
  - Same as login page
  - Text: "or sign up with"

- **Social Sign Up:**
  - **Google Sign Up:**
    - Style: Same as login Google button
    - Text: "Sign up with Google"
    - Icon: Google logo
    - Margin: `mb-6`

- **Sign In Link:**
  - Margin: `mt-8 text-center`
  - Text: `text-sm text-gray-600`
  - "Already have an account? "
  - Link: `font-semibold text-primary-600 hover:text-primary-700`
  - Link text: "Sign In"

### 3.5 Form Validation

**Real-time Validation:**
- Validate on blur (when user leaves field)
- Show success checkmark for valid fields
- Show error icon and message for invalid fields
- Password strength meter updates as user types

**Submit Validation:**
- Check all required fields
- Verify password requirements
- Confirm terms acceptance
- Verify email format
- Check password match

**Error Display:**
- Icon: AlertCircle, `text-danger-500`
- Message: Below input, `text-sm text-danger-600`
- Input border: `border-danger-500`
- Shake animation on error

**Success State:**
- Show success message
- Auto-redirect to OTP verification page
- Or redirect to dashboard if no email verification needed

---

## 4. Forgot Password Page

### 4.1 Page Overview

**Purpose:** Help users recover their account by resetting password

**Layout:** Centered single card on clean background

**Process Flow:** 
1. Enter email
2. Receive OTP
3. Redirect to OTP verification

### 4.2 Page Structure

**Layout:** Centered card with minimal distractions

**Structure:**
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                    [Back to Login]                          │
│                                                             │
│                 ┌─────────────────────┐                     │
│                 │                     │                     │
│                 │  [Lock Icon]        │                     │
│                 │                     │                     │
│                 │  Forgot Password?   │                     │
│                 │                     │                     │
│                 │  Enter your email   │                     │
│                 │  and we'll send OTP │                     │
│                 │                     │                     │
│                 │  [Email Input]      │                     │
│                 │                     │                     │
│                 │  [Send OTP Button]  │                     │
│                 │                     │                     │
│                 │  ← Back to Login    │                     │
│                 └─────────────────────┘                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```


### 4.3 Page Details

**Page Container:**
- Background: `bg-gradient-to-br from-gray-50 to-primary-50`
- Min height: `min-h-screen`
- Display: `flex items-center justify-center`
- Padding: `px-4 py-12`

**Back to Login Link (Top):**
- Position: `absolute top-8 left-8`
- Style: `flex items-center gap-2 text-gray-600 hover:text-primary-600 font-medium`
- Icon: ChevronLeft
- Text: "Back to Login"
- Transition: `transition-colors duration-200`

**Card Container:**
- Max width: `max-w-md w-full`
- Background: `bg-white/70 backdrop-blur-xl` (Glass effect)
- Border: `border border-white/30`
- Shadow: `shadow-2xl`
- Rounded: `rounded-2xl`
- Padding: `p-8 lg:p-10`

**Card Content:**

**Icon Container:**
- Size: `w-16 h-16`
- Background: `bg-primary-100`
- Display: `flex items-center justify-center`
- Rounded: `rounded-full`
- Position: `mx-auto mb-6`
- Icon: Lock icon, `w-8 h-8 text-primary-600`

**Heading:**
- Font: `text-3xl font-bold font-heading text-gray-900`
- Alignment: `text-center`
- Margin: `mb-3`
- Text: "Forgot Password?"

**Description:**
- Font: `text-base text-gray-600`
- Alignment: `text-center`
- Max width: `max-w-sm mx-auto`
- Margin: `mb-8`
- Line height: `leading-relaxed`
- Text: "No worries! Enter your email address and we'll send you a verification code to reset your password."

**Email Input:**
- Label: "Email Address"
- Style: `text-sm font-medium text-gray-700 mb-2 block`
- Input:
  ```
  w-full px-4 py-3 pl-12 rounded-xl border-2 border-gray-300
  text-gray-900 placeholder-gray-400 bg-white
  focus:border-primary-500 focus:ring-4 focus:ring-primary-200
  focus:outline-none transition-all duration-200
  ```
- Placeholder: "your.email@example.com"
- Icon: Mail icon, positioned absolutely on left
- Margin: `mb-6`

**Send OTP Button:**
- Style:
  ```
  w-full px-6 py-3.5 bg-primary-600 text-white text-base font-semibold
  rounded-xl shadow-lg shadow-primary-500/30
  hover:bg-primary-700 hover:scale-[1.02]
  active:scale-[0.98] transition-all duration-200
  focus:ring-4 focus:ring-primary-200 focus:outline-none
  disabled:opacity-50 disabled:cursor-not-allowed
  ```
- Text: "Send Verification Code"
- Icon: Send icon (optional)
- Loading state: Spinner + "Sending..."
- Margin: `mb-6`

**Back to Login Link (Bottom):**
- Container: `text-center`
- Style: `flex items-center justify-center gap-2`
- Icon: ChevronLeft, `w-4 h-4`
- Text: `text-sm font-semibold text-primary-600 hover:text-primary-700`
- Link text: "Back to Login"

### 4.4 Success State

**After sending OTP:**

**Success Alert:**
- Background: `bg-success-50`
- Border: `border-l-4 border-success-500`
- Padding: `p-4`
- Rounded: `rounded-lg`
- Margin: `mb-6`
- Icon: CheckCircle, `text-success-600 w-5 h-5`
- Text: `text-success-800 text-sm`
- Message: "Verification code sent! Check your email."

**Auto-redirect:**
- Show countdown: "Redirecting in 3... 2... 1..."
- Or manual redirect button: "Continue to Verification"
- Redirect to OTP Verification page with email pre-filled

### 4.5 Error States

**Email Not Found:**
- Error message below input
- Icon: AlertCircle, `text-danger-500`
- Text: "No account found with this email address"
- Suggestion: Link to "Sign Up" page

**Network Error:**
- Error message above button
- Background: `bg-danger-50 border-l-4 border-danger-500 p-4 rounded-lg`
- Text: "Failed to send verification code. Please try again."
- Retry button enabled

**Rate Limit Error:**
- Message: "Too many attempts. Please try again in 15 minutes."
- Show timer countdown

---

## 5. OTP Verification Page

### 5.1 Page Overview

**Purpose:** Verify user identity using OTP (One-Time Password)

**OTP Type:** 6-digit code sent to email

**Layout:** Centered card with OTP input boxes

**Use Cases:**
- Password reset verification
- Email verification for new accounts
- Two-factor authentication

### 5.2 Page Structure

**Layout:** Centered card with OTP input

**Structure:**
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                 ┌─────────────────────┐                     │
│                 │                     │                     │
│                 │  [Email Icon]       │                     │
│                 │                     │                     │
│                 │  Verify Your Email  │                     │
│                 │                     │                     │
│                 │  We sent a code to  │                     │
│                 │  user@example.com   │                     │
│                 │                     │                     │
│                 │  [□][□][□][□][□][□] │  (6 boxes)         │
│                 │                     │                     │
│                 │  ⏱ 02:45 remaining  │                     │
│                 │                     │                     │
│                 │  [Verify Button]    │                     │
│                 │                     │                     │
│                 │  Didn't receive?    │                     │
│                 │  [Resend Code]      │                     │
│                 │                     │                     │
│                 │  ← Back             │                     │
│                 └─────────────────────┘                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```


### 5.3 Page Details

**Page Container:**
- Background: `bg-gradient-to-br from-gray-50 to-primary-50`
- Min height: `min-h-screen`
- Display: `flex items-center justify-center`
- Padding: `px-4 py-12`

**Card Container:**
- Max width: `max-w-md w-full`
- Background: `bg-white/70 backdrop-blur-xl`
- Border: `border border-white/30`
- Shadow: `shadow-2xl`
- Rounded: `rounded-2xl`
- Padding: `p-8 lg:p-10`

**Card Content:**

**Icon Container:**
- Size: `w-16 h-16`
- Background: `bg-primary-100`
- Display: `flex items-center justify-center`
- Rounded: `rounded-full`
- Position: `mx-auto mb-6`
- Icon: Mail or Shield icon, `w-8 h-8 text-primary-600`

**Heading:**
- Font: `text-3xl font-bold font-heading text-gray-900`
- Alignment: `text-center`
- Margin: `mb-3`
- Text: "Verify Your Email"

**Description:**
- Font: `text-base text-gray-600`
- Alignment: `text-center`
- Margin: `mb-2`
- Text: "We sent a 6-digit verification code to"

**Email Display:**
- Font: `text-base font-semibold text-gray-900`
- Alignment: `text-center`
- Margin: `mb-8`
- Text: User's email (e.g., "user@example.com")
- Edit icon: Small pencil icon to change email
- Edit link: `text-sm text-primary-600 hover:underline`

**OTP Input Container:**
- Layout: `flex gap-3 justify-center`
- Margin: `mb-6`

**Individual OTP Box:**
- Size: `w-12 h-14 md:w-14 md:h-16`
- Style:
  ```
  text-center text-2xl font-bold text-gray-900
  border-2 border-gray-300 rounded-xl
  focus:border-primary-500 focus:ring-4 focus:ring-primary-200
  focus:outline-none transition-all duration-200
  ```
- Type: `text` with `maxLength={1}`
- Auto-focus: First box on load
- Auto-tab: Move to next box on input
- Auto-backspace: Move to previous box on delete
- Paste support: Paste all 6 digits at once

**OTP Box States:**

- **Empty:**
  - Border: `border-gray-300`
  - Background: `bg-white`

- **Filled:**
  - Border: `border-primary-500`
  - Background: `bg-primary-50`
  - Text: Bold, centered

- **Focused:**
  - Border: `border-primary-500`
  - Ring: `ring-4 ring-primary-200`
  - Scale: `scale-105`

- **Error:**
  - Border: `border-danger-500`
  - Background: `bg-danger-50`
  - Shake animation

**Timer:**
- Container: `flex items-center justify-center gap-2 mb-6`
- Icon: Clock icon, `w-5 h-5 text-gray-500`
- Text: `text-sm text-gray-600`
- Format: "02:45 remaining"
- Color changes:
  - Green (>1 min): `text-success-600`
  - Orange (<1 min): `text-warning-600`
  - Red (<30s): `text-danger-600`

**Verify Button:**
- Style:
  ```
  w-full px-6 py-3.5 bg-primary-600 text-white text-base font-semibold
  rounded-xl shadow-lg shadow-primary-500/30
  hover:bg-primary-700 hover:scale-[1.02]
  active:scale-[0.98] transition-all duration-200
  focus:ring-4 focus:ring-primary-200 focus:outline-none
  disabled:opacity-50 disabled:cursor-not-allowed
  ```
- Text: "Verify Code"
- Disabled: Until all 6 digits entered
- Loading state: Spinner + "Verifying..."
- Margin: `mb-6`

**Resend Section:**
- Container: `text-center mb-6`
- Text: `text-sm text-gray-600`
- "Didn't receive the code? "
- Button/Link: `font-semibold text-primary-600 hover:text-primary-700`
- Link text: "Resend Code"
- Disabled: While timer active
- Enabled: After timer expires or on click
- Cooldown: 60 seconds between resends
- Success message: "Code resent! Check your email."

**Back Button:**
- Container: `text-center`
- Style: `flex items-center justify-center gap-2`
- Icon: ChevronLeft, `w-4 h-4`
- Text: `text-sm font-semibold text-gray-600 hover:text-primary-600`
- Link text: "Back"
- Action: Return to previous page (Forgot Password)

### 5.4 OTP Input Behavior

**Auto-focus Logic:**
1. First box focused on page load
2. On input: Auto-move to next box
3. On backspace in empty box: Move to previous box
4. On paste: Fill all boxes with pasted digits

**Paste Handling:**
- Detect paste event
- Extract digits from pasted text
- Fill boxes left to right
- Auto-submit if all 6 digits pasted

**Keyboard Navigation:**
- Arrow keys: Move between boxes
- Tab: Move forward
- Shift+Tab: Move backward
- Backspace: Clear current + move back
- Number keys: Enter digit

### 5.5 Success State

**On successful verification:**

**Success Animation:**
- All boxes turn green: `border-success-500 bg-success-50`
- Check icon appears in each box
- Success message appears

**Success Alert:**
- Background: `bg-success-50 border-l-4 border-success-500`
- Padding: `p-4 rounded-lg`
- Icon: CheckCircle, `text-success-600`
- Text: "Email verified successfully!"
- Margin: `mb-6`

**Auto-redirect:**
- Show message: "Redirecting..."
- Redirect to Reset Password page (for password reset flow)
- Or redirect to Dashboard (for email verification flow)
- Delay: 2 seconds


### 5.6 Error States

**Invalid OTP:**
- All boxes shake animation
- Border: `border-danger-500`
- Background: `bg-danger-50`
- Error message below OTP:
  - Icon: AlertCircle, `text-danger-500`
  - Text: `text-sm text-danger-600`
  - Message: "Invalid verification code. Please try again."
- Clear all boxes after animation
- Focus first box

**Expired OTP:**
- Error alert:
  - Background: `bg-warning-50 border-l-4 border-warning-500`
  - Icon: AlertTriangle
  - Text: "This code has expired. Please request a new one."
- Disable verify button
- Enable resend button
- Timer shows "00:00"

**Max Attempts Reached:**
- Lock icon replaces email icon
- Error message: "Too many failed attempts. Please try again in 15 minutes."
- Disable all inputs
- Show countdown timer
- Disable resend button

**Network Error:**
- Error message: "Connection error. Please check your internet and try again."
- Retry button enabled

---

## 6. Reset Password Page

### 6.1 Page Overview

**Purpose:** Allow users to create a new password after OTP verification

**Layout:** Centered card with password inputs

**Security:** 
- Strong password requirements enforced
- Password strength indicator
- Confirm password matching

### 6.2 Page Structure

**Layout:** Centered card with password form

**Structure:**
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                 ┌─────────────────────┐                     │
│                 │                     │                     │
│                 │  [Key Icon]         │                     │
│                 │                     │                     │
│                 │  Reset Password     │                     │
│                 │                     │                     │
│                 │  Create a strong    │                     │
│                 │  new password       │                     │
│                 │                     │                     │
│                 │  [New Password]     │                     │
│                 │  ▓▓▓▓▓▓▓▓ (Strength)│                     │
│                 │  ✓ Requirements     │                     │
│                 │                     │                     │
│                 │  [Confirm Password] │                     │
│                 │                     │                     │
│                 │  [Reset Button]     │                     │
│                 │                     │                     │
│                 └─────────────────────┘                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6.3 Page Details

**Page Container:**
- Background: `bg-gradient-to-br from-gray-50 to-primary-50`
- Min height: `min-h-screen`
- Display: `flex items-center justify-center`
- Padding: `px-4 py-12`

**Card Container:**
- Max width: `max-w-md w-full`
- Background: `bg-white/70 backdrop-blur-xl`
- Border: `border border-white/30`
- Shadow: `shadow-2xl`
- Rounded: `rounded-2xl`
- Padding: `p-8 lg:p-10`

**Card Content:**

**Icon Container:**
- Size: `w-16 h-16`
- Background: `bg-primary-100`
- Display: `flex items-center justify-center`
- Rounded: `rounded-full`
- Position: `mx-auto mb-6`
- Icon: Key icon, `w-8 h-8 text-primary-600`

**Heading:**
- Font: `text-3xl font-bold font-heading text-gray-900`
- Alignment: `text-center`
- Margin: `mb-3`
- Text: "Reset Password"

**Description:**
- Font: `text-base text-gray-600`
- Alignment: `text-center`
- Max width: `max-w-sm mx-auto`
- Margin: `mb-8`
- Line height: `leading-relaxed`
- Text: "Create a strong new password for your account. Make sure it's different from previous passwords."

**New Password Input:**
- Label: "New Password"
- Style: `text-sm font-medium text-gray-700 mb-2 block`
- Input:
  ```
  w-full px-4 py-3 pl-12 pr-12 rounded-xl border-2 border-gray-300
  text-gray-900 placeholder-gray-400 bg-white
  focus:border-primary-500 focus:ring-4 focus:ring-primary-200
  focus:outline-none transition-all duration-200
  ```
- Placeholder: "Enter new password"
- Left icon: Lock icon
- Right icon: Eye/EyeOff toggle for visibility
- Type: `password` (toggleable to `text`)
- Margin: `mb-3`

**Password Strength Meter:**
- Container: `mb-3`
- Progress bar container:
  ```
  w-full h-2 bg-gray-200 rounded-full overflow-hidden
  ```
- Progress bar fill:
  ```
  h-full transition-all duration-300 rounded-full
  ```
- Colors based on strength:
  - Weak (0-30%): `bg-danger-500 w-[30%]`
  - Fair (31-60%): `bg-warning-500 w-[60%]`
  - Good (61-80%): `bg-primary-500 w-[80%]`
  - Strong (81-100%): `bg-success-500 w-full`
- Label below:
  - Font: `text-xs font-semibold`
  - Color: Matches strength color
  - Text: "Weak" | "Fair" | "Good" | "Strong"

**Password Requirements:**
- Container: `mb-6 space-y-2`
- Each requirement:
  - Layout: `flex items-center gap-2`
  - Icon: Check (valid) or X (invalid)
  - Valid: `text-success-600`
  - Invalid: `text-gray-400`
  - Font: `text-xs text-gray-600`

**Requirements List:**
1. "At least 8 characters"
2. "Contains uppercase letter (A-Z)"
3. "Contains lowercase letter (a-z)"
4. "Contains number (0-9)"
5. "Contains special character (@$!%*?&)"

**Confirm Password Input:**
- Label: "Confirm New Password"
- Style: Same as new password input
- Placeholder: "Re-enter new password"
- Left icon: Lock icon
- Right icon: Eye/EyeOff toggle
- Validation: Real-time matching check
- Margin: `mb-6`

**Match Indicator:**
- Shows when user starts typing in confirm field
- Valid match:
  - Icon: Check, `text-success-600`
  - Text: "Passwords match"
  - Color: `text-success-600`
- Invalid match:
  - Icon: X, `text-danger-600`
  - Text: "Passwords don't match"
  - Color: `text-danger-600`
- Display: Below confirm password input
- Font: `text-sm font-medium`


**Reset Password Button:**
- Style:
  ```
  w-full px-6 py-3.5 bg-primary-600 text-white text-base font-semibold
  rounded-xl shadow-lg shadow-primary-500/30
  hover:bg-primary-700 hover:scale-[1.02]
  active:scale-[0.98] transition-all duration-200
  focus:ring-4 focus:ring-primary-200 focus:outline-none
  disabled:opacity-50 disabled:cursor-not-allowed
  ```
- Text: "Reset Password"
- Icon: Key or CheckCircle icon
- Disabled conditions:
  - Password doesn't meet requirements
  - Passwords don't match
  - Form is submitting
- Loading state: Spinner + "Resetting password..."
- Margin: `mb-6`

**Security Note:**
- Container: `bg-primary-50 border-l-4 border-primary-500 p-4 rounded-lg`
- Icon: Info icon, `text-primary-600 w-5 h-5`
- Text: `text-sm text-primary-800`
- Message: "For your security, you'll be logged out of all devices after resetting your password."

### 6.4 Password Strength Calculator

**Strength Scoring:**

**Weak (0-30 points):**
- Less than 8 characters
- Only lowercase or only numbers
- No special characters

**Fair (31-60 points):**
- 8+ characters
- Mix of lowercase + numbers
- One requirement missing

**Good (61-80 points):**
- 8+ characters
- Mix of upper, lower, numbers
- Missing special character or length < 12

**Strong (81-100 points):**
- 12+ characters
- All requirements met
- Mix of all character types
- Bonus: Common patterns avoided

**Bonus Points:**
- +10 for length > 12 characters
- +10 for length > 16 characters
- +5 for multiple special characters
- -20 for common patterns (123456, password, qwerty)

### 6.5 Form Validation

**Real-time Validation:**
- Check password requirements as user types
- Update strength meter live
- Highlight valid requirements in green
- Show match indicator for confirm password

**Submit Validation:**
- All requirements must be met
- Passwords must match exactly
- Password must not be in common password list
- Password must be different from old password (API check)

**Client-side Checks:**
- Minimum length
- Character type requirements
- Match validation
- Common password detection

**Server-side Checks:**
- Password history check
- Breached password database check
- Account-specific restrictions

### 6.6 Success State

**On successful password reset:**

**Success Modal/Alert:**
- Overlay: `fixed inset-0 bg-black/50 backdrop-blur-sm`
- Modal: Center of screen
- Background: `bg-white rounded-2xl shadow-2xl p-8`
- Animation: Scale in from center

**Modal Content:**

**Success Icon:**
- Size: `w-20 h-20`
- Background: `bg-success-100`
- Rounded: `rounded-full`
- Position: `mx-auto mb-6`
- Icon: CheckCircle, `w-12 h-12 text-success-600`
- Animation: Check mark draw animation

**Success Heading:**
- Font: `text-2xl font-bold font-heading text-gray-900`
- Alignment: `text-center`
- Margin: `mb-3`
- Text: "Password Reset Successful!"

**Success Message:**
- Font: `text-base text-gray-600`
- Alignment: `text-center`
- Margin: `mb-8`
- Text: "Your password has been reset successfully. You can now sign in with your new password."

**Continue Button:**
- Style:
  ```
  w-full px-8 py-3.5 bg-primary-600 text-white text-base font-semibold
  rounded-xl shadow-lg shadow-primary-500/30
  hover:bg-primary-700
  ```
- Text: "Continue to Login"
- Action: Redirect to login page
- Margin: `mb-4`

**Auto-redirect:**
- Show countdown: "Redirecting to login in 5... 4... 3..."
- Or manual button click
- Clear any tokens/session data
- Redirect to login page

### 6.7 Error States

**Password Too Weak:**
- Error below password input
- Icon: AlertCircle, `text-danger-500`
- Text: `text-sm text-danger-600`
- Message: "Password is too weak. Please choose a stronger password."
- Button disabled

**Passwords Don't Match:**
- Error below confirm password
- Red border on confirm password input
- Message: "Passwords don't match"
- Button disabled

**Common Password Detected:**
- Warning alert:
  - Background: `bg-warning-50 border-l-4 border-warning-500 p-4 rounded-lg`
  - Icon: AlertTriangle
  - Text: "This password is commonly used and may be compromised. Please choose a different one."
- Button disabled

**Same as Old Password:**
- Error from API
- Message: "New password must be different from your current password."
- Clear both fields
- Focus new password input

**Network Error:**
- Error alert above button
- Background: `bg-danger-50 border-l-4 border-danger-500 p-4 rounded-lg`
- Message: "Failed to reset password. Please try again."
- Retry button enabled

**Session Expired:**
- Modal alert
- Message: "Your session has expired. Please start the password reset process again."
- Button: "Back to Forgot Password"
- Redirect to Forgot Password page

---

## 7. Additional UI Elements

### 7.1 Loading States

**Full Page Loader:**
- Overlay: `fixed inset-0 bg-white/80 backdrop-blur-sm z-50`
- Spinner: Center of screen
- Logo: Animated logo pulse
- Text: "Loading..." below spinner

**Button Loader:**
- Spinner icon: `animate-spin w-5 h-5`
- Text changes: "Processing..."
- Button disabled during loading

**Skeleton Loader:**
- Used for content loading
- Animated pulse effect
- Matches content dimensions

### 7.2 Toast Notifications

**Position:** Top-right corner, fixed

**Success Toast:**
- Background: `bg-white border-l-4 border-success-500 shadow-xl`
- Icon: CheckCircle, `text-success-600`
- Auto-dismiss: 5 seconds
- Animation: Slide in from right

**Error Toast:**
- Background: `bg-white border-l-4 border-danger-500 shadow-xl`
- Icon: AlertCircle, `text-danger-600`
- Manual dismiss or 7 seconds auto-dismiss

**Warning Toast:**
- Background: `bg-white border-l-4 border-warning-500 shadow-xl`
- Icon: AlertTriangle, `text-warning-600`

**Info Toast:**
- Background: `bg-white border-l-4 border-info-500 shadow-xl`
- Icon: Info, `text-info-600`

### 7.3 Modal Overlays

**Structure:**
- Overlay: `fixed inset-0 bg-black/50 backdrop-blur-sm z-50`
- Modal: `bg-white rounded-2xl shadow-2xl max-w-md w-full`
- Position: Center of screen
- Animation: Scale + fade in
- Close: X button top-right or click overlay

### 7.4 Progress Indicators

**Multi-step Progress:**
- Dots or numbers
- Current step highlighted
- Completed steps in success color
- Future steps in gray

---

## 8. Responsive Behavior

### 8.1 Mobile Optimizations

**All Pages:**
- Remove left illustration panel (< 1024px)
- Full-width form on mobile
- Larger touch targets (min 44x44px)
- Simplified navigation
- Stack elements vertically

**Hero Section:**
- Text center-aligned on mobile
- Illustration below text or hidden
- Larger font sizes scale down
- Buttons stack vertically

**Forms:**
- Full-width inputs
- Larger padding for touch
- Error messages below inputs
- Fixed submit buttons at bottom

**OTP Input:**
- Slightly smaller boxes on mobile
- 3-gap spacing instead of 4
- Responsive box sizing

### 8.2 Tablet Adjustments

**Grid Layouts:**
- 2-column feature grids
- Maintain split-screen auth pages
- Adjust illustration sizes

### 8.3 Desktop Enhancements

**Max Widths:**
- Constrain content width
- Center align content
- Add more whitespace
- Show all illustrations

---

## Summary

**Completed Page Designs:**
1. ✅ Landing Page - Complete with 8 sections
2. ✅ Login Page - Split screen with social auth
3. ✅ Register Page - Multi-field form with validation
4. ✅ Forgot Password - Clean, focused single task
5. ✅ OTP Verification - 6-digit input with timer
6. ✅ Reset Password - Strength meter and requirements

**Design Characteristics:**
- Healthcare-themed with medical blue primary color
- Glassmorphism effects throughout
- Consistent spacing and typography
- Full accessibility compliance
- Responsive design for all devices
- Real-time validation and feedback
- Clear error states and success messages
- Smooth animations and transitions

**Ready for Implementation** ✅

---

**End of Page Designs Document**
