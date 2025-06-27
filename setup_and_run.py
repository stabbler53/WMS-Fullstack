#!/usr/bin/env python3
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND = os.path.join(ROOT, 'backend')
FRONTEND = os.path.join(ROOT, 'frontend')

BOLD = '\033[1m'
ENDC = '\033[0m'


def run(cmd, cwd=None, shell=True, check=True):
    print(f'{BOLD}>>> {cmd}{ENDC}')
    return subprocess.run(cmd, cwd=cwd, shell=shell, check=check)


def check_docker():
    try:
        subprocess.run('docker --version', shell=True, check=True, stdout=subprocess.DEVNULL)
        subprocess.run('docker-compose --version', shell=True, check=True, stdout=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def backend_setup():
    print(f'{BOLD}\n[Backend Setup]{ENDC}')
    run('pip install -r requirements.txt', cwd=BACKEND)
    run('python manage.py migrate', cwd=BACKEND)
    run('python manage.py collectstatic --noinput', cwd=BACKEND)
    # Create superuser if not exists
    create_superuser_py = """
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Created default admin user: admin / admin123')
else:
    print('Admin user already exists')
"""
    run(f'echo "{create_superuser_py}" | python manage.py shell', cwd=BACKEND)


def frontend_setup():
    print(f'{BOLD}\n[Frontend Setup]{ENDC}')
    run('npm install', cwd=FRONTEND)


def start_with_docker():
    print(f'{BOLD}\n[Starting with Docker Compose]{ENDC}')
    run('docker-compose up --build', cwd=ROOT, check=False)


def start_local():
    print(f'{BOLD}\n[Starting Backend]{ENDC}')
    backend_proc = subprocess.Popen('python manage.py runserver', cwd=BACKEND, shell=True)
    print(f'{BOLD}\n[Starting Frontend]{ENDC}')
    frontend_proc = subprocess.Popen('npm start', cwd=FRONTEND, shell=True)
    print(f"\n{BOLD}Site is starting...{ENDC}")
    print("- Frontend: http://localhost:3000")
    print("- Backend:  http://localhost:8000")
    print("- Admin:    http://localhost:8000/admin/")
    print("\nDefault admin: admin / admin123")
    print("\nPress Ctrl+C to stop.")
    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        backend_proc.terminate()
        frontend_proc.terminate()


def main():
    print(f"{BOLD}WMS Fullstack Setup & Start Script{ENDC}")
    print("="*40)
    if check_docker():
        print("Docker & Docker Compose detected. Using Docker Compose for setup and run.")
        start_with_docker()
    else:
        print("Docker not found. Using local Python/Node setup.")
        backend_setup()
        frontend_setup()
        start_local()

if __name__ == '__main__':
    main() 