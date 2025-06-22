# 🏠 Shelter.com - Django Real Estate Management System

[![](https://img.shields.io/badge/Django-4.2+-blue.svg)](https://www.djangoproject.com/) [![](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/) [![](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://www.postgresql.org/) [![](https://img.shields.io/badge/SQLite-3+-lightgrey.svg)](https://www.sqlite.org/)

A comprehensive, enterprise-grade real estate management system built with Django, featuring advanced property listings, intelligent agent management, team collaboration tools, and REST API integration.

## � Project Overview

**Shelter.com** is a full-featured Django-based real estate platform that provides a complete ecosystem for property management, agent portfolios, customer relationship management, and marketing automation. The system is designed for real estate agencies, property developers, and individual agents who need a professional, scalable solution for their business operations.

### 🎯 Key Objectives
- **Streamline Operations**: Centralize property management, agent coordination, and customer interactions
- **Enhance Customer Experience**: Provide intuitive search, detailed property information, and seamless contact options
- **Boost Productivity**: Automate routine tasks, track leads, and manage marketing campaigns
- **Scale Efficiently**: Support multiple agents, teams, and large property inventories
- **Data-Driven Insights**: Track performance metrics, lead conversion, and marketing ROI

## ✨ Features

### 🏘️ Property Management
- **Property Listings**: Browse and search properties with detailed information
- **Property Details**: Comprehensive property pages with multiple images
- **Search & Filter**: Advanced search by location, price, bedrooms, bathrooms
- **Property Status**: Support for both rental and sale properties
- **Featured Properties**: Highlight premium listings on homepage
- **Property Categories**: Residential, commercial, land, and investment properties
- **Virtual Tours**: 360° property views and virtual walkthroughs
- **Price History**: Track property price changes over time

### 👥 Agent Management
- **Agent Profiles**: Detailed agent pages with photos and descriptions
- **Work Experience**: Display agent experience as formatted bullet points
- **Contact Information**: Phone, email, WhatsApp, Instagram, LinkedIn
- **Agent Contact Forms**: Direct communication with specific agents
- **Performance Metrics**: Track agent sales and customer satisfaction
- **Agent Territories**: Manage geographic specializations
- **Lead Assignment**: Automatic lead distribution to agents
- **Commission Tracking**: Monitor agent earnings and commissions

### 🤝 Team Management
- **Team Member Profiles**: Dedicated team section with member details
- **Team Contact**: Individual contact forms for team members
- **Social Media Integration**: LinkedIn, Instagram, WhatsApp links
- **Role Management**: Define team roles and responsibilities
- **Team Collaboration**: Internal messaging and task assignment
- **Performance Dashboard**: Team analytics and KPIs
- **Training Management**: Track team member certifications

### 📞 User Interactions
- **Contact Forms**: Multiple contact form types for different purposes
- **Newsletter Subscription**: Email subscription with WhatsApp updates option
- **Quick Contact**: Simplified contact form for quick inquiries
- **Live Chat**: Real-time customer support integration
- **Appointment Booking**: Schedule property viewings
- **Customer Reviews**: Property and agent rating system
- **Wishlist**: Save favorite properties for later

### 📱 Additional Features
- **Responsive Design**: Mobile-friendly interface across all devices
- **Media Management**: Image uploads with organized file structure
- **Admin Interface**: Django admin for comprehensive content management
- **Static Pages**: About, Services, Terms, Privacy, Cookies pages
- **SEO Optimization**: Meta tags, sitemaps, and search engine friendly URLs
- **REST API**: Django REST Framework integration with authentication
- **Email Notifications**: Automated email alerts for inquiries and updates

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 4.2+
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Media Handling**: Pillow for image processing
- **Deployment**: Gunicorn + WhiteNoise for static files
- **Security**: Django security middleware, CSRF protection
- **API**: Django REST Framework with authentication and filtering

### Frontend
- **Styling**: HTML5/CSS3 with responsive design
- **JavaScript**: Vanilla JS for interactive features
- **Icons**: Font Awesome
- **UI Framework**: Bootstrap-compatible components

### DevOps & Deployment
- **Web Server**: Gunicorn
- **Static Files**: WhiteNoise
- **Database**: PostgreSQL (production), SQLite (development)
- **Cloud Ready**: AWS, Heroku, DigitalOcean compatible

### Third-Party Integrations
- **Email**: Django email backend
- **Social Media**: WhatsApp, Instagram, LinkedIn integration
- **File Storage**: Local storage with cloud storage ready
- **SEO**: Django SEO optimization tools

## 📋 Requirements

```
asgiref
dj-database-url<1.0.0
Django
djangorestframework
django-import-export
django-guardian
django-filter
django-crispy-forms
gunicorn
Pillow
pandas
openpyxl
xlrd
xlwt
pytz
python-decouple
sqlparse
whitenoise
psycopg2-binary
```

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/amananilofficial/shelter.com.git
cd shelter.com
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Collect Static Files
```bash
python manage.py collectstatic
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to view the application.

## 📊 Database Models

### Shelter App Models
- **Listening**: Property listings with details, images, and status (Note: misspelled class name)
- **Contact**: General contact form submissions
- **Quickcontact**: Quick contact form entries
- **Newsletter**: Newsletter subscribers with preferences

### Agents App Models
- **Agent**: Agent profiles with contact info and experience
- **AgentRole**: Role-based permissions for agents (admin, manager, agent)
- **AgentContact**: General agent contact messages
- **AgentPropertyContact**: Property-specific agent contacts
- **WorkNote**: Work notes and follow-up records for agents

### Team App Models
- **Team**: Team member profiles and information
- **TeamContactMessage**: Contact messages for team members

### Users App Models
- **User**: Custom user model extending Django's AbstractUser

## 🔧 Configuration

### Environment Variables
Set the following environment variables for production:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `False` for production
- `DATABASE_URL`: Database connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Media Files
- Property images: `media/listings/YYYY/MM/DD/`
- Agent photos: `media/agents/YYYY/MM/DD/`
- Team photos: `media/photos/YYYY/MM/DD/`

## 🌐 URL Structure

### Main Routes
- `/` - Homepage with featured properties and agents
- `/properties-list/` - All properties listing
- `/property-detail/<slug>/` - Individual property details
- `/search/` - Property search with filters
- `/contact/` - General contact page
- `/about/` - About page
- `/services/` - Services page

### Agent Routes
- `/agents/` - All agents listing
- `/agents/<id>/` - Individual agent profile
- `/agents/contact/` - Agent contact form
- `/agents/property-contact/` - Property-specific agent contact

### Team Routes
- `/team/` - Team members listing
- `/team/<id>/` - Individual team member profile
- `/team/<id>/contact/` - Team member contact form

## 🎨 Frontend Features

### Search Functionality
- Location-based search
- Price range filtering
- Bedroom/bathroom filters
- Keyword search in descriptions

### Contact Forms
- General contact form
- Agent-specific contact
- Property inquiry forms
- Team member contact
- Quick contact widget
- Newsletter subscription

### Property Display
- Image galleries
- Property details
- Agent information
- Related properties sidebar

## 🔐 Admin Interface

Access the Django admin at `/admin/` to manage:
- Property listings
- Agent profiles
- Team members
- Contact messages
- Newsletter subscribers
- User accounts

## 📱 Responsive Design

The application is fully responsive and optimized for:
- Desktop computers
- Tablets
- Mobile phones
- Various screen sizes

## 🚀 Deployment

### Production Settings
1. Set `DEBUG = False`
2. Configure proper database (PostgreSQL recommended)
3. Set up media file serving
4. Configure email backend for contact forms
5. Set up SSL/HTTPS
6. Configure static file serving with WhiteNoise

### Deployment Platforms
- Heroku (ready with Procfile and requirements)
- DigitalOcean
- AWS
- Google Cloud Platform

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request


## 🐛 Bug Reports

If you find any bugs or issues, please report them using the GitHub issue tracker.

## 🔄 Version History

- **v1.0.0** - Initial release with core functionality
- Property listings and search
- Agent and team management
- Contact forms and newsletter
- Admin interface

---

# Shelter.com - Automated User Setup System

This project includes a comprehensive automated user setup system that creates users, roles, and sample data for all applications.

## 🚀 Quick Start

### Option 1: Python Script (Recommended)
```bash
python quick_setup.py
```

### Option 2: Django Management Command
```bash
python manage.py setup_users
```

### Option 3: Batch File (Windows)
```bash
setup_users.bat
```

### Option 4: Shell Script (Linux/Mac)
```bash
./setup_users.sh
```

## 🔄 Reset Mode
To completely reset and recreate all data:
```bash
python quick_setup.py --reset
# OR
python manage.py setup_users --reset
```

## 👥 User Accounts Created

### 🔧 System Administrator
| Username | Password | Email | Role |
|----------|----------|-------|------|
| admin | admin123 | admin@shelter.com | Superuser |

### 🏠 Shelter App Users
| Username | Password | Email | Role |
|----------|----------|-------|------|
| shelter_manager | shelter123 | manager@shelter.com | Manager |
| shelter_employee | shelter123 | employee@shelter.com | Employee |

### 🏘️ Agents App Users
| Username | Password | Email | Role |
|----------|----------|-------|------|
| agent_admin | agent123 | admin@agents.com | Admin |
| agent_manager | agent123 | manager@agents.com | Manager |
| agent_1 | agent123 | agent1@agents.com | Agent |
| agent_2 | agent123 | agent2@agents.com | Agent |

### 👥 Team App Users
| Username | Password | Email | Role |
|----------|----------|-------|------|
| team_admin | team123 | admin@team.com | Admin |
| team_manager | team123 | manager@team.com | Manager |
| team_member_1 | team123 | member1@team.com | Member |
| team_member_2 | team123 | member2@team.com | Member |

## 📊 Sample Data Generated

### Shelter App
- **Property Listings**: Luxury villa, modern apartment, family house
- **Contact Inquiries**: Sample customer inquiries
- **Newsletter Subscribers**: Sample email subscribers

### Agents App
- **Agent Profiles**: Complete profiles with contact info and experience
- **Agent Contacts**: Sample client contact messages
- **Work Notes**: Follow-up notes and customer interactions

### Team App
- **Team Profiles**: Complete team member profiles
- **Contact Messages**: Sample team contact inquiries
- **Work Experience**: Professional experience data

## 🔐 Role-Based Permissions

### Admin
- ✅ Full access to all data
- ✅ Create, edit, delete all records
- ✅ Manage user roles
- ✅ Export/import data
- ✅ System configuration

### Manager
- ✅ View and edit most data
- ✅ Create new records
- ✅ Export data
- ⚠️ Limited delete permissions
- ❌ Cannot manage user roles

### Employee/Agent/Member
- ✅ View assigned/own data
- ✅ Edit own records
- ⚠️ Limited create permissions
- ❌ No delete permissions
- ❌ Cannot export data

## 🛠️ What Each App Needs

### Shelter App (Main)
- **Required**: Property listings, contacts, newsletter
- **Features**: Search, filtering, featured properties
- **Permissions**: Manager can manage all listings

### Agents App
- **Required**: Agent profiles, client contacts, work notes
- **Features**: Agent portfolio, client management
- **Permissions**: Agents see only their own data

### Team App
- **Required**: Team member profiles, contact messages
- **Features**: Team showcase, contact forms
- **Permissions**: Members see only their own profile

## 🔄 Inter-App Synchronization

The system includes automatic synchronization between apps:
- **Team → Agents**: Team members with manager/admin roles sync to agents
- **Agents**: Work notes and client interactions
- **System**: Role-based permissions across all apps

## 🧪 Testing

After setup, you can test:
1. **Login** with any user credentials
2. **Role-based access** - try accessing different sections
3. **CRUD operations** - create, read, update, delete based on permissions
4. **Data export** - test CSV/Excel export functionality
5. **Inter-app sync** - modify data in one app and check others

## 📝 Development Notes

- All passwords are simple for development (change in production)
- Sample data includes realistic contact information
- Role permissions are enforced at the model level
- Export functionality is available for all data
- All Django admin features are properly configured

## 🚀 Getting Started

1. **Run Setup**:
   ```bash
   python quick_setup.py
   ```

2. **Start Server**:
   ```bash
   python manage.py runserver
   ```

3. **Access Admin**:
   - URL: http://127.0.0.1:8000/admin/
   - Login with any user credentials above

4. **Test Features**:
   - Try different user roles
   - Test permissions
   - View sample data
   - Test export functionality

## 🐛 Troubleshooting

**Issue**: "manage.py not found"
- **Solution**: Make sure you're in the project root directory

**Issue**: Migration errors
- **Solution**: Run `python manage.py makemigrations` first

**Issue**: Permission denied
- **Solution**: Ensure user has proper role assignment

**Issue**: Missing sample data
- **Solution**: Run with `--reset` flag to recreate everything

---

<div align="center">

**Built with ❤️ using Django by Aman Anil**

</div>
