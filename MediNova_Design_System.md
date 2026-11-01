# MediNova AI: Design System
## Healthcare-Themed UI/UX with Glassmorphism

---

**Project:** MediNova AI - Multi-Agent Healthcare Intelligence Platform  
**Design Philosophy:** Modern Healthcare Aesthetics with Glassmorphism  
**Framework:** Tailwind CSS  
**Date:** July 2, 2026  

---

## Table of Contents

1. [Design Philosophy](#1-design-philosophy)
2. [Color Palette](#2-color-palette)
3. [Typography](#3-typography)
4. [Spacing System](#4-spacing-system)
5. [Icons](#5-icons)
6. [Buttons](#6-buttons)
7. [Cards](#7-cards)
8. [Forms](#8-forms)
9. [Tables](#9-tables)
10. [Navigation](#10-navigation)
11. [Sidebar](#11-sidebar)
12. [Dark Mode](#12-dark-mode)
13. [Light Mode](#13-light-mode)

---

## 1. Design Philosophy

### 1.1 Core Principles

**Trust & Professionalism**
- Clean, minimalist interfaces
- Medical-grade precision in design
- Calming color psychology

**Accessibility First**
- WCAG 2.1 AA compliance
- High contrast ratios
- Clear visual hierarchy

**Glassmorphism Aesthetics**
- Frosted glass effects
- Subtle transparency
- Soft shadows and blurs
- Layered depth perception

**Healthcare Theme**
- Medical blues and greens
- Sterile whites
- Warm accent colors for comfort
- Nature-inspired secondary colors

### 1.2 Design Goals

- **Reduce Anxiety**: Calming colors and smooth interactions
- **Build Trust**: Professional, medical-grade appearance
- **Enhance Clarity**: Clear information hierarchy
- **Ensure Accessibility**: Readable for all users
- **Modern Appeal**: Contemporary glassmorphism aesthetics

---

## 2. Color Palette

### 2.1 Primary Colors (Medical Blue)

**Primary Blue** - Trust, Medical, Professional
```
primary-50:  #EBF5FF  (Lightest - backgrounds)
primary-100: #D1E9FF  (Very light)
primary-200: #B2DBFF  (Light)
primary-300: #84C5FF  (Medium light)
primary-400: #53A8FF  (Medium)
primary-500: #2E90FA  (Base - main brand)
primary-600: #1570EF  (Dark)
primary-700: #175CD3  (Darker)
primary-800: #1849A9  (Very dark)
primary-900: #194185  (Darkest)
```

**Usage:**
- primary-500: Main CTAs, links, active states
- primary-600: Hover states on primary buttons
- primary-100: Subtle backgrounds, highlights
- primary-50: Very subtle backgrounds

### 2.2 Secondary Colors (Medical Green)

**Success Green** - Health, Wellness, Success
```
success-50:  #ECFDF3  (Lightest)
success-100: #D1FADF  (Very light)
success-200: #A6F4C5  (Light)
success-300: #6CE9A6  (Medium light)
success-400: #32D583  (Medium)
success-500: #12B76A  (Base - success messages)
success-600: #039855  (Dark)
success-700: #027A48  (Darker)
success-800: #05603A  (Very dark)
success-900: #054F31  (Darkest)
```

**Usage:**
- success-500: Success states, completed actions
- success-100: Success message backgrounds
- success-600: Positive health indicators

### 2.3 Accent Colors

**Warm Coral** - Comfort, Care, Compassion
```
accent-50:  #FFF4ED  (Lightest)
accent-100: #FFE6D5  (Very light)
accent-200: #FFD6AE  (Light)
accent-300: #FFBC8B  (Medium light)
accent-400: #FF9C66  (Medium)
accent-500: #FF7A47  (Base - warm accents)
accent-600: #FF5A1F  (Dark)
accent-700: #E04F1A  (Darker)
accent-800: #C1410F  (Very dark)
accent-900: #A23A0F  (Darkest)
```

**Usage:**
- accent-500: Warm CTAs, highlights
- accent-100: Attention backgrounds (non-critical)


### 2.4 Semantic Colors

**Warning Yellow**
```
warning-50:  #FFFAEB  
warning-100: #FEF0C7  
warning-200: #FEDF89  
warning-300: #FEC84B  
warning-400: #FDB022  
warning-500: #F79009  (Base - warnings)
warning-600: #DC6803  
warning-700: #B54708  
warning-800: #93370D  
warning-900: #7A2E0E  
```

**Danger Red**
```
danger-50:  #FEF3F2  
danger-100: #FEE4E2  
danger-200: #FECDCA  
danger-300: #FDA29B  
danger-400: #F97066  
danger-500: #F04438  (Base - errors, critical)
danger-600: #D92D20  
danger-700: #B42318  
danger-800: #912018  
danger-900: #7A271A  
```

**Info Purple**
```
info-50:  #F4F3FF  
info-100: #EBE9FE  
info-200: #D9D6FE  
info-300: #BDB4FE  
info-400: #9B8AFB  
info-500: #7A5AF8  (Base - information)
info-600: #6938EF  
info-700: #5925DC  
info-800: #4A1FB8  
info-900: #3E1C96  
```

### 2.5 Neutral Colors (Grays)

**Gray Scale** - Text, Borders, Backgrounds
```
gray-50:  #F9FAFB  (Lightest backgrounds)
gray-100: #F3F4F6  (Light backgrounds)
gray-200: #E5E7EB  (Subtle borders)
gray-300: #D1D5DB  (Borders)
gray-400: #9CA3AF  (Disabled text)
gray-500: #6B7280  (Secondary text)
gray-600: #4B5563  (Body text)
gray-700: #374151  (Headings)
gray-800: #1F2937  (Dark headings)
gray-900: #111827  (Darkest text)
```

**Usage:**
- gray-900: Primary headings (light mode)
- gray-700: Subheadings
- gray-600: Body text
- gray-500: Secondary text, labels
- gray-300: Borders, dividers
- gray-100: Subtle backgrounds
- gray-50: Page backgrounds

### 2.6 Glassmorphism Colors

**Glass Overlays** - Frosted Glass Effects
```
glass-light:   rgba(255, 255, 255, 0.7)  
glass-medium:  rgba(255, 255, 255, 0.5)  
glass-subtle:  rgba(255, 255, 255, 0.3)  

glass-dark:    rgba(17, 24, 39, 0.7)    
glass-dark-md: rgba(17, 24, 39, 0.5)    
glass-dark-st: rgba(17, 24, 39, 0.3)    
```

**Usage with Tailwind:**
- `bg-white/70 backdrop-blur-xl` - Light glass
- `bg-white/50 backdrop-blur-lg` - Medium glass
- `bg-white/30 backdrop-blur-md` - Subtle glass

### 2.7 Gradient Colors

**Medical Gradients**
```
gradient-primary:   linear-gradient(135deg, #2E90FA 0%, #1570EF 100%)
gradient-success:   linear-gradient(135deg, #12B76A 0%, #027A48 100%)
gradient-warm:      linear-gradient(135deg, #FF7A47 0%, #FF5A1F 100%)
gradient-cool:      linear-gradient(135deg, #7A5AF8 0%, #5925DC 100%)
gradient-health:    linear-gradient(135deg, #2E90FA 0%, #12B76A 100%)
gradient-sunset:    linear-gradient(135deg, #FF7A47 0%, #F79009 100%)
```

**Tailwind Classes:**
- `bg-gradient-to-br from-primary-500 to-primary-700`
- `bg-gradient-to-r from-success-500 to-success-700`
- `bg-gradient-to-br from-primary-500 to-success-500` (health gradient)

---

## 3. Typography

### 3.1 Font Families

**Primary Font: Inter**
- Modern, highly readable
- Excellent for digital interfaces
- Wide range of weights
- Great for medical/professional context

**Secondary Font: Manrope** (Headings)
- Geometric, professional
- Strong visual hierarchy
- Medical-grade precision feel

**Monospace: JetBrains Mono** (Code, Data)
- Medical data, measurements
- Technical information
- Code snippets

**Tailwind Config:**
```
fontFamily: {
  sans: ['Inter', 'system-ui', 'sans-serif'],
  heading: ['Manrope', 'Inter', 'sans-serif'],
  mono: ['JetBrains Mono', 'monospace']
}
```

### 3.2 Font Sizes

**Scale: Type Scale with 1.25 ratio (Major Third)**

```
text-xs:    0.75rem   (12px)  - Captions, small labels
text-sm:    0.875rem  (14px)  - Secondary text, table content
text-base:  1rem      (16px)  - Body text, paragraphs
text-lg:    1.125rem  (18px)  - Large body, emphasized text
text-xl:    1.25rem   (20px)  - H5 headings, card titles
text-2xl:   1.5rem    (24px)  - H4 headings
text-3xl:   1.875rem  (30px)  - H3 headings
text-4xl:   2.25rem   (36px)  - H2 headings
text-5xl:   3rem      (48px)  - H1 headings, hero titles
text-6xl:   3.75rem   (60px)  - Display, hero text
text-7xl:   4.5rem    (72px)  - Extra large display
```

### 3.3 Font Weights

```
font-light:     300  - Subtle text, decorative
font-normal:    400  - Body text
font-medium:    500  - Emphasis, labels
font-semibold:  600  - Subheadings, important text
font-bold:      700  - Headings, strong emphasis
font-extrabold: 800  - Display headings
```

**Usage Guidelines:**
- Body text: font-normal (400)
- Labels: font-medium (500)
- Buttons: font-semibold (600)
- Headings: font-bold (700)
- Display: font-extrabold (800)

### 3.4 Line Heights

```
leading-none:    1      - Tight, display headings
leading-tight:   1.25   - Headings
leading-snug:    1.375  - Subheadings
leading-normal:  1.5    - Body text (default)
leading-relaxed: 1.625  - Comfortable reading
leading-loose:   2      - Very spacious
```

### 3.5 Letter Spacing

```
tracking-tighter:  -0.05em  - Very tight
tracking-tight:    -0.025em - Tight
tracking-normal:   0em      - Default
tracking-wide:     0.025em  - Slightly wide
tracking-wider:    0.05em   - Wide (labels, buttons)
tracking-widest:   0.1em    - Very wide (all-caps headings)
```

**Usage:**
- Headings: tracking-tight
- Body: tracking-normal
- Buttons/Labels: tracking-wide
- All-caps text: tracking-widest

### 3.6 Typography Hierarchy

**Display Text (Hero Sections)**
- Font: Manrope
- Size: text-5xl to text-7xl
- Weight: font-extrabold
- Line Height: leading-tight
- Color: gray-900 (light mode), white (dark mode)

**H1 - Page Titles**
- Font: Manrope
- Size: text-4xl
- Weight: font-bold
- Line Height: leading-tight
- Color: gray-900

**H2 - Section Headings**
- Font: Manrope
- Size: text-3xl
- Weight: font-bold
- Line Height: leading-snug
- Color: gray-800

**H3 - Subsection Headings**
- Font: Manrope
- Size: text-2xl
- Weight: font-semibold
- Line Height: leading-snug
- Color: gray-700

**H4 - Card Titles**
- Font: Inter
- Size: text-xl
- Weight: font-semibold
- Line Height: leading-normal
- Color: gray-700


**Body Text - Large**
- Font: Inter
- Size: text-lg
- Weight: font-normal
- Line Height: leading-relaxed
- Color: gray-600

**Body Text - Regular**
- Font: Inter
- Size: text-base
- Weight: font-normal
- Line Height: leading-normal
- Color: gray-600

**Body Text - Small**
- Font: Inter
- Size: text-sm
- Weight: font-normal
- Line Height: leading-normal
- Color: gray-500

**Caption / Helper Text**
- Font: Inter
- Size: text-xs
- Weight: font-normal
- Line Height: leading-normal
- Color: gray-500

**Labels**
- Font: Inter
- Size: text-sm
- Weight: font-medium
- Line Height: leading-normal
- Color: gray-700

---

## 4. Spacing System

### 4.1 Spacing Scale (8px Base Unit)

**Tailwind Spacing:**
```
0:    0px      - No spacing
px:   1px      - Hairline borders
0.5:  2px      (0.125rem)
1:    4px      (0.25rem)
1.5:  6px      (0.375rem)
2:    8px      (0.5rem)   ← Base unit
2.5:  10px     (0.625rem)
3:    12px     (0.75rem)
3.5:  14px     (0.875rem)
4:    16px     (1rem)
5:    20px     (1.25rem)
6:    24px     (1.5rem)
7:    28px     (1.75rem)
8:    32px     (2rem)
10:   40px     (2.5rem)
12:   48px     (3rem)
14:   56px     (3.5rem)
16:   64px     (4rem)
20:   80px     (5rem)
24:   96px     (6rem)
32:   128px    (8rem)
40:   160px    (10rem)
48:   192px    (12rem)
56:   224px    (14rem)
64:   256px    (16rem)
```

### 4.2 Component Spacing Guidelines

**Padding Inside Components:**
- Extra small: `p-2` (8px)
- Small: `p-3` (12px) or `p-4` (16px)
- Medium: `p-6` (24px) - Cards, modals
- Large: `p-8` (32px) - Sections
- Extra large: `p-12` (48px) - Hero sections

**Margin Between Components:**
- Tight: `mb-2` or `mb-4` (8-16px)
- Normal: `mb-6` (24px)
- Relaxed: `mb-8` (32px)
- Spacious: `mb-12` (48px)
- Section gaps: `mb-16` or `mb-20` (64-80px)

**Container Padding:**
- Mobile: `px-4` (16px)
- Tablet: `px-6` (24px)
- Desktop: `px-8` (32px)
- Max width container: `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`

### 4.3 Grid & Layout Spacing

**Gap Between Grid Items:**
- Tight: `gap-2` or `gap-3` (8-12px)
- Normal: `gap-4` or `gap-6` (16-24px)
- Relaxed: `gap-8` (32px)

**Section Spacing:**
- Between sections: `py-12` to `py-20` (48-80px)
- Page top/bottom: `py-16` (64px)


---

## 5. Icons

### 5.1 Icon Library

**Primary: Lucide React**
- Modern, consistent design
- Healthcare-friendly icons
- Tree-shakeable, lightweight
- Perfect for medical UI

**Icon Categories Needed:**

**Medical Icons:**
- Heart, HeartPulse (vital signs)
- Activity (health monitoring)
- Pill, Syringe (medication)
- Stethoscope, Hospital (medical)
- Thermometer (temperature)
- Brain (mental health)
- Eye, Ear (body parts)

**Interface Icons:**
- User, Users (profiles)
- Calendar, Clock (appointments)
- FileText, ClipboardList (records)
- MessageCircle, Video (communication)
- Bell (notifications)
- Settings, Menu (navigation)
- Search, Filter (actions)
- ChevronRight, ChevronDown (arrows)
- Check, X (status)
- AlertCircle, AlertTriangle (alerts)
- Info, HelpCircle (information)

### 5.2 Icon Sizes

```
Icon Size Guidelines:
icon-xs:   12px  (w-3 h-3)   - Inline text icons
icon-sm:   16px  (w-4 h-4)   - Button icons, small UI
icon-base: 20px  (w-5 h-5)   - Default, navigation
icon-md:   24px  (w-6 h-6)   - Cards, prominent icons
icon-lg:   32px  (w-8 h-8)   - Feature icons
icon-xl:   48px  (w-12 h-12) - Hero icons
icon-2xl:  64px  (w-16 h-16) - Large feature icons
```

### 5.3 Icon Colors & States

**Default State:**
- Primary icons: `text-gray-600`
- Secondary icons: `text-gray-500`
- Subtle icons: `text-gray-400`

**Active/Hover State:**
- Primary: `text-primary-600 hover:text-primary-700`
- Success: `text-success-600`
- Warning: `text-warning-600`
- Danger: `text-danger-600`

**Icon in Buttons:**
- Same color as button text
- Size: icon-sm (16px) for small buttons
- Size: icon-base (20px) for regular buttons
- Spacing: `mr-2` (8px gap between icon and text)

**Icon Backgrounds (Avatar Style):**
- Light: `bg-primary-100 text-primary-600`
- Medium: `bg-primary-500 text-white`
- Glass: `bg-white/20 backdrop-blur text-white`

### 5.4 Icon Usage Guidelines

**Inline with Text:**
- Vertical align: `inline-flex items-center`
- Icon first: `<Icon className="w-4 h-4 mr-2" /> Text`
- Icon last: `Text <Icon className="w-4 h-4 ml-2" />`

**Standalone Icons (Buttons):**
- Add padding: `p-2` or `p-3`
- Rounded: `rounded-lg` or `rounded-full`
- Hover effect: `hover:bg-gray-100`

**Status Icons:**
- Success: Check icon + `text-success-600`
- Error: X icon + `text-danger-600`
- Warning: AlertTriangle icon + `text-warning-600`
- Info: Info icon + `text-info-600`

---

## 6. Buttons

### 6.1 Button Variants

**Primary Button (Solid)**

- **Purpose:** Main CTAs (Book Appointment, Submit, Save)
- **Appearance:** Solid background, high contrast
- **Classes:**
  ```
  Base: bg-primary-600 text-white font-semibold
  Hover: hover:bg-primary-700
  Active: active:bg-primary-800
  Focus: focus:ring-4 focus:ring-primary-200
  Disabled: disabled:opacity-50 disabled:cursor-not-allowed
  Shadow: shadow-lg shadow-primary-500/20
  Rounded: rounded-xl
  ```

**Secondary Button (Outlined)**
- **Purpose:** Secondary actions (Cancel, Back)
- **Appearance:** Border with transparent background
- **Classes:**
  ```
  Base: bg-transparent border-2 border-gray-300 text-gray-700 font-semibold
  Hover: hover:bg-gray-50 hover:border-gray-400
  Active: active:bg-gray-100
  Focus: focus:ring-4 focus:ring-gray-200
  Rounded: rounded-xl
  ```

**Ghost Button (Text Only)**
- **Purpose:** Tertiary actions, less emphasis
- **Appearance:** No background or border
- **Classes:**
  ```
  Base: bg-transparent text-primary-600 font-semibold
  Hover: hover:bg-primary-50
  Active: active:bg-primary-100
  Focus: focus:ring-4 focus:ring-primary-100
  Rounded: rounded-xl
  ```

**Success Button**
- **Purpose:** Confirm, Complete actions
- **Classes:**
  ```
  Base: bg-success-600 text-white font-semibold
  Hover: hover:bg-success-700
  Shadow: shadow-lg shadow-success-500/20
  Rounded: rounded-xl
  ```

**Danger Button**
- **Purpose:** Delete, Cancel critical actions
- **Classes:**
  ```
  Base: bg-danger-600 text-white font-semibold
  Hover: hover:bg-danger-700
  Shadow: shadow-lg shadow-danger-500/20
  Rounded: rounded-xl
  ```


**Glass Button (Glassmorphism)**
- **Purpose:** Floating CTAs, modern aesthetic
- **Appearance:** Frosted glass effect with blur
- **Classes:**
  ```
  Base: bg-white/20 backdrop-blur-md text-white font-semibold
        border border-white/30
  Hover: hover:bg-white/30
  Shadow: shadow-xl
  Rounded: rounded-2xl
  ```

### 6.2 Button Sizes

**Extra Small (xs)**
```
Padding: px-3 py-1.5
Text: text-xs
Icon: w-3 h-3
Min Height: 28px
```

**Small (sm)**
```
Padding: px-4 py-2
Text: text-sm
Icon: w-4 h-4
Min Height: 36px
```

**Medium (base) - Default**
```
Padding: px-6 py-2.5
Text: text-base
Icon: w-5 h-5
Min Height: 44px
```

**Large (lg)**
```
Padding: px-8 py-3
Text: text-lg
Icon: w-6 h-6
Min Height: 52px
```

**Extra Large (xl)**
```
Padding: px-10 py-4
Text: text-xl
Icon: w-6 h-6
Min Height: 60px
```

### 6.3 Button States

**Default**
- Normal appearance with subtle shadow

**Hover**
- Darker background (or lighter for outlined)
- Slightly larger shadow
- Smooth transition: `transition-all duration-200`

**Active (Pressed)**
- Even darker background
- Reduced shadow (pressed effect)
- Transform: `active:scale-95`


**Focus**
- Visible focus ring for accessibility
- Ring color matches button color
- `focus:outline-none focus:ring-4`

**Disabled**
- Reduced opacity: `opacity-50`
- No pointer events: `cursor-not-allowed`
- No hover effects

**Loading**
- Show spinner icon
- Disable button interaction
- Opacity: `opacity-70`
- Spinner classes: `animate-spin w-5 h-5`

### 6.4 Button Grouping

**Horizontal Button Group**
```
Container: flex items-center gap-3
Primary + Secondary pattern
```

**Vertical Button Group (Mobile)**
```
Container: flex flex-col gap-2
Stack buttons on small screens
```

**Icon Buttons**
```
Square: p-2.5 rounded-lg
Circle: p-2.5 rounded-full
Icon size: w-5 h-5
Background: hover:bg-gray-100
```

---

## 7. Cards

### 7.1 Card Variants

**Standard Card (Light Mode)**
- **Purpose:** General content containers
- **Appearance:** White background with subtle shadow
- **Classes:**
  ```
  Base: bg-white rounded-2xl shadow-lg
  Border: border border-gray-200
  Padding: p-6
  Hover: hover:shadow-xl transition-shadow duration-300
  ```

**Glass Card (Glassmorphism)**
- **Purpose:** Modern, floating content
- **Appearance:** Frosted glass with backdrop blur
- **Classes:**
  ```
  Base: bg-white/70 backdrop-blur-xl rounded-2xl
  Border: border border-white/30
  Shadow: shadow-xl shadow-gray-500/10
  Padding: p-6
  ```


**Elevated Card**
- **Purpose:** Important content, highlighted sections
- **Appearance:** Stronger shadow, more prominence
- **Classes:**
  ```
  Base: bg-white rounded-2xl shadow-2xl
  Border: border border-gray-100
  Padding: p-8
  Transform: hover:scale-[1.02] transition-transform
  ```

**Gradient Card**
- **Purpose:** Feature highlights, premium content
- **Appearance:** Gradient background
- **Classes:**
  ```
  Base: bg-gradient-to-br from-primary-500 to-primary-700
        rounded-2xl shadow-xl text-white
  Padding: p-6
  Shadow: shadow-primary-500/30
  ```

**Stat Card (Dashboard)**
- **Purpose:** Display metrics, statistics
- **Appearance:** Clean, minimal with icon
- **Classes:**
  ```
  Base: bg-white rounded-xl shadow-md p-5
  Border: border-l-4 border-primary-500
  Hover: hover:shadow-lg
  ```

**Interactive Card (Clickable)**
- **Purpose:** Navigation cards, selection cards
- **Appearance:** Hover and active states
- **Classes:**
  ```
  Base: bg-white rounded-2xl shadow-md p-6 cursor-pointer
  Hover: hover:shadow-xl hover:scale-[1.02]
  Active: active:scale-[0.98]
  Transition: transition-all duration-200
  ```

### 7.2 Card Components

**Card Header**
```
Classes: flex items-center justify-between mb-4 pb-4 border-b border-gray-200
Title: text-xl font-semibold text-gray-900
Subtitle: text-sm text-gray-500 mt-1
```

**Card Body**
```
Classes: text-gray-600 leading-relaxed
Spacing: space-y-4 (for multiple paragraphs)
```

**Card Footer**
```
Classes: flex items-center justify-between mt-6 pt-4 border-t border-gray-200
Buttons: Usually secondary or ghost buttons
```


**Card with Icon**
```
Icon Container: w-12 h-12 rounded-xl bg-primary-100 flex items-center justify-center
Icon: w-6 h-6 text-primary-600
Placement: Top of card or left-aligned
```

### 7.3 Card Layouts

**Grid Layout (3 Columns)**
```
Container: grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6
Responsive: Stacks on mobile, 2 cols on tablet, 3 on desktop
```

**List Layout (Full Width)**
```
Container: space-y-4
Each card: Full width with consistent padding
```

**Masonry Layout**
```
Container: columns-1 md:columns-2 lg:columns-3 gap-6
Cards: break-inside-avoid-column mb-6
```

### 7.4 Card Shadows & Depth

**Subtle Shadow (Resting State)**
```
shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1)
```

**Medium Shadow (Default)**
```
shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1)
```

**Strong Shadow (Hover/Elevated)**
```
shadow-xl: 0 20px 25px -5px rgba(0,0,0,0.1)
```

**Colored Shadow (Brand Cards)**
```
shadow-xl shadow-primary-500/20
shadow-xl shadow-success-500/20
```

---

## 8. Forms

### 8.1 Input Fields

**Text Input (Default)**
- **Appearance:** Rounded rectangle with border
- **Classes:**
  ```
  Base: w-full px-4 py-3 rounded-xl border-2 border-gray-300
        text-gray-900 placeholder-gray-400
        bg-white
  Focus: focus:border-primary-500 focus:ring-4 focus:ring-primary-200
         focus:outline-none
  Disabled: disabled:bg-gray-100 disabled:cursor-not-allowed
  Error: border-danger-500 focus:ring-danger-200
  Success: border-success-500 focus:ring-success-200
  Transition: transition-all duration-200
  ```


**Glass Input (Glassmorphism)**
- **Appearance:** Frosted glass effect
- **Classes:**
  ```
  Base: w-full px-4 py-3 rounded-xl
        bg-white/50 backdrop-blur-md
        border border-white/30
        text-gray-900 placeholder-gray-500
  Focus: focus:bg-white/70 focus:border-white/50
  ```

**Input Sizes**

Small:
```
px-3 py-2 text-sm rounded-lg
Height: 36px
```

Medium (Default):
```
px-4 py-3 text-base rounded-xl
Height: 44px
```

Large:
```
px-6 py-4 text-lg rounded-xl
Height: 56px
```

### 8.2 Form Labels

**Label Style**
```
Classes: block text-sm font-medium text-gray-700 mb-2
Required indicator: text-danger-500 ml-1
```

**Floating Label (Modern)**
```
Position: Absolute, moves up on focus
Classes: absolute left-4 top-3 text-gray-500 text-sm
         peer-focus:-top-2 peer-focus:left-3 peer-focus:text-xs
         peer-focus:bg-white peer-focus:px-2
         peer-focus:text-primary-600
         transition-all duration-200
```

### 8.3 Form Helper Text & Validation

**Helper Text**
```
Classes: text-xs text-gray-500 mt-1.5
Icon: Info icon (w-3.5 h-3.5) inline
```

**Error Message**
```
Classes: text-xs text-danger-600 mt-1.5 flex items-center
Icon: AlertCircle (w-4 h-4 mr-1)
```

**Success Message**
```
Classes: text-xs text-success-600 mt-1.5 flex items-center
Icon: Check (w-4 h-4 mr-1)
```

### 8.4 Select Dropdown

```
Base: Same as text input
Icon: ChevronDown (w-5 h-5 absolute right-3)
Appearance: appearance-none (remove default styling)
Padding: pr-10 (space for icon)
```

**Dropdown Menu (Custom)**
```
Container: absolute w-full mt-2 bg-white rounded-xl shadow-xl
           border border-gray-200 z-50 max-h-60 overflow-auto
Options: px-4 py-3 hover:bg-primary-50 cursor-pointer
         transition-colors duration-150
Selected: bg-primary-100 text-primary-700 font-medium
```

### 8.5 Checkbox & Radio

**Checkbox**
```
Input: w-5 h-5 rounded-md border-2 border-gray-300
       text-primary-600 focus:ring-4 focus:ring-primary-200
       cursor-pointer
Label: ml-3 text-sm text-gray-700 cursor-pointer
Container: flex items-center
```

**Radio Button**
```
Input: w-5 h-5 rounded-full border-2 border-gray-300
       text-primary-600 focus:ring-4 focus:ring-primary-200
       cursor-pointer
Label: ml-3 text-sm text-gray-700 cursor-pointer
```

**Toggle Switch**
```
Track: w-11 h-6 bg-gray-300 rounded-full
       peer-checked:bg-primary-600
       transition-colors duration-200
Circle: w-5 h-5 bg-white rounded-full shadow-md
        transform translate-x-0 peer-checked:translate-x-5
        transition-transform duration-200
```

### 8.6 Textarea

```
Base: Same as text input
Rows: rows-4 (default), adjustable
Resize: resize-none or resize-vertical
Min height: min-h-[100px]
```

### 8.7 File Upload

**Upload Area (Drag & Drop)**
```
Container: border-2 border-dashed border-gray-300 rounded-xl
           p-8 text-center bg-gray-50
           hover:border-primary-500 hover:bg-primary-50
           transition-all duration-200
Icon: Upload icon (w-12 h-12) text-gray-400
Text: text-sm text-gray-600
Button: text-primary-600 font-semibold underline
```


### 8.8 Search Input

```
Container: relative
Input: pl-10 (space for icon)
Icon: Search icon, absolute left-3 top-1/2 -translate-y-1/2
      w-5 h-5 text-gray-400
Clear button: X icon, absolute right-3 (when has value)
```

### 8.9 Form Layouts

**Vertical Form (Default)**
```
Container: space-y-6
Field spacing: mb-6
Full width inputs
```

**Horizontal Form (Label + Input side by side)**
```
Container: grid grid-cols-12 gap-4 items-center
Label: col-span-3 text-right
Input: col-span-9
```

**Inline Form**
```
Container: flex items-center gap-3
Inputs: flex-1
Submit button: flex-shrink-0
```

**Multi-column Form**
```
Container: grid grid-cols-1 md:grid-cols-2 gap-6
Full-width fields: col-span-full
```

---

## 9. Tables

### 9.1 Table Variants

**Standard Table**
- **Appearance:** Clean, bordered rows
- **Classes:**
  ```
  Table: w-full border-collapse
  Container: overflow-x-auto rounded-xl border border-gray-200
  ```

**Striped Table**
- **Appearance:** Alternating row colors
- **Classes:**
  ```
  Odd rows: bg-white
  Even rows: bg-gray-50
  ```

**Hoverable Table**
- **Appearance:** Row highlights on hover
- **Classes:**
  ```
  Row hover: hover:bg-primary-50 transition-colors duration-150
  Cursor: cursor-pointer (for clickable rows)
  ```

### 9.2 Table Structure

**Table Head**
```
<thead>: bg-gray-100 border-b-2 border-gray-200
<th>: px-6 py-4 text-left text-xs font-semibold text-gray-700
      uppercase tracking-wider
Sticky header: sticky top-0 z-10 bg-gray-100
```


**Table Body**
```
<tbody>: bg-white divide-y divide-gray-200
<tr>: hover:bg-gray-50 transition-colors
<td>: px-6 py-4 text-sm text-gray-900
Whitespace: whitespace-nowrap (for compact content)
```

**Table Footer**
```
<tfoot>: bg-gray-50 border-t-2 border-gray-200
<td>: px-6 py-4 font-semibold text-gray-900
```

### 9.3 Table Cells Content Types

**Text Cell**
```
Classes: text-gray-900 font-medium
Truncate: max-w-xs truncate (for long text)
```

**Status Badge Cell**
```
Badge: inline-flex px-3 py-1 rounded-full text-xs font-semibold
Success: bg-success-100 text-success-800
Warning: bg-warning-100 text-warning-800
Danger: bg-danger-100 text-danger-800
Info: bg-info-100 text-info-800
```

**Action Cell**
```
Alignment: text-right
Buttons: Inline icon buttons or dropdown
Spacing: space-x-2
```

**Avatar Cell**
```
Container: flex items-center space-x-3
Avatar: w-10 h-10 rounded-full
Name: text-sm font-medium text-gray-900
Subtitle: text-xs text-gray-500
```

**Number Cell (Right-aligned)**
```
Classes: text-right font-mono text-gray-900
Currency: font-semibold
Percentage: text-success-600 (positive) or text-danger-600 (negative)
```

### 9.4 Responsive Tables

**Mobile Card View**
```
Desktop: table display
Mobile: Each row becomes a card
        block w-full mb-4 bg-white rounded-lg shadow p-4
Label: Show data labels inline
       font-medium text-gray-700 mr-2
```

**Horizontal Scroll**
```
Container: overflow-x-auto
Table: min-w-full
Mobile: Scroll horizontally, preserve table structure
```


### 9.5 Table Features

**Sortable Headers**
```
Header: cursor-pointer hover:bg-gray-200 transition-colors
Icon: ChevronUp or ChevronDown (w-4 h-4 ml-1 inline)
Active: text-primary-600 font-bold
```

**Selectable Rows**
```
Checkbox: First column, w-4 h-4
Selected row: bg-primary-50 border-l-4 border-primary-500
Select all: Checkbox in header
```

**Expandable Rows**
```
Trigger: ChevronRight icon (rotates to ChevronDown when expanded)
Expanded content: colspan="full" bg-gray-50 p-4
                  border-t border-gray-200
Transition: max-height animation
```

**Pagination**
```
Container: flex items-center justify-between px-6 py-4
          bg-white border-t border-gray-200
Info: text-sm text-gray-700
Buttons: Previous/Next with ChevronLeft/Right icons
Page numbers: px-3 py-1 rounded-lg hover:bg-gray-100
              active:bg-primary-600 active:text-white
```

**Empty State**
```
Container: py-12 text-center
Icon: Large icon (w-16 h-16) text-gray-300
Message: text-gray-500 mt-4
Action: Primary button to add first item
```

---

## 10. Navigation

### 10.1 Top Navigation Bar

**Desktop Navigation**
```
Container: sticky top-0 z-50 bg-white/80 backdrop-blur-lg
          border-b border-gray-200 shadow-sm
Layout: flex items-center justify-between px-8 py-4
Max width: max-w-7xl mx-auto
```

**Logo Section**
```
Container: flex items-center space-x-3
Logo: h-8 w-auto
Text: text-xl font-bold text-gray-900
```

**Navigation Links**
```
Container: hidden md:flex items-center space-x-1
Link: px-4 py-2 rounded-lg text-sm font-medium text-gray-700
      hover:bg-primary-50 hover:text-primary-700
      transition-all duration-200
Active: bg-primary-100 text-primary-700 font-semibold
```


**Right Section (Actions)**
```
Container: flex items-center space-x-3
Notification: Relative, icon button with badge
              Badge: absolute -top-1 -right-1 w-5 h-5 
                     bg-danger-500 rounded-full text-xs text-white
Avatar: w-10 h-10 rounded-full cursor-pointer
        border-2 border-transparent hover:border-primary-500
Dropdown: Appears below avatar on click
```

**Mobile Menu Toggle**
```
Button: md:hidden p-2 rounded-lg hover:bg-gray-100
Icon: Menu icon (w-6 h-6)
Position: Right side of navbar
```

### 10.2 Mobile Navigation

**Mobile Menu (Drawer)**
```
Container: fixed inset-y-0 left-0 z-50 w-64 bg-white
          shadow-2xl transform transition-transform
Closed: -translate-x-full
Open: translate-x-0
Overlay: fixed inset-0 bg-black/50 backdrop-blur-sm
```

**Mobile Menu Content**
```
Header: flex items-center justify-between p-6 border-b
Close button: p-2 rounded-lg hover:bg-gray-100
Links: px-6 py-3 text-base font-medium text-gray-700
       hover:bg-primary-50 hover:text-primary-700
Active: bg-primary-100 text-primary-700 border-r-4 border-primary-600
```

### 10.3 Breadcrumbs

```
Container: flex items-center space-x-2 text-sm mb-6
Item: text-gray-500 hover:text-primary-600
Active: text-gray-900 font-medium
Separator: ChevronRight icon (w-4 h-4 text-gray-400)
```

### 10.4 Tabs Navigation

**Primary Tabs**
```
Container: border-b border-gray-200 mb-6
Tab list: flex space-x-8
Tab: pb-4 px-1 border-b-2 border-transparent
     text-gray-600 hover:text-gray-900 hover:border-gray-300
     font-medium transition-all duration-200
Active: text-primary-600 border-primary-600
```

**Pills Tabs (Alternative)**
```
Container: bg-gray-100 p-1 rounded-xl inline-flex gap-1
Tab: px-6 py-2 rounded-lg text-sm font-medium
     text-gray-700 hover:text-gray-900
Active: bg-white text-primary-700 shadow-md
```


### 10.5 Dropdown Menu

**User Dropdown**
```
Container: absolute right-0 top-full mt-2 w-56
          bg-white rounded-xl shadow-xl border border-gray-200
          py-2 z-50
Arrow: Absolute -top-2 right-4 w-4 h-4 bg-white
       border-l border-t border-gray-200 rotate-45
```

**Menu Items**
```
Item: px-4 py-2.5 flex items-center space-x-3
      hover:bg-primary-50 text-gray-700 hover:text-primary-700
      transition-colors cursor-pointer
Icon: w-5 h-5
Text: text-sm font-medium
Divider: my-2 border-t border-gray-200
```

**Menu Footer (Logout)**
```
Item: px-4 py-2.5 text-danger-600 hover:bg-danger-50
      border-t border-gray-200 font-medium
```

---

## 11. Sidebar

### 11.1 Desktop Sidebar

**Sidebar Container**
```
Position: fixed inset-y-0 left-0 z-40
Width: w-64 (256px)
Background: bg-white border-r border-gray-200
Shadow: shadow-lg
```

**Sidebar Glass (Alternative)**
```
Background: bg-white/70 backdrop-blur-xl
Border: border-r border-white/30
```

**Sidebar Header**
```
Container: px-6 py-8 border-b border-gray-200
Logo: flex items-center space-x-3
Icon: w-10 h-10
Text: text-xl font-bold text-gray-900
```

### 11.2 Sidebar Navigation

**Nav Container**
```
Padding: px-4 py-6
Spacing: space-y-1
```

**Nav Section Title**
```
Classes: px-3 py-2 text-xs font-semibold text-gray-400
        uppercase tracking-wider
```

**Nav Link**
```
Base: flex items-center space-x-3 px-3 py-2.5 rounded-xl
      text-gray-700 font-medium
      hover:bg-primary-50 hover:text-primary-700
      transition-all duration-200
Icon: w-5 h-5
Text: text-sm
```


**Active Nav Link**
```
Classes: bg-primary-100 text-primary-700
Border: border-l-4 border-primary-600 (alternative)
Icon: text-primary-600
```

**Nav Badge (Notification Count)**
```
Classes: ml-auto px-2 py-0.5 text-xs font-semibold
        rounded-full bg-danger-100 text-danger-700
```

### 11.3 Collapsible Sidebar

**Collapsed State**
```
Width: w-20 (80px)
Icons: Center-aligned, no text
Tooltip: Show text on hover
```

**Toggle Button**
```
Position: absolute -right-3 top-6
Button: w-6 h-6 rounded-full bg-white border-2 border-gray-300
        shadow-md hover:bg-gray-50
Icon: ChevronLeft (collapsed) / ChevronRight (expanded)
```

### 11.4 Sidebar Footer

**User Profile Section**
```
Container: absolute bottom-0 left-0 right-0 p-4
          border-t border-gray-200 bg-gray-50
Layout: flex items-center space-x-3
Avatar: w-10 h-10 rounded-full
Info: flex-1
Name: text-sm font-semibold text-gray-900
Role: text-xs text-gray-500
Action: Icon button (Settings, Logout)
```

### 11.5 Nested Navigation

**Expandable Section**
```
Parent: flex items-center justify-between
Icon: ChevronRight (collapsed) / ChevronDown (expanded)
      transition-transform duration-200
```

**Child Links**
```
Container: pl-8 mt-1 space-y-1
Link: Smaller padding (py-2)
      Border left: border-l-2 border-gray-200
Active child: border-primary-600 text-primary-700
```

### 11.6 Sidebar Overlay (Mobile)

**Mobile Sidebar**
```
Same as drawer navigation
Appears from left: transform -translate-x-full to translate-x-0
Overlay: fixed inset-0 bg-black/50 backdrop-blur-sm z-30
```

---

## 12. Dark Mode

### 12.1 Dark Mode Color Palette

**Background Colors**
```
dark-bg-primary:   #0F172A  (slate-900) - Main background
dark-bg-secondary: #1E293B  (slate-800) - Cards, panels
dark-bg-tertiary:  #334155  (slate-700) - Elevated elements
```


**Text Colors**
```
dark-text-primary:   #F8FAFC  (slate-50)  - Headings
dark-text-secondary: #CBD5E1  (slate-300) - Body text
dark-text-tertiary:  #94A3B8  (slate-400) - Secondary text
dark-text-muted:     #64748B  (slate-500) - Muted text
```

**Border Colors**
```
dark-border:         #334155  (slate-700)
dark-border-subtle:  #1E293B  (slate-800)
```

**Primary Colors (Dark Mode)**
```
Same as light mode but slightly adjusted:
dark-primary-400: #60A5FA  (Lighter for better contrast)
dark-primary-500: #3B82F6  (Main)
dark-primary-600: #2563EB  (Hover)
```

### 12.2 Dark Mode Components

**Cards in Dark Mode**
```
Base: dark:bg-slate-800 dark:border-slate-700
Glass: dark:bg-slate-800/70 dark:backdrop-blur-xl
      dark:border-slate-700/50
Shadow: dark:shadow-2xl dark:shadow-black/50
Text: dark:text-slate-50
```

**Buttons in Dark Mode**
```
Primary: dark:bg-primary-500 dark:hover:bg-primary-600
         (same as light mode)
Secondary: dark:bg-slate-700 dark:border-slate-600
          dark:text-slate-200 dark:hover:bg-slate-600
Ghost: dark:text-primary-400 dark:hover:bg-slate-800
```

**Inputs in Dark Mode**
```
Base: dark:bg-slate-800 dark:border-slate-600
      dark:text-slate-100 dark:placeholder-slate-500
Focus: dark:border-primary-400 dark:ring-primary-900/30
Disabled: dark:bg-slate-900 dark:text-slate-600
```

**Navigation in Dark Mode**
```
Navbar: dark:bg-slate-900/80 dark:border-slate-800
Link: dark:text-slate-300 dark:hover:bg-slate-800
      dark:hover:text-slate-100
Active: dark:bg-slate-800 dark:text-primary-400
```

**Sidebar in Dark Mode**
```
Base: dark:bg-slate-900 dark:border-slate-800
Link: dark:text-slate-300 dark:hover:bg-slate-800
Active: dark:bg-slate-800 dark:text-primary-400
      dark:border-primary-500
Section title: dark:text-slate-500
```


**Tables in Dark Mode**
```
Base: dark:bg-slate-900 dark:border-slate-700
Header: dark:bg-slate-800 dark:text-slate-300
Row: dark:hover:bg-slate-800/50
Cell: dark:text-slate-300
Striped: dark:odd:bg-slate-900 dark:even:bg-slate-800/50
```

### 12.3 Dark Mode Glassmorphism

**Glass Cards (Dark)**
```
Background: dark:bg-slate-800/50 dark:backdrop-blur-xl
Border: dark:border-slate-700/50
Shadow: dark:shadow-2xl dark:shadow-black/50
```

**Glass Navbar (Dark)**
```
Background: dark:bg-slate-900/70 dark:backdrop-blur-xl
Border: dark:border-slate-800/50
```

### 12.4 Dark Mode Toggle

**Toggle Button**
```
Base: p-2 rounded-lg hover:bg-gray-100
      dark:hover:bg-slate-800 transition-colors
Icon: Sun icon (light mode) / Moon icon (dark mode)
      w-5 h-5 text-gray-600 dark:text-slate-400
```

**Position:**
- Top right corner of navbar
- Next to user avatar or notification icon

### 12.5 Dark Mode Best Practices

**Contrast Ratios:**
- Heading text: Minimum 7:1 contrast ratio
- Body text: Minimum 4.5:1 contrast ratio
- Interactive elements: Clear focus indicators

**Color Adjustments:**
- Use lighter primary colors for dark mode
- Increase shadows for depth perception
- Soften borders (less contrast)
- Maintain brand colors but adjust brightness

**Transitions:**
- Smooth color transitions: `transition-colors duration-200`
- Apply to all color-changing elements
- Use `prefers-color-scheme` media query

---

## 13. Light Mode

### 13.1 Light Mode Color Strategy

**Background Hierarchy**
```
Page background:    bg-gray-50   (#F9FAFB)
Card background:    bg-white     (#FFFFFF)
Elevated elements:  bg-white + shadow-xl
Subtle backgrounds: bg-gray-100  (#F3F4F6)
```

**Text Hierarchy**
```
Primary headings:   text-gray-900  (#111827)
Subheadings:        text-gray-800  (#1F2937)
Body text:          text-gray-700  (#374151)
Secondary text:     text-gray-600  (#4B5563)
Muted text:         text-gray-500  (#6B7280)
Disabled text:      text-gray-400  (#9CA3AF)
```


**Border & Dividers**
```
Strong borders:     border-gray-300  (#D1D5DB)
Subtle borders:     border-gray-200  (#E5E7EB)
Very subtle:        border-gray-100  (#F3F4F6)
```

### 13.2 Light Mode Components

**Cards**
```
Standard: bg-white border border-gray-200 shadow-lg
Glass: bg-white/70 backdrop-blur-xl border-white/30
Elevated: bg-white shadow-2xl
Hover: hover:shadow-xl transition-shadow
```

**Buttons**
```
Primary: bg-primary-600 hover:bg-primary-700
         shadow-lg shadow-primary-500/20
Secondary: bg-white border-2 border-gray-300
          hover:bg-gray-50 text-gray-700
Ghost: text-primary-600 hover:bg-primary-50
```

**Forms**
```
Input: bg-white border-2 border-gray-300
       focus:border-primary-500 focus:ring-primary-200
Label: text-gray-700 font-medium
Helper: text-gray-500
Error: border-danger-500 text-danger-600
```

**Navigation**
```
Navbar: bg-white/80 backdrop-blur-lg border-gray-200
Link: text-gray-700 hover:bg-primary-50 hover:text-primary-700
Active: bg-primary-100 text-primary-700
```

**Tables**
```
Container: bg-white border border-gray-200
Header: bg-gray-100 text-gray-700
Row: hover:bg-gray-50
Cell: text-gray-900
Striped: even:bg-gray-50
```

### 13.3 Light Mode Shadows

**Elevation System**
```
Level 0 (flat):     shadow-none
Level 1 (subtle):   shadow-sm    (cards at rest)
Level 2 (default):  shadow-md    (buttons, inputs)
Level 3 (raised):   shadow-lg    (dropdowns, modals)
Level 4 (floating): shadow-xl    (sticky headers)
Level 5 (highest):  shadow-2xl   (modal overlays)
```

**Colored Shadows (Brand Elements)**
```
Primary shadow:  shadow-lg shadow-primary-500/20
Success shadow:  shadow-lg shadow-success-500/20
Warning shadow:  shadow-lg shadow-warning-500/20
Danger shadow:   shadow-lg shadow-danger-500/20
```


### 13.4 Light Mode Accessibility

**Focus States**
```
All interactive elements must have visible focus:
- Ring: focus:ring-4 focus:ring-primary-200
- Outline: focus:outline-none (with ring)
- Border: focus:border-primary-500
```

**Contrast Requirements**
- Body text on white: Must meet 4.5:1 ratio → gray-700
- Headings on white: Must meet 4.5:1 ratio → gray-900
- Interactive elements: Clear visual distinction
- Disabled states: Obvious visual difference

**Color Blindness Considerations**
- Don't rely on color alone for meaning
- Use icons + color for status
- Provide text labels
- Test with color blindness simulators

### 13.5 Light Mode Best Practices

**Whitespace:**
- Generous padding and margins
- Clear visual breathing room
- Use gray-50 backgrounds to separate sections

**Hierarchy:**
- Use size, weight, and color to create hierarchy
- Primary actions stand out (colored buttons)
- Secondary actions are more subtle

**Consistency:**
- Maintain consistent spacing
- Use design tokens from spacing system
- Follow established patterns

**Performance:**
- Optimize shadow usage (can impact performance)
- Use backdrop-blur sparingly
- Minimize gradient usage on large areas

---

## 14. Additional Design Tokens

### 14.1 Border Radius

```
rounded-none:   0px       - No rounding
rounded-sm:     2px       - Subtle (0.125rem)
rounded:        4px       - Default (0.25rem)
rounded-md:     6px       - Moderate (0.375rem)
rounded-lg:     8px       - Large (0.5rem)
rounded-xl:     12px      - Extra large (0.75rem) ← Most used
rounded-2xl:    16px      - 2XL (1rem)
rounded-3xl:    24px      - 3XL (1.5rem)
rounded-full:   9999px    - Circular
```

**Usage:**
- Buttons: `rounded-xl` (12px)
- Cards: `rounded-2xl` (16px)
- Inputs: `rounded-xl` (12px)
- Modals: `rounded-2xl` (16px)
- Badges: `rounded-full`
- Avatars: `rounded-full`


### 14.2 Opacity Scale

```
opacity-0:    0%     - Invisible
opacity-5:    5%     - Nearly invisible
opacity-10:   10%    - Very transparent
opacity-20:   20%    - Transparent
opacity-30:   30%    - Glass overlays
opacity-40:   40%    - 
opacity-50:   50%    - Semi-transparent (glass)
opacity-60:   60%    - 
opacity-70:   70%    - Glass cards
opacity-75:   75%    - Modals backdrop
opacity-80:   80%    - 
opacity-90:   90%    - Nearly opaque
opacity-95:   95%    - 
opacity-100:  100%   - Fully opaque
```

### 14.3 Z-Index Layers

```
z-0:     0      - Base layer
z-10:    10     - Content
z-20:    20     - Dropdowns
z-30:    30     - Fixed elements (sidebar overlay)
z-40:    40     - Sidebar, fixed panels
z-50:    50     - Modal backdrop, top navigation
z-60:    60     - Modal content
z-70:    70     - Tooltips, popovers
z-80:    80     - 
z-90:    90     - 
z-100:   100    - Highest priority (notifications toast)
```

### 14.4 Transitions & Animations

**Duration**
```
duration-75:    75ms    - Very fast
duration-100:   100ms   - Fast
duration-150:   150ms   - Quick
duration-200:   200ms   - Default (most used)
duration-300:   300ms   - Medium
duration-500:   500ms   - Slow
duration-700:   700ms   - Very slow
duration-1000:  1000ms  - Extra slow
```

**Easing Functions**
```
ease-linear:     linear              - Constant speed
ease-in:         cubic-bezier(0.4, 0, 1, 1)
ease-out:        cubic-bezier(0, 0, 0.2, 1)  ← Recommended
ease-in-out:     cubic-bezier(0.4, 0, 0.2, 1)
```

**Common Transitions**
```
Button hover:      transition-all duration-200 ease-out
Card hover:        transition-shadow duration-300 ease-out
Color changes:     transition-colors duration-200
Transform:         transition-transform duration-200
Backdrop blur:     transition-all duration-300
```

**Animations**
```
Spin (loading):    animate-spin
Ping (badge):      animate-ping
Pulse:             animate-pulse
Bounce:            animate-bounce
```


### 14.5 Breakpoints (Responsive)

```
sm:   640px    - Small devices (large phones landscape)
md:   768px    - Medium devices (tablets)
lg:   1024px   - Large devices (laptops)
xl:   1280px   - Extra large (desktops)
2xl:  1536px   - 2X large (large desktops)
```

**Mobile-First Approach:**
```
Base styles: Mobile (< 640px)
sm: Small tablets and up
md: Tablets and up (most common breakpoint)
lg: Desktop and up
xl: Large desktop
```

**Common Patterns:**
```
Grid: grid-cols-1 md:grid-cols-2 lg:grid-cols-3
Text: text-2xl md:text-3xl lg:text-4xl
Padding: px-4 md:px-6 lg:px-8
Hidden: hidden md:block (hide on mobile)
```

---

## 15. Component Interactions & States

### 15.1 Hover States

**Cards**
```
Transform: hover:scale-[1.02]
Shadow: hover:shadow-xl
Transition: transition-all duration-300
```

**Buttons**
```
Background: hover:bg-primary-700
Transform: hover:scale-105 active:scale-95
Shadow: hover:shadow-lg
```

**Links**
```
Color: hover:text-primary-700
Underline: hover:underline (optional)
Background: hover:bg-primary-50 (when in list)
```

### 15.2 Active States

**Buttons**
```
Transform: active:scale-95
Background: active:bg-primary-800
```

**Clickable Cards**
```
Transform: active:scale-[0.98]
Shadow: active:shadow-md
```

### 15.3 Focus States (Accessibility)

**All Interactive Elements**
```
Ring: focus:ring-4 focus:ring-primary-200
Outline: focus:outline-none (use ring instead)
Border: focus:border-primary-500
```

**Keyboard Navigation**
```
Visible focus indicators on all focusable elements
Tab order follows logical reading order
Skip links for keyboard users
```


### 15.4 Loading States

**Button Loading**
```
Icon: Spinning circle (animate-spin)
Text: "Loading..." or hide text
Disabled: opacity-70 cursor-not-allowed
```

**Skeleton Loaders**
```
Base: bg-gray-200 rounded animate-pulse
Height: Match expected content height
Width: Match expected content width
```

**Spinner**
```
Size: w-6 h-6 to w-12 h-12
Color: border-primary-600
Animation: animate-spin
Border: border-4 border-t-transparent
```

### 15.5 Disabled States

```
Opacity: opacity-50
Cursor: cursor-not-allowed
Background: Grayed out (bg-gray-100)
Text: text-gray-400
No hover effects
```

### 15.6 Error States

**Form Inputs**
```
Border: border-danger-500
Ring: focus:ring-danger-200
Icon: AlertCircle (text-danger-500)
Message: text-danger-600 text-sm mt-1
```

**Inline Errors**
```
Background: bg-danger-50 border-l-4 border-danger-500
Icon: AlertCircle
Text: text-danger-800
Padding: p-4
```

### 15.7 Success States

**Form Inputs**
```
Border: border-success-500
Icon: Check (text-success-500)
Message: text-success-600 text-sm mt-1
```

**Success Alerts**
```
Background: bg-success-50 border-l-4 border-success-500
Icon: CheckCircle
Text: text-success-800
```

---

## 16. Tailwind Configuration

### 16.1 tailwind.config.js

```javascript
module.exports = {
  darkMode: 'class',
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#EBF5FF',
          100: '#D1E9FF',
          200: '#B2DBFF',
          300: '#84C5FF',
          400: '#53A8FF',
          500: '#2E90FA',
          600: '#1570EF',
          700: '#175CD3',
          800: '#1849A9',
          900: '#194185',
        },
        success: {
          50: '#ECFDF3',
          100: '#D1FADF',
          200: '#A6F4C5',
          300: '#6CE9A6',
          400: '#32D583',
          500: '#12B76A',
          600: '#039855',
          700: '#027A48',
          800: '#05603A',
          900: '#054F31',
        },
        accent: {
          50: '#FFF4ED',
          100: '#FFE6D5',
          200: '#FFD6AE',
          300: '#FFBC8B',
          400: '#FF9C66',
          500: '#FF7A47',
          600: '#FF5A1F',
          700: '#E04F1A',
          800: '#C1410F',
          900: '#A23A0F',
        },
        warning: {
          50: '#FFFAEB',
          100: '#FEF0C7',
          200: '#FEDF89',
          300: '#FEC84B',
          400: '#FDB022',
          500: '#F79009',
          600: '#DC6803',
          700: '#B54708',
          800: '#93370D',
          900: '#7A2E0E',
        },
        danger: {
          50: '#FEF3F2',
          100: '#FEE4E2',
          200: '#FECDCA',
          300: '#FDA29B',
          400: '#F97066',
          500: '#F04438',
          600: '#D92D20',
          700: '#B42318',
          800: '#912018',
          900: '#7A271A',
        },
        info: {
          50: '#F4F3FF',
          100: '#EBE9FE',
          200: '#D9D6FE',
          300: '#BDB4FE',
          400: '#9B8AFB',
          500: '#7A5AF8',
          600: '#6938EF',
          700: '#5925DC',
          800: '#4A1FB8',
          900: '#3E1C96',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        heading: ['Manrope', 'Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.07)',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
```

---

## 17. Design System Summary

### 17.1 Key Design Principles

✅ **Healthcare-First Design**
- Medical blue (#2E90FA) as primary color
- Calming, trust-building aesthetics
- Professional, clinical precision

✅ **Glassmorphism Aesthetic**
- Frosted glass effects with backdrop-blur
- Layered depth perception
- Modern, premium feel

✅ **Accessibility**
- WCAG 2.1 AA compliance
- High contrast ratios
- Clear focus indicators
- Keyboard navigation support

✅ **Responsive Design**
- Mobile-first approach
- Breakpoint-based layouts
- Touch-friendly interactions

✅ **Consistent Spacing**
- 8px base unit system
- Predictable, rhythmic layout
- Clear visual hierarchy

### 17.2 Component Checklist


**Base Components:**
- [x] Color Palette (Primary, Secondary, Semantic)
- [x] Typography System (Fonts, Sizes, Weights)
- [x] Spacing Scale (8px base unit)
- [x] Icon Guidelines (Lucide React)

**Interactive Components:**
- [x] Buttons (6 variants, 5 sizes)
- [x] Forms (Inputs, Select, Checkbox, Radio, Toggle)
- [x] Cards (6 variants, glassmorphism)
- [x] Tables (Sortable, filterable, responsive)

**Navigation Components:**
- [x] Top Navigation (Glass navbar)
- [x] Sidebar (Collapsible, nested)
- [x] Breadcrumbs
- [x] Tabs
- [x] Dropdown Menus

**Modes:**
- [x] Light Mode (Complete)
- [x] Dark Mode (Complete with slate colors)

**Additional:**
- [x] Shadows & Elevation
- [x] Border Radius
- [x] Animations & Transitions
- [x] Responsive Breakpoints
- [x] Component States (Hover, Active, Focus, Disabled, Loading)
- [x] Tailwind Configuration

### 17.3 Usage Guidelines

**For Developers:**
1. Use Tailwind utility classes as defined in this design system
2. Follow component structure and naming conventions
3. Maintain consistent spacing using the 8px grid
4. Test all components in both light and dark modes
5. Ensure keyboard accessibility for all interactive elements

**For Designers:**
1. Reference this document for all UI specifications
2. Use the defined color palette (no custom colors without justification)
3. Maintain typography hierarchy
4. Use glassmorphism sparingly for modern aesthetic
5. Design mobile-first, then scale up

### 17.4 Healthcare-Specific Considerations

**Color Psychology:**
- Blue: Trust, stability, professionalism
- Green: Health, wellness, growth
- Warm accents: Compassion, care, comfort
- Red: Critical alerts, urgent attention

**Medical Data Display:**
- Use monospace font for numbers and measurements
- Clear labels for all medical data
- Status indicators with both color AND icons
- Large, readable text for vital signs

**Patient Comfort:**
- Calming color schemes
- Generous whitespace
- Soft, rounded corners
- Smooth animations (not jarring)

**Doctor Efficiency:**
- Quick-access navigation
- Dense information display options
- Keyboard shortcuts
- Efficient table layouts


---

## 18. Quick Reference Cheat Sheet

### Common Patterns

**Standard Card**
```
className="bg-white rounded-2xl shadow-lg border border-gray-200 p-6
           hover:shadow-xl transition-shadow duration-300
           dark:bg-slate-800 dark:border-slate-700"
```

**Glass Card**
```
className="bg-white/70 backdrop-blur-xl rounded-2xl border border-white/30
           shadow-xl p-6
           dark:bg-slate-800/70 dark:border-slate-700/50"
```

**Primary Button**
```
className="px-6 py-2.5 bg-primary-600 text-white font-semibold
           rounded-xl shadow-lg shadow-primary-500/20
           hover:bg-primary-700 hover:scale-105
           active:scale-95 transition-all duration-200
           focus:ring-4 focus:ring-primary-200 focus:outline-none
           disabled:opacity-50 disabled:cursor-not-allowed"
```

**Text Input**
```
className="w-full px-4 py-3 rounded-xl border-2 border-gray-300
           text-gray-900 placeholder-gray-400 bg-white
           focus:border-primary-500 focus:ring-4 focus:ring-primary-200
           focus:outline-none transition-all duration-200
           disabled:bg-gray-100 disabled:cursor-not-allowed
           dark:bg-slate-800 dark:border-slate-600 dark:text-slate-100"
```

**Navigation Link**
```
className="flex items-center space-x-3 px-3 py-2.5 rounded-xl
           text-gray-700 font-medium hover:bg-primary-50
           hover:text-primary-700 transition-all duration-200
           dark:text-slate-300 dark:hover:bg-slate-800"
```

**Active Navigation Link**
```
className="flex items-center space-x-3 px-3 py-2.5 rounded-xl
           bg-primary-100 text-primary-700 font-semibold
           dark:bg-slate-800 dark:text-primary-400"
```

**Section Heading**
```
className="text-3xl font-bold text-gray-900 mb-6
           dark:text-slate-50 font-heading"
```

**Body Text**
```
className="text-base text-gray-600 leading-normal
           dark:text-slate-300"
```

**Status Badge - Success**
```
className="inline-flex px-3 py-1 rounded-full text-xs font-semibold
           bg-success-100 text-success-800
           dark:bg-success-900/30 dark:text-success-400"
```

**Icon Button**
```
className="p-2.5 rounded-lg hover:bg-gray-100 transition-colors
           dark:hover:bg-slate-800"
```

---

## 19. Export Assets

### 19.1 Design Tokens (JSON)

```json
{
  "colors": {
    "primary": {
      "50": "#EBF5FF",
      "500": "#2E90FA",
      "600": "#1570EF"
    },
    "success": {
      "500": "#12B76A"
    },
    "danger": {
      "500": "#F04438"
    }
  },
  "spacing": {
    "base": "8px",
    "scale": [0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96]
  },
  "typography": {
    "fontFamily": {
      "primary": "Inter",
      "heading": "Manrope",
      "mono": "JetBrains Mono"
    },
    "fontSize": {
      "xs": "12px",
      "sm": "14px",
      "base": "16px",
      "lg": "18px",
      "xl": "20px",
      "2xl": "24px",
      "3xl": "30px",
      "4xl": "36px",
      "5xl": "48px"
    }
  },
  "borderRadius": {
    "lg": "8px",
    "xl": "12px",
    "2xl": "16px",
    "full": "9999px"
  }
}
```

---

## 20. Conclusion

This design system provides a complete foundation for building **MediNova AI** with:

✅ **Consistent Visual Language** - All components follow the same design patterns
✅ **Healthcare-Optimized** - Colors, typography, and layouts suited for medical context
✅ **Modern Aesthetic** - Glassmorphism creates a premium, contemporary feel
✅ **Fully Accessible** - WCAG compliant with proper contrast and focus states
✅ **Dark Mode Support** - Complete dark theme implementation
✅ **Developer-Ready** - Tailwind CSS classes ready to use
✅ **Scalable** - Design tokens and patterns can be extended

**Next Steps:**
1. Implement design system in React components
2. Create Storybook documentation for all components
3. Build design system library/package
4. Create Figma design file based on this system
5. Conduct accessibility audit
6. Test with real users (patients and doctors)

---

**Design System Version:** 1.0  
**Last Updated:** July 2, 2026  
**Status:** ✅ Complete and Ready for Implementation

---

**End of Design System Document**
