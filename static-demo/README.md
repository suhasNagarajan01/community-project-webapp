# 🚀 College Project 10% Milestone Demo

This folder (`static-demo/`) contains the **standalone static presentation suite** prepared specifically for your **10% milestone project evaluation**.

It requires **no Python, no database setup, and no server**. You can double-click and open any file directly in Google Chrome, Microsoft Edge, or any modern web browser.

---

## 📋 What to Show During the Presentation

1. **Dual Theme System (Green/White vs. Brown/Beige)**:
   - Click the **"Theme"** dropdown in the top navbar on any screen to switch between **Emerald Green & Crisp White** (Default) and **Warm Earth & Soft Beige**.
   - Click the **Moon / Sun** icon to demonstrate viewport-wide **Dark Mode and Light Mode**.

2. **Dedicated Role-Based Authentication (`login.html` & `register.html`)**:
   - Open [login.html](file:///c:/Users/SUHAS/Documents/community-project-work/static-demo/login.html).
   - Show the smooth tab switch between **Worker Login** and **Contractor Login**.
   - Use the green/blue **"1-Click Demo Login"** buttons to instantly enter either role's dashboard.
   - Show [register.html](file:///c:/Users/SUHAS/Documents/community-project-work/static-demo/register.html) with trade-specific registration fields (expected daily wage, skills, languages, contractor company types).

3. **Worker Experience & Discovery (`worker-dashboard.html`)**:
   - Live search bar, category chips (Electrical, Plumbing, Painting, Construction, etc.).
   - Clean cards showing **Daily Wage Pills** (e.g. `₹900/day`), estimated distance (`2.1 km away`), duration, and employer rating.
   - Top-left **Hamburger Drawer Menu** and persistent mobile **Bottom Navigation Bar**.

4. **Digital Wallet System (`wallet.html`)**:
   - Shows **Available Balance** (`₹1,750.00`), **Lifetime Earnings** (`₹4,250.00`), and **Pending Clearance** (`₹900.00`).
   - Earnings ledger with daily wage credits from past assignments.
   - Interactive **"Withdraw to UPI / Bank"** modal simulating direct transfer to Google Pay / PhonePe (`9876543210@upi`).

5. **Contractor Experience & Worker Rankings (`contractor-dashboard.html`)**:
   - Workers ranked using the PRD formula:
     $$\text{Ranking Score} = (\text{Rating} \times 0.40) + (\text{Reliability} \times 0.30) + (\text{Attendance} \times 0.20) + (\text{Completed Jobs} \times 0.20)$$
   - Displays reliability % meters, attendance %, completed job counters, expected wages, and client ratings.
   - Bottom-right **Floating Action Button (`+`)** opening the Job Posting form ([post-job.html](file:///c:/Users/SUHAS/Documents/community-project-work/static-demo/post-job.html)).

6. **Worker Profile & Reviews (`profile.html`)**:
   - Profile photo, badge, skills chips, languages, daily wage, and verified employer reviews.

---

## 🖥️ How to Run

Simply double-click:
- **`static-demo/index.html`** or **`static-demo/login.html`**

Or serve statically using Python if preferred:
```bash
python -m http.server 3000 --directory static-demo
```
Then open: **`http://localhost:3000`**
