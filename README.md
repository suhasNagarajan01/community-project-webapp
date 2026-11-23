# RojgarSetu - Daily Wage Worker & Contractor Job Platform

A modern, production-oriented daily wage job marketplace built with **Django**, **HTMX**, **Bootstrap 5.3**, and **Custom CSS**. 

Designed specifically to eliminate income instability for local daily laborers (electricians, plumbers, masons, painters, housekeeping, security, and helpers) while giving contractors and households verified, rated skilled workers on short notice.

---

## 🎨 Dual Theme System (Green/White vs Brown/Beige)

To fulfill your exact aesthetic inquiry:
> *"follow green, white theme for web application, or brown, beige?"*

This platform provides **both** in a unified, switchable design system:

1. **Emerald Green & Crisp White (Default Theme)**
   - **Vibe**: High-contrast, clean, symbolizing growth, daily prosperity, approved assignments, and vitality.
   - **Colors**: Emerald `#059669`, `#10B981`, Mint `#34D399`, pristine white `#FFFFFF`, cool slate `#0F172A` / `#F8FAFC`.
2. **Warm Earth & Soft Beige (Alternative Theme)**
   - **Vibe**: Warm craft, artisan masonry, grounded clay/amber tones with gentle linen comfort.
   - **Colors**: Deep earth `#78350F`, warm amber `#92400E`, `#D97706`, creamy beige `#FEF3C7`, `#FFFDF7`.
3. **Dark / Light Mode**:
   - Both palettes adapt viewport-wide to system preferences and include manual 1-click toggles in the top navbar and settings page.
   - Follows modern web platform standards (`color-scheme: light dark;`, `light-dark()` tokens, and accessible WCAG contrast).

---

## 🚀 Key Features

### For Daily Wage Workers (Job Seekers)
- **Nearby Job Search & HTMX Filtering**: Search by trade, skill, locality, distance, or minimum wage without full page reloads.
- **Upfront Transparent Wages**: Each job card clearly highlights the daily wage offered (e.g. `₹850/day`), duration, and contractor rating.
- **Worker Digital Wallet**:
  - Lifetime verified earnings summary.
  - Pending employer clearances awaiting task sign-off.
  - Payment ledger and instant UPI withdrawal simulation (`9876543210@upi`).
- **Reputation & Ranking**: Track punctuality score, work quality, attendance %, and client reviews.
- **Mobile-First Bottom Navigation**: Persistent bar with Home, Wallet, Applied Jobs, Chat, and Profile.

### For Contractors & Employers (Hiring)
- **Smart Worker Rankings**: Worker cards ranked using a weighted formula:
  $$\text{Ranking Score} = (\text{Rating} \times 0.40) + (\text{Reliability} \times 0.30) + (\text{Attendance} \times 0.20) + (\text{Completed Jobs} \times 0.20)$$
- **Quick Job Posting**: Floating Action Button (`+`) allows broadcasting a job in under 60 seconds with required skills, pay, location, and workers needed.
- **Applicant Management**:
  - Accept & hire workers.
  - Mark work complete: automatically credits daily wage to the worker's wallet.
  - 4-factor review submission (Punctuality, Quality, Communication, Reliability).
- **Direct Communication**: One-tap phone dialer and interactive in-app chat.

---

## 🛠️ Technology Stack & Architecture

- **Backend**: Python 3, Django 6
- **Database**: 
  - SQLite (Default for instant zero-setup local execution)
  - PostgreSQL ready via `dj-database-url` (Automatic on Render/Production)
- **Frontend Interactivity**: HTMX (live search, filter updates, chat stream)
- **Styling**: Bootstrap 5.3 + Bootstrap Icons + Custom Modern CSS (`theme.css`)
- **Static Assets**: WhiteNoise (compressed static file serving)
- **Deployment**: Render-ready with `render.yaml` and `Procfile`

---

## ⚡ Quick Start & Running Locally

### 1. Activate Virtual Environment
```bash
# Windows
.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate
```

### 2. Run Database Migrations
```bash
python manage.py migrate
```

### 3. Seed Realistic Sample Data
Populates 8 verified workers, 4 contractors, 8 open jobs across Bengaluru localities, wallet ledger records, and reviews:
```bash
python manage.py seed_data
```

### 4. Start Development Server
```bash
python manage.py runserver
```
Visit: **`http://127.0.0.1:8000/`**

---

## 🔑 Pre-seeded Demo Accounts

For instant testing and evaluation without manual signup:

| Role | Username | Password | Notes |
|---|---|---|---|
| **Admin** | `admin` | `admin123` | Django Admin at `/admin/` |
| **Worker (Electrician)** | `ramesh_kumar` | `worker123` | Top-rated electrician (4.94★), wallet balance & jobs |
| **Worker (Plumber)** | `manjunath_plumber` | `worker123` | Plumbing & tank cleaning (4.89★) |
| **Worker (Painter)** | `sunil_verma` | `worker123` | Putty & roller specialist (4.82★) |
| **Contractor (Construction)** | `buildwell_infra` | `contractor123` | Rajesh Sharma, BuildWell Infrastructure |
| **Contractor (Renovations)**| `prestige_homes` | `contractor123` | Suresh Reddy, Prestige Home Renovations |

> **Pro Tip**: The Login page includes 1-click **"Quick Demo Login"** buttons for both Worker and Contractor roles!

---

## 🧪 Running Automated Tests

A test suite verifying ranking algorithms, application flows, wallet payouts, and theme endpoints is included:
```bash
python manage.py test jobs
```
*(Runs and verifies all model and view flows with 100% pass rate)*.
