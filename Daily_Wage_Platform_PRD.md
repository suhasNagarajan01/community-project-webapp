# Daily Wage Worker Job Platform - Product Requirements & Architecture Document

## Project Overview

We are building a local daily-wage job marketplace focused on connecting workers and contractors within a city or locality.

Unlike LinkedIn, Naukri, or Indeed, this platform is specifically designed for:

- Daily wage workers
- Temporary workers
- Skilled and unskilled laborers
- Housekeeping staff
- Security guards
- Helpers
- Electricians
- Plumbers
- Painters
- Construction workers
- Delivery helpers
- Cleaning staff
- General labor workers

The goal is to help workers find short-term employment opportunities and allow contractors, households, businesses, and individuals to quickly hire workers for temporary jobs.

---

# Problem Statement

Many daily wage workers struggle because:

- Jobs are not available every day.
- Work opportunities are found through word-of-mouth.
- Lack of visibility causes income instability.
- Contractors cannot easily find qualified workers at short notice.

Example:

A worker may earn money on Monday but receive no work on Tuesday, causing complete income loss for that day.

This platform aims to reduce these gaps by creating a digital marketplace specifically for local daily wage opportunities.

---

# User Types

## Worker (Job Seeker)

Goals:
- Find nearby jobs
- View wages before applying
- Receive work quickly
- Build reputation through ratings
- Track earnings

## Contractor (Employer)

Goals:
- Find reliable workers
- Post temporary jobs easily
- Hire workers quickly
- Compare worker ratings
- View reviews before hiring

---

# Authentication System

At application startup users choose:

1. Worker Login
2. Contractor Login

Each role receives a dedicated experience tailored to their needs.

---

# Worker Dashboard Requirements

## Home Screen

Features:
- Job search bar
- Nearby job recommendations
- Skill-based filtering
- Location filtering
- Keyword search

## Job Card Information

Each card should show:
- Job title
- Wage offered
- Location
- Duration
- Contractor rating
- Estimated distance

## Bottom Navigation

### Home
Displays available jobs.

### Wallet
Displays:
- Total earnings
- Previous jobs
- Payment history
- Pending payments

## Profile Section

Located on the top-right.

Displays:
- Profile photo
- Name
- Rating
- Languages known
- Skills
- Expected daily wage
- Experience

## Hamburger Menu

Located on the top-left.

Contains:
- About Us
- Contact Us
- Settings
- Logout (bottom positioned)

---

# Contractor Dashboard Requirements

## Home Screen

Displays worker profiles instead of jobs.

## Worker Cards

Each worker card should display:
- Photo
- Name
- Rating
- Skills
- Languages
- Expected daily wage

## Worker Ranking Logic

Workers are ranked based on:
- Ratings
- Reviews
- Reliability score
- Attendance score
- Completed jobs

## Worker Profile Details

Displays:
- Personal information
- Languages known
- Skills
- Reviews
- Rating score
- Expected wage
- Experience

---

# Job Posting System

Contractors have a floating '+' button.

Job form fields:
- Job title
- Description
- Required skill
- Location
- Duration
- Pay offered
- Number of workers required
- Contact details

---

# Ratings & Review System

## Worker Rating

Contractors can rate workers based on:
- Punctuality
- Work quality
- Communication
- Reliability

## Contractor Rating

Workers can rate contractors based on:
- Timely payment
- Professional behavior
- Job accuracy
- Safety conditions

---

# Design & UI Guidelines

## Design Language

Modern SaaS-inspired interface.

Inspiration:
- Uber
- Rapido
- Swiggy
- Airbnb
- Stripe Dashboard
- Notion

## Colors

Primary Orange Palette:
- #FF6B35
- #FF7B00
- #FF9500
- #FFB700

Secondary Colors:
- #0F172A
- #F8FAFC
- #FFFFFF

## UI Features

Required:
- Gradient backgrounds
- Glassmorphism cards
- Rounded corners
- Responsive layouts
- Dark mode support
- Subtle animations
- Dashboard cards
- Bottom navigation
- Modern typography

## Animation Rules

Allowed:
- Fade in
- Slide up
- Card lift effects
- Hover animations
- Loading indicators

Avoid:
- Distracting motion
- Excessive animations

---

# Chat System

Future enhancement:
- Worker-to-contractor chat
- AI assistant integration
- Job discussions

Database strategy:
- PostgreSQL initially
- MongoDB optionally for advanced chat scalability

---

# Recommended Technical Stack

## Backend
- Django

## Database
- PostgreSQL (Primary)
- MySQL (Alternative)
- MongoDB (Optional for chat)

## Frontend
- Django Templates
- HTML
- CSS

## Dynamic UI Layer
- HTMX

## Styling
- Bootstrap
- Custom CSS

## Deployment
- GitHub
- Render

## Version Control
- Git
- GitHub

---

# Recommended Project Structure

```text
project/
├── accounts/
├── chat/
├── dashboard/
├── reports/
├── notifications/
├── templates/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── media/
├── project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── requirements.txt
├── manage.py
└── README.md
```

---

# AI UI Design Prompt

Create a mobile-first daily wage job marketplace application connecting workers and contractors. Use a modern SaaS-inspired design with orange gradient branding, green success colors, glassmorphism cards, rounded components, subtle animations, modern typography, responsive layouts, worker and contractor dashboards, rating systems, search functionality, wallet tracking, profile pages, floating action buttons, and bottom navigation suitable for Django Templates, HTMX, Bootstrap, and custom CSS. The interface should prioritize accessibility, trust, simplicity, and quick job discovery for daily wage workers while maintaining a professional experience for contractors.
