# WMS Backend (Django)

## Overview
Production-grade Warehouse Management System backend built with Django & DRF. Supports inventory, inbound, outbound, user/role management, audit logs, bulk upload, and more.

## Features
- Inventory, inbound, outbound management
- User roles: Admin, Manager, Operator
- Audit logs, dashboard, low stock alerts
- Bulk CSV upload, file attachments
- JWT authentication
- PostgreSQL database
- Dockerized for production
- Swagger/OpenAPI docs

## Setup
1. Clone the repo and `cd backend`
2. Create a `.env` file (see below)
3. Build and run with Docker Compose:
   ```sh
   docker-compose up --build
   ```

## Environment Variables (`.env` example)
```
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=wms_db
POSTGRES_USER=wms_user
POSTGRES_PASSWORD=wms_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

## Database Migration
```sh
docker-compose exec backend python manage.py migrate
```

## Superuser Creation
```sh
docker-compose exec backend python manage.py createsuperuser
```

## API Usage
- Obtain JWT: `POST /api/token/` (username, password)
- Refresh JWT: `POST /api/token/refresh/`
- Core endpoints: `/api/products/`, `/api/inbound/`, `/api/outbound/`, `/api/suppliers/`, `/api/customers/`
- Bulk upload: `POST /api/upload-csv/` (file, type)
- Stock reconciliation: `POST /api/reconcile-stock/`
- Dashboard: `/api/dashboard/`

## API Documentation
- Swagger: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- Redoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

## Media & File Uploads
- Uploaded files (invoices, delivery notes) are stored in `/media/`

## Testing
```sh
docker-compose exec backend python manage.py test
```

## Deployment
- Use Docker Compose for local/prod
- Set `DJANGO_DEBUG=False` and configure `ALLOWED_HOSTS` for production
- Use Nginx as a reverse proxy (see docker/ for example configs)

## License
MIT 