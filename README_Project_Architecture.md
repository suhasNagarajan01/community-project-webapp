# College Project Technical Stack & Architecture Rules

## Core Philosophy

This project should be:

- Production-oriented rather than a simple academic prototype.
- Primarily Python-based.
- Easily deployable from GitHub.
- Maintainable by a student team.
- Scalable enough to demonstrate real-world software engineering practices.
- Visually modern without requiring expertise in JavaScript frameworks.

### Key Constraint

Preferred:
- Python

Avoid where possible:
- React
- Angular
- Vue
- Large JavaScript ecosystems

---

## Final Recommended Technology Stack

### Backend
**Django**

Reasons:
- Mature ecosystem
- Built-in authentication
- ORM included
- Admin panel included
- Security features included
- Huge community support
- Production-proven

### Database

#### Preferred: PostgreSQL

Why:
- Industry standard
- Excellent Django support
- Advanced querying capabilities
- Better scalability

#### Alternative: MySQL

Acceptable when:
- Team already has MySQL experience
- College curriculum uses MySQL

#### Conditional: MongoDB

Use MongoDB only when the project heavily depends on:
- Chat systems
- Message storage
- Flexible user-generated content
- Dynamic JSON-like documents

Possible architecture:

```text
Primary Data
    ↓
PostgreSQL

Chat Features
    ↓
MongoDB
```

---

## Frontend Strategy

### Django Templates

Frontend stack:

```text
Django Templates
HTML
CSS
```

Benefits:
- Simple
- Reliable
- Python-friendly
- Easy maintenance

---

## UI Enhancement Layer

### HTMX

Purpose:
- Dynamic content updates
- Search without page reload
- Live filtering
- Form submissions
- Partial page refreshes
- Modal interactions

HTMX provides modern interactivity without React.

---

## Styling Strategy

### Recommended

```text
Bootstrap
+
Custom CSS
```

Benefits:
- Fast development
- Modern responsive UI
- Large component library
- Easy for beginners

### Tailwind CSS

Optional.

Use Tailwind only if the team is comfortable learning it.

Otherwise Bootstrap + Custom CSS is completely sufficient.

---

## Design Guidelines

### Color System

Primary Accent:

```text
#FF6B35
#FF7B00
#FF9500
#FFB700
```

Supporting Colors:

```text
#0F172A
#F8FAFC
#FFFFFF
```

### Gradient Example

```css
background: linear-gradient(
135deg,
#ff7b00,
#ff9500,
#ffb700
);
```

---

## Modern UI Features Required

- Gradient backgrounds
- Glassmorphism
- Dark mode
- Hover effects
- Dashboard layouts
- Responsive design
- Animated cards
- Smooth transitions
- Sidebar navigation
- Search functionality
- Notifications

---

## Animation Guidelines

Allowed:
- Fade In
- Slide Up
- Hover Glow
- Card Lift Effect
- Loading Indicators

Avoid:
- Excessive animations
- Distracting transitions
- Constantly moving backgrounds

---

## Authentication Requirements

Use Django authentication.

Required:
- Login
- Logout
- Registration
- Password reset
- User roles

Example roles:
- Admin
- Faculty
- Student
- Moderator

---

## Chat System Considerations

Potential uses:
- Student support
- Internal communication
- AI assistant integration

Database recommendation:

```text
PostgreSQL
or
PostgreSQL + MongoDB
```

depending on scale.

---

## Deployment Rules

### GitHub

Source of truth.

Recommended branches:

```text
main
dev
feature/*
```

### Render

Deployment pipeline:

```text
GitHub
  ↓
Render
  ↓
Automatic Deployment
```

Every push to GitHub can trigger a redeployment.

---

## Recommended Project Structure

```text
project/
│
├── accounts/
├── chat/
├── dashboard/
├── reports/
├── notifications/
│
├── templates/
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│
├── media/
│
├── project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── requirements.txt
├── manage.py
└── README.md
```

---

## Final Approved Stack

```text
Backend
--------
Django

Database
--------
PostgreSQL

Optional Database
--------
MongoDB (Chat Features)

Frontend
--------
Django Templates

UI Enhancement
--------
HTMX

Styling
--------
Bootstrap
Custom CSS

Deployment
--------
GitHub
Render

Version Control
--------
Git
GitHub
```

---

## AI UI Generation Prompt

Create a modern SaaS-style web interface for a Django + HTMX application. Use an orange-gradient design system with glassmorphism elements, responsive layouts, rounded cards, subtle animations, dashboard-style navigation, dark/light mode support, modern typography, and Bootstrap-compatible components. The design should feel similar to Linear, Notion, Stripe Dashboard, or modern startup SaaS products while remaining easy to implement using Django templates, HTMX, Bootstrap, and custom CSS without requiring React or heavy JavaScript frameworks.

---

## Final Decision

The officially recommended stack is:

```text
Django
+
PostgreSQL
+
HTMX
+
Bootstrap
+
Custom CSS
+
GitHub
+
Render
```

MongoDB should only be added if chat functionality grows beyond simple message storage requirements.
