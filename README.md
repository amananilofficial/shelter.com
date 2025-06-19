# Django Real Estate Website

A comprehensive real estate management system built with Django, featuring property listings, agent management, team profiles, and user interactions.

## 🏠 Project Overview

This Django-based real estate platform provides a complete solution for property management, agent portfolios, and customer interactions. The system includes property listings, agent profiles, team management, contact forms, and newsletter subscriptions.

## ✨ Features

### Property Management
- **Property Listings**: Browse and search properties with detailed information
- **Property Details**: Comprehensive property pages with multiple images
- **Search & Filter**: Advanced search by location, price, bedrooms, bathrooms
- **Property Status**: Support for both rental and sale properties

### Agent Management
- **Agent Profiles**: Detailed agent pages with photos and descriptions
- **Work Experience**: Display agent experience as formatted bullet points
- **Contact Information**: Phone, email, WhatsApp, Instagram, LinkedIn
- **Agent Contact Forms**: Direct communication with specific agents

### Team Management
- **Team Member Profiles**: Dedicated team section with member details
- **Team Contact**: Individual contact forms for team members
- **Social Media Integration**: LinkedIn, Instagram, WhatsApp links

### User Interactions
- **Contact Forms**: Multiple contact form types for different purposes
- **Newsletter Subscription**: Email subscription with WhatsApp updates option
- **Quick Contact**: Simplified contact form for quick inquiries

### Additional Features
- **Responsive Design**: Mobile-friendly interface
- **Media Management**: Image uploads with organized file structure
- **Admin Interface**: Django admin for content management
- **Static Pages**: About, Services, Terms, Privacy, Cookies pages

## 🛠️ Technology Stack

- **Backend**: Django 3.x
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Media Handling**: Pillow for image processing
- **Deployment**: Gunicorn + WhiteNoise for static files
- **Styling**: HTML/CSS with responsive design

## 📋 Requirements

```
asgiref
dj-database-url<1.0.0
Django
gunicorn
Pillow
pytz
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
- **Listing**: Property listings with details, images, and status
- **Contact**: General contact form submissions
- **Quickcontact**: Quick contact form entries
- **Newsletter**: Newsletter subscribers with preferences

### Agents App Models
- **Agent**: Agent profiles with contact info and experience
- **AgentContact**: General agent contact messages
- **AgentPropertyContact**: Property-specific agent contacts

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
<div align="center">

**Built with ❤️ using Django**

</div>
