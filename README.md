# Warehouse Management System (WMS)

A full-stack warehouse management system for modern inventory, batch, and operations control. Built with Django (backend) and React (frontend).

---

## 🚀 Quick Start

### 1. Requirements
- Docker & Docker Compose (recommended)
- Python 3.11+
- Node.js 18+

### 2. One-Click Setup
Run this in your project root:
```bash
python setup_and_run.py
```

Or, with Docker Compose:
```bash
docker-compose up --build
```

### 3. Access the App
- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend/API: [http://localhost:8000](http://localhost:8000)
- Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 🗂️ Project Structure

```
WMS-Fullstack/
  backend/      # Django backend (API, admin, models, webhooks)
  frontend/     # React frontend (UI, dashboard, inventory)
  docker/       # Docker configs
  docker-compose.yml
  setup_and_run.py
  README.md     # (this file)
```

---

## 📦 Features
- Inventory, batch, and expiry tracking
- Role-based access (admin, manager, operator)
- Real-time webhooks & integration hooks
- CSV import/export
- Modern React dashboard
- REST API (JWT auth)

---

## 🛠️ Development
- See `backend/README.md` and `frontend/README.md` for details
- Use Docker for easiest setup
- For custom setup, run backend and frontend separately

---

## 👤 Default Admin Login
- Username: `admin`
- Password: `admin123` (or as set during setup)

---

## 📄 License
MIT 