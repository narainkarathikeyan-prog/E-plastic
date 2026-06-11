# 🌱 EcoChain — E-Plastic Management & Data Mining Platform

A full-stack Django web application for managing e-plastic waste collection, 
processing, and data mining analytics.

---

## 🚀 Quick Setup

### 1. Install Python & Django
```bash
pip install -r requirements.txt
```

### 2. Run Database Migrations
```bash
python manage.py makemigrations eplastic
python manage.py migrate
```

### 3. Create Admin User
```bash
python manage.py createsuperuser
```

### 4. Seed Sample Data
```bash
python manage.py seed_data
```

### 5. Run Development Server
```bash
python manage.py runserver
```

Open: http://127.0.0.1:8000

---

## 📁 Project Structure

```
eplastic_project/
├── eplastic_project/
│   ├── settings.py         # Django settings
│   ├── urls.py             # Root URL config
│   └── wsgi.py
│
├── eplastic/               # Main app
│   ├── models.py           # Database models
│   ├── views.py            # Page & API views
│   ├── urls.py             # App URL patterns
│   ├── admin.py            # Admin panel config
│   └── management/
│       └── commands/
│           └── seed_data.py  # Demo data seeder
│
├── templates/              # HTML templates
│   ├── base.html           # Layout with nav/footer
│   ├── index.html          # Homepage
│   ├── submit.html         # Waste submission form
│   ├── dashboard.html      # Analytics dashboard
│   ├── centers.html        # Collection centers
│   ├── reports.html        # Data mining reports
│   └── track.html          # Submission tracker
│
├── static/
│   ├── css/main.css        # Full stylesheet
│   └── js/main.js          # Frontend JS
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🌐 Pages & Features

| URL | Page | Features |
|-----|------|----------|
| `/` | Homepage | Hero, stats, plastic guide, how-it-works |
| `/submit/` | Submit Waste | Registration form, green points calculator |
| `/dashboard/` | Analytics | Charts, KPIs, live data mining results |
| `/centers/` | Centers Map | All collection centers with details |
| `/reports/` | Reports | Data mining techniques & generated reports |
| `/track/` | Track | Submission status tracker with progress bar |
| `/admin/` | Django Admin | Full data management |
| `/api/stats/` | API | JSON stats for AJAX dashboard |
| `/api/centers/` | API | JSON list of centers |
| `/api/submit/` | API | POST endpoint for submissions |
| `/api/mining/` | API | JSON data mining insights |

---

## 🗃️ Database Models

- **PlasticType** — 7 plastic categories (PET, HDPE, PVC, etc.)
- **CollectionCenter** — Physical drop-off locations with geo coordinates
- **WasteSubmission** — Individual plastic waste submissions with status tracking
- **RecyclingData** — Monthly aggregated recycling statistics
- **DataMiningReport** — AI-generated analytical insights

---

## 🔬 Data Mining Features

- **Pattern Recognition** — Most common plastic types and submission patterns
- **Geographic Clustering** — City-level collection heat maps
- **Trend Analysis** — Monthly waste collection trends
- **Efficiency Metrics** — Recycling rate calculations
- **Predictive Insights** — Forecast models for capacity planning
- **Association Rules** — Co-occurring plastic type behaviors

---

## 🎨 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.x + Django 4.x |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Frontend | HTML5 + CSS3 + Vanilla JS |
| Charts | Chart.js 4.x |
| Fonts | Google Fonts (Syne + DM Sans) |
| Admin | Django Admin |

---

## ♻ Environmental Impact Calculations

- **CO₂ Saved**: 2.5 kg CO₂ per kg plastic recycled
- **Energy Saved**: 5.8 kWh per kg plastic recycled
- **Trees Equivalent**: 0.1 tree per kg plastic recycled
- **Green Points**: 10 points per kg submitted

---

Built with 💚 for a sustainable future.
