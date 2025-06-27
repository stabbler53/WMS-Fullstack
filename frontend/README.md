# WMS Frontend (React + Tailwind)

## Overview
Modern, responsive frontend for the Warehouse Management System. Built with React, Tailwind CSS, and Recharts. Supports inventory, inbound, outbound, dashboard, user roles, and more.

## Features
- JWT authentication (login)
- Role-based access (Admin, Manager, Operator)
- Inventory, inbound, outbound management
- Dashboard with charts, stats, and audit logs
- Bulk CSV upload (admin only)
- File attachments for inbound/outbound
- Responsive Tailwind UI
- Toast notifications for feedback

## Setup
1. `cd frontend`
2. Install dependencies:
   ```sh
   npm install
   ```
3. Create a `.env` file (see below)
4. Start the app:
   ```sh
   npm start
   ```

## Environment Variables (`.env` example)
```
REACT_APP_API_BASE_URL=http://localhost:8000/api/
```
- Make sure this matches your backend API URL.

## API Usage
- All API calls are made to `${REACT_APP_API_BASE_URL}` (see `src/services/api.js`).
- Login: `/token/` (POST, username & password)
- Inventory: `/products/`
- Inbound: `/inbound/`
- Outbound: `/outbound/`
- Dashboard: `/dashboard/`
- Bulk upload: `/upload-csv/`

## Scripts
- `npm start` — Run in development mode
- `npm run build` — Build for production
- `npm test` — Run tests

## Best Practices
- Uses Tailwind for all styling (see `tailwind.config.js`)
- Responsive and mobile-friendly layouts
- Role-based route protection (`ProtectedRoute`, `RequireAdmin`)
- Toast notifications for all user actions
- Error and loading states handled in all pages

## Deployment
- Build with `npm run build` and serve with any static file server
- For Docker, see the provided `Dockerfile`

## License
MIT
