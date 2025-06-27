# WMS Backend (Django)

This is the backend for the Warehouse Management System. It provides the REST API, admin panel, batch/expiry tracking, webhooks, and business logic.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Migrate Database
```bash
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

### 4. Run the Server
```bash
python manage.py runserver
```

Or use Docker Compose:
```bash
docker-compose up backend
```

---

## 🛠️ Features
- JWT authentication
- Role-based permissions (admin, manager, operator)
- Inventory, batch, and expiry tracking
- FIFO outbound fulfillment
- Webhook & integration hooks
- CSV import/export
- Audit logging

---

## 📚 API Endpoints
- `/api/products/` - Product CRUD
- `/api/batches/` - Batch/expiry management
- `/api/inbound/` - Inbound stock
- `/api/outbound/` - Outbound stock
- `/api/webhooks/` - Webhook management
- `/api/webhook-deliveries/` - Webhook delivery logs
- `/api/users/me/` - Current user info

See the code for more endpoints and details.

---

## 🧪 Testing
```bash
python manage.py test
```

---

## 👤 Default Admin Login
- Username: `admin`
- Password: `admin123` (or as set during setup)

---

## 📄 License
MIT 