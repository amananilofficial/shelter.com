#!/usr/bin/env python
"""
Quick Setup Script for Shelter.com User Management
This script provides an easy way to set up all users and sample data.
"""

import os
import sys
import subprocess

def run_command(command):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {command}")
            return True
        else:
            print(f"✗ {command}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ {command}")
        print(f"Error: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("Shelter.com Automated User Setup")
    print("=" * 60)
    print()
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found!")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check for reset flag
    reset_mode = '--reset' in sys.argv
    
    if reset_mode:
        print("🔄 Running in RESET mode - all existing data will be removed!")
        confirm = input("Are you sure? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Cancelled.")
            sys.exit(0)
    
    print("📦 Setting up database migrations...")
    if not run_command("python manage.py makemigrations"):
        print("❌ Failed to create migrations")
        sys.exit(1)
    
    if not run_command("python manage.py migrate"):
        print("❌ Failed to run migrations")
        sys.exit(1)
    
    print("\n👥 Creating users and sample data...")
    
    setup_command = "python manage.py setup_users"
    if reset_mode:
        setup_command += " --reset"
    
    if not run_command(setup_command):
        print("❌ Failed to setup users")
        sys.exit(1)
    
    print("\n✅ Setup completed successfully!")
    print("\n" + "=" * 60)
    print("USER CREDENTIALS")
    print("=" * 60)
    
    credentials = [
        ("SUPERUSER", [
            ("admin", "admin123", "admin@shelter.com", "Full Access")
        ]),
        ("SHELTER APP", [
            ("shelter_manager", "shelter123", "manager@shelter.com", "Manager"),
            ("shelter_employee", "shelter123", "employee@shelter.com", "Employee")
        ]),
        ("AGENTS APP", [
            ("agent_admin", "agent123", "admin@agents.com", "Admin"),
            ("agent_manager", "agent123", "manager@agents.com", "Manager"),
            ("agent_1", "agent123", "agent1@agents.com", "Agent"),
            ("agent_2", "agent123", "agent2@agents.com", "Agent")
        ]),
        ("TEAM APP", [
            ("team_admin", "team123", "admin@team.com", "Admin"),
            ("team_manager", "team123", "manager@team.com", "Manager"),
            ("team_member_1", "team123", "member1@team.com", "Member"),
            ("team_member_2", "team123", "member2@team.com", "Member")
        ]),
        ("CRM APP", [
            ("crm_admin", "crm123", "admin@crm.com", "Admin"),
            ("crm_manager", "crm123", "manager@crm.com", "Manager"),
            ("crm_employee_1", "crm123", "employee1@crm.com", "Employee"),
            ("crm_employee_2", "crm123", "employee2@crm.com", "Employee")
        ]),
        ("MARKETING APP", [
            ("marketing_admin", "marketing123", "admin@marketing.com", "Admin"),
            ("marketing_manager", "marketing123", "manager@marketing.com", "Manager"),
            ("marketing_employee", "marketing123", "employee@marketing.com", "Employee")
        ])
    ]
    
    for app_name, users in credentials:
        print(f"\n{app_name}:")
        print("-" * len(app_name))
        for username, password, email, role in users:
            print(f"Username: {username:20} | Password: {password:15} | Role: {role}")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000/admin/")
    print("3. Login with any of the credentials above")
    print("4. Test role-based access and features")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()