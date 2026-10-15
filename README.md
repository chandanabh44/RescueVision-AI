# RescueVision AI
### AI-Powered Disaster Detection, Early Warning & Emergency Response System

> **A Humanitarian Disaster Intelligence Platform built for Hackathons & Emergency Preparedness.**  
> Delivering verified real-time disaster alerts, community incident crowdsourcing, computer vision hazard classification, bilingual accessibility (English & Kannada), and offline-resilient survival guidance.

---

## 📑 Table of Contents
1. [Overview & Key Objectives](#1-overview--key-objectives)
2. [Disaster Categories & Data Transparency](#2-disaster-categories--data-transparency)
3. [Technology Stack](#3-technology-stack)
4. [Project File Structure](#4-project-file-structure)
5. [Prerequisites & System Setup](#5-prerequisites--system-setup)
6. [Database Setup & Seeding](#6-database-setup--seeding)
7. [Running the Application](#7-running-the-application)
8. [Automated Testing](#8-automated-testing)
9. [AI Assistant & Vision Configuration](#9-ai-assistant--vision-configuration)
10. [Authoritative Data Sources](#10-authoritative-data-sources)
11. [Kaggle Dataset Preparation Pipeline](#11-kaggle-dataset-preparation-pipeline)
12. [Offline Mode & PWA Operation](#12-offline-mode--pwa-operation)
13. [Local Network & Public Cloud Deployment](#13-local-network--public-cloud-deployment)
14. [Coordinator / Admin Review Portal](#14-coordinator--admin-review-portal)
15. [Judge Demonstration Checklist](#15-judge-demonstration-checklist)

---

## 1. Overview & Key Objectives
When catastrophic disasters strike, immediate access to verified emergency instructions and ground-truth situational reports is critical.

**RescueVision AI** solves this through a multi-tiered emergency system:
- **Authoritative Aggregation:** Ingests live telemetry from official global agencies (USGS Earthquake Hazards, NASA EONET, Open-Meteo).
- **Civilian Crowdsourcing:** Enables citizens to submit geo-tagged incident reports with photographs and GPS coordinates.
- **Strict Verification Workflow:** Citizen reports enter an isolated review queue and are never marked as verified alerts until cleared by authorized emergency coordinators.
- **Offline Resilience:** Functions even when cellular networks fail via Service Worker caching, local IndexedDB draft queuing, and offline survival guides.
- **AI Safety Assistant:** Offers conversational survival guidance (Floods, Earthquakes, Wildfires, Landslides) with strict life-safety guardrails.

---

## 2. Disaster Categories & Data Transparency

The system monitors **four core disaster categories**:
1. **Floods (🌊):** Hydrological inundation, river surges, urban waterlogging.
2. **Earthquakes (🌋):** Seismic ground motion, magnitude grading, aftershock warnings.
3. **Wildfires (🔥):** Forest thermal anomalies, smoke plumes, defensible perimeter buffers.
4. **Landslides (⛰️):** Slope failures, debris flows, rainfall-triggered mudflows.

### Data Origin Classification (Strict Integrity Protocol)
To ensure complete transparency and prevent false alarms, every record is labeled with its exact data origin:
- **Official Verified:** Live telemetry directly fetched from authoritative agencies (USGS, NASA EONET).
- **User Incident Report:** Citizen-submitted reports; private reporter identity is shielded from public view.
- **DEMO DATA (Simulation):** Clearly badged sample drill records created for hackathon demonstration.
- **Historical Dataset:** Reference benchmarks from Kaggle datasets.

---

## 3. Technology Stack

- **Backend:** Python 3.10+, Flask 3.1, Flask-SQLAlchemy 3.1
- **WSGI Production Server:** Waitress (Windows & Linux native multi-threaded server)
- **Database:** SQLite 3 (Default local database) with full PostgreSQL schema compatibility
- **Frontend:** Semantic HTML5, Vanilla CSS3 (Custom Dark Navy & Obsidian design system with responsive tokens), JavaScript (ES6+)
- **Mapping:** Leaflet 1.9 with OpenStreetMap basemap & custom disaster SVG marker pins
- **Analytics:** Chart.js 4.4 (Donut category distributions and severity bar charts)
- **PWA & Offline:** Service Worker (`sw.js`), Web App Manifest (`manifest.json`), IndexedDB / LocalStorage
- **Image Processing:** Pillow (PIL) header verification and secure UUID file handling
- **AI / LLM:** Configurable provider architecture (Google Gemini, OpenAI, or Built-in Emergency Knowledge Base)
- **Internationalization (i18n):** English and Kannada (ಕನ್ನಡ) bilingual toggle

---

## 4. Project File Structure

```
prj2/
├── .env                  # Local environment configuration
├── .env.example          # Template environment file (safe defaults)
├── .gitignore            # Git exclusion rules
├── requirements.txt      # Python dependencies
├── config.py             # App & Test configuration
├── app.py                # Flask application factory
├── wsgi.py               # Waitress production WSGI server
├── models.py             # SQLAlchemy models (Incidents, Alerts, Sources, Audit)
├── routes/
│   ├── __init__.py
│   ├── main_routes.py    # Landing, Dashboard, Map, Alerts, Guide, About
│   ├── incident_routes.py# Report form, public history, JSON APIs
│   ├── ai_routes.py      # AI assistant & image classification endpoints
│   ├── admin_routes.py   # Coordinator review queue, status verification
│   └── api_routes.py     # Live stats, health check, offline sync bundle
├── services/
│   ├── __init__.py
│   ├── external_data_service.py # Real USGS & NASA EONET APIs
│   ├── ai_service.py            # Gemini/OpenAI/Offline Knowledge provider
│   ├── image_analysis_service.py# Vision heuristic classifier & pluggable model
│   └── sync_service.py          # Offline draft queue reconciliation
├── static/
│   ├── css/
│   │   └── styles.css    # Premium dark-navy design system
│   ├── js/
│   │   ├── main.js       # PWA worker, network monitor, notifications
│   │   ├── dashboard.js  # Chart.js metrics & live counters
│   │   ├── map.js        # Leaflet interactive map with custom pins
│   │   ├── report.js     # Form validation, GPS capture, offline saving
│   │   ├── assistant.js  # AI chat interface & typing animations
│   │   ├── image_analysis.js # Drag-and-drop photo inspection
│   │   ├── offline_manager.js# LocalStorage queue & sync engine
│   │   └── i18n.js       # Bilingual English & Kannada engine
│   ├── images/
│   │   └── logo.svg      # Vector SVG logo
│   ├── manifest.json     # PWA manifest
│   └── sw.js             # Service Worker offline cache
├── templates/
│   ├── base.html         # Master layout & responsive navigation
│   ├── index.html        # Landing page & data origin hierarchy
│   ├── dashboard.html    # KPI cards, charts, and data source health
│   ├── map.html          # Interactive disaster map & coordinate display
│   ├── alerts.html       # Official live alerts table
│   ├── report.html       # Incident submission form
│   ├── assistant.html    # AI Disaster Assistant chatbot
│   ├── image_analysis.html# Disaster photo analysis
│   ├── safety_guide.html # 4-Category survival guides + 72-hour Go-Bag
│   ├── incident_history.html # Public records archive
│   ├── admin_login.html  # Coordinator login
│   ├── admin.html        # Review queue & verification portal
│   ├── about.html        # System architecture & Kaggle datasets
│   ├── offline.html      # Disconnected offline fallback
│   ├── 404.html          # Resource not found error
│   └── 500.html          # Internal server error
├── data/
│   ├── DATASETS.md       # Kaggle dataset catalog & licenses
│   └── sample_demo_data.json # Badged demo disaster records
├── scripts/
│   ├── prepare_dataset.py# Dataset validation & train/val/test splitter
│   └── seed_demo_data.py # Seeder script for initial demo & live feeds
├── tests/
│   ├── conftest.py       # Isolated in-memory SQLite fixtures
│   ├── test_routes.py    # Route & endpoint tests
│   ├── test_incidents.py # Validation & privacy tests
│   ├── test_ai_service.py# AI fallback & prompt tests
│   ├── test_image_analysis.py # Image upload & security tests
│   ├── test_offline_sync.py # Offline queue & duplicate prevention tests
│   └── test_external_data.py# Official alert & deduplication tests
├── instance/             # Local SQLite database (gitignored)
└── uploads/              # Validated user photo uploads (gitignored)
```

---

## 5. Prerequisites & System Setup

### Requirements
- **OS:** Windows 10/11, macOS, or Linux
- **Python:** Version 3.10, 3.11, 3.12, 3.13, or 3.14

### Installation (Windows Commands)
Open PowerShell or Command Prompt in the project folder (`c:\Users\keert\prj2`):

```powershell
# 1. Create a Python virtual environment
python -m venv venv

# 2. Activate the virtual environment
# In PowerShell:
.\venv\Scripts\Activate.ps1
# (Or in Command Prompt cmd.exe):
.\venv\Scripts\activate.bat

# 3. Upgrade pip and install dependencies
pip install -r requirements.txt
```

---

## 6. Database Setup & Seeding

The application creates all database tables automatically on first startup.

To populate the database with clearly badged **demonstration incidents** and immediately pull the latest **live events from USGS and NASA EONET**:

```powershell
python scripts/seed_demo_data.py
```

Output:
```
============================================================
RescueVision AI - Database Initialization & Seeding
============================================================
✓ Database tables verified.
✓ Seeded 4 demonstration incidents (Explicitly marked DEMO DATA).
Fetching authoritative live feeds (USGS Earthquake & NASA EONET)...
✓ USGS Earthquake sync: success (20 events)
✓ NASA EONET sync: success (24 events)
============================================================
```

---

## 7. Running the Application

### Development Server
```powershell
python app.py
```
Open your browser and navigate to:  
👉 **`http://127.0.0.1:5000`**

### Production WSGI Server (Waitress)
For production-grade multi-threading:
```powershell
python wsgi.py
```

---

## 8. Automated Testing

RescueVision AI includes a comprehensive automated test suite with **28 tests** covering input validation, route rendering, security boundaries, and offline sync. Tests run against an isolated **in-memory SQLite database** (`sqlite:///:memory:`) so real data is never touched or corrupted.

Run all tests:
```powershell
python -m pytest tests/ -v
```

Expected result:
```
============================= 28 passed in 0.85s ==============================
```

---

## 9. AI Assistant & Vision Configuration

### AI Assistant (LLM Integration)
Configure your desired provider in `.env`:
```env
# Options: demo_fallback, gemini, openai
AI_PROVIDER=demo_fallback

# To connect Google Gemini (Get free key from https://aistudio.google.com/):
GEMINI_API_KEY=your_gemini_api_key_here
```
- **Zero-Cost Mode:** If no API key is provided, the assistant uses the built-in **RescueVision Emergency Knowledge Base**, answering questions on flood evacuation, earthquake Drop/Cover/Hold On, wildfire defensible space, landslide signs, and 72-hour survival kits.
- **Safety Guardrails:** Always displays a clear disclaimer reminding users that AI advice does not replace 911 / 112 emergency services.

### Computer Vision & Image Classification
- Users can upload disaster photos (`.jpg`, `.png`, `.webp` up to 10MB).
- **Heuristic Demo Engine:** Default out-of-the-box mode analyzes visual spectrum patterns and clearly displays: `[DEMO MODE - NOT A TRAINED PRODUCTION MODEL]`.
- **Trained Deep Learning Plug-in:** To deploy a real CNN model (ResNet, EfficientNet), export weights to `models/disaster_classifier.pth`. The service will automatically detect the model file and switch to neural inference!

---

## 10. Authoritative Data Sources

The platform integrates directly with public, free APIs without requiring paid keys:
1. **USGS Earthquake Hazards API:**  
   `https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson`  
   Real-time seismic events filtered by magnitude.
2. **NASA Earth Observatory Natural Event Tracker (EONET v3):**  
   `https://eonet.gsfc.nasa.gov/api/v3/events`  
   Monitors active wildfires, severe storms, floods, and landslides globally.
3. **Open-Meteo Hydrology & Weather:**  
   `https://flood-api.open-meteo.com/v1/flood`  
   Severe rainfall and river discharge forecasts.

**Offline Cache:** If internet access fails, previously synced records are served from SQLite with an archive timestamp to prevent presenting old data as new alerts.

---

## 11. Kaggle Dataset Preparation Pipeline

A dataset validation and splitting script is located in `scripts/prepare_dataset.py`.

```powershell
# Validate and generate train/val/test splits:
python scripts/prepare_dataset.py --data-dir path/to/dataset --output-dir data/processed --split-ratio 0.7,0.15,0.15
```

The script:
- Verifies image integrity using Pillow (`verify()`).
- Detects duplicate files using cryptographic MD5 content hashing.
- Checks class balance.
- Outputs reproducible splits without data leakage.

Refer to [`data/DATASETS.md`](data/DATASETS.md) for full dataset references and licenses.

---

## 12. Offline Mode & PWA Operation

RescueVision AI is designed for communication-denied environments:
1. **Service Worker:** Caches application shell, CSS, icons, and safety guides.
2. **Offline Indicator:** A network monitor detects internet loss and updates the topbar pill to **Offline Mode**.
3. **Local Draft Queue:** Reports submitted offline are stored in device storage (`localStorage`).
4. **Idempotent Background Sync:** When online connectivity resumes, pending reports automatically synchronize to `/api/sync` without creating duplicates.
5. **Interactive Map Fallback:** If map tiles cannot be downloaded, a clean message explains that basemap streaming requires internet and presents a tabular incident record view.

---

## 13. Local Network & Public Cloud Deployment

### Accessing over Local Wi-Fi (e.g. from a mobile phone)
1. Find your laptop's local IP address (`ipconfig` in Command Prompt, e.g. `192.168.1.15`).
2. Start the server with host `0.0.0.0`:
   ```powershell
   python wsgi.py
   ```
3. On your phone connected to the same Wi-Fi, open:  
   `http://192.168.1.15:5000`

### Public Cloud Deployment (e.g. Render, Railway, VPS)
1. **WSGI Server:** Use Waitress on Windows or Gunicorn on Linux (`gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app`).
2. **Environment Variables:** Set `SECRET_KEY`, `ADMIN_PASSWORD`, and optionally `GEMINI_API_KEY`.
3. **Database:** Set `DATABASE_URL` to a persistent PostgreSQL instance (e.g. `postgresql://user:pass@host/dbname`).
4. **Health Probe:** Point your hosting platform's health check to `/api/health`.

---

## 14. Coordinator / Admin Review Portal

- **URL:** `http://127.0.0.1:5000/admin`
- **Default Username:** `admin`
- **Default Password:** `RescueAdmin2026!` (Configured via `ADMIN_PASSWORD` in `.env`)

### Reviewer Features:
- View pending community incident reports.
- Inspect confidential reporter contact details (name and phone/email, hidden from public APIs).
- Update verification status:
  - `Verified by reviewer` (Marks incident as field-verified)
  - `Under Review`
  - `Rejected or resolved`
- Add reviewer verification notes and capture audit logs.
- Trigger manual synchronization of USGS and NASA feeds.

---

## 15. Judge Demonstration Checklist

Follow this sequence to present RescueVision AI during hackathon judging:

1. **Start on Landing Page (`/`):**
   - Show the dark-navy interface and the 4 disaster category cards (Floods, Earthquakes, Wildfires, Landslides).
   - Point out the **Data Origin Transparency** section explaining how real official alerts, community reports, and demo data are strictly segregated.
2. **Open Dashboard (`/dashboard`):**
   - Highlight the dynamic KPI counters computed directly from SQLite.
   - Show the Chart.js Donut chart for category breakdown and Bar chart for severity.
   - Show the **Authoritative Data Sources** health table tracking USGS and NASA EONET.
3. **Explore Interactive Map (`/map`):**
   - Show color-coded disaster pins (Cyan = Flood, Amber = Earthquake, Red = Wildfire, Brown = Landslide).
   - Filter by category and severity.
   - Click a marker to reveal incident popup details and GPS coordinates.
4. **Demonstrate Bilingual Toggle (`🌐 EN | ಕನ್ನಡ`):**
   - Click the language button in the topbar and watch the navigation and titles dynamically translate into **Kannada (ಕನ್ನಡ)**.
5. **Demonstrate AI Assistant (`/assistant`):**
   - Click the prompt button: *"What should I do during a flood?"*
   - Show the structured emergency protocols and safety disclaimer banner.
6. **Demonstrate Computer Vision (`/image-analysis`):**
   - Upload a sample disaster photo.
   - Show the heuristic visual inspection results and the honest **Demo Mode** limitation disclosure.
7. **Demonstrate Offline Resiliency:**
   - Go to **Report Incident (`/report`)**.
   - Click *"Capture GPS Location"* to autofill coordinates.
   - Disconnect Wi-Fi (or toggle Chrome DevTools Network to "Offline").
   - Notice the topbar pill change to **Offline Mode**.
   - Click *"Save Draft Offline"* and show that the report is saved safely on the device.
   - Reconnect internet and observe automatic background synchronization!
8. **Demonstrate Coordinator Portal (`/admin`):**
   - Log in with `admin` / `RescueAdmin2026!`.
   - Inspect the pending report, view confidential reporter contact info, approve the report, and view the audit log entry.
