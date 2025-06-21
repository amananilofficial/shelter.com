@echo off
REM Automated User Setup Script for Shelter.com
REM This script sets up all users, roles, and sample data

echo Starting Shelter.com User Setup...
echo ==================================
echo.

REM Check if manage.py exists
if not exist "manage.py" (
    echo Error: manage.py not found. Make sure you're in the project root directory.
    pause
    exit /b 1
)

REM Run migrations first
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Check if --reset flag is provided
if "%1"=="--reset" (
    echo Resetting all data and creating fresh users...
    python manage.py setup_users --reset
) else (
    echo Creating users and sample data...
    python manage.py setup_users
)

echo.
echo Setup completed successfully!
echo.
echo USER CREDENTIALS:
echo ==================
echo.
echo SUPERUSER:
echo Username: admin ^| Password: admin123 ^| Email: admin@shelter.com
echo.
echo SHELTER APP:
echo Username: shelter_manager ^| Password: shelter123 ^| Role: Manager
echo Username: shelter_employee ^| Password: shelter123 ^| Role: Employee
echo.
echo AGENTS APP:
echo Username: agent_admin ^| Password: agent123 ^| Role: Admin
echo Username: agent_manager ^| Password: agent123 ^| Role: Manager
echo Username: agent_1 ^| Password: agent123 ^| Role: Agent
echo Username: agent_2 ^| Password: agent123 ^| Role: Agent
echo.
echo TEAM APP:
echo Username: team_admin ^| Password: team123 ^| Role: Admin
echo Username: team_manager ^| Password: team123 ^| Role: Manager
echo Username: team_member_1 ^| Password: team123 ^| Role: Member
echo Username: team_member_2 ^| Password: team123 ^| Role: Member
echo.
echo CRM APP:
echo Username: crm_admin ^| Password: crm123 ^| Role: Admin
echo Username: crm_manager ^| Password: crm123 ^| Role: Manager
echo Username: crm_employee_1 ^| Password: crm123 ^| Role: Employee
echo Username: crm_employee_2 ^| Password: crm123 ^| Role: Employee
echo.
echo MARKETING APP:
echo Username: marketing_admin ^| Password: marketing123 ^| Role: Admin
echo Username: marketing_manager ^| Password: marketing123 ^| Role: Manager
echo Username: marketing_employee ^| Password: marketing123 ^| Role: Employee
echo.
echo To start the development server:
echo python manage.py runserver
echo.
echo Access admin panel at: http://127.0.0.1:8000/admin/
echo.
pause