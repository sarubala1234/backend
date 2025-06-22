# JobPortal - Django Job Portal System

A comprehensive job portal system built with Django that connects job seekers with employers. This system provides a modern, responsive web application for posting jobs, searching for opportunities, and managing applications.

## Features

### For Job Seekers
- **User Registration & Profile Management**: Create accounts and manage detailed profiles
- **Job Search & Filtering**: Advanced search with filters for location, category, employment type, and experience level
- **Job Applications**: Apply to jobs with cover letters and resume uploads
- **Job Bookmarks**: Save interesting jobs for later review
- **Application Tracking**: Monitor the status of your job applications
- **Dashboard**: Overview of applications, bookmarks, and profile information

### For Employers
- **Company Registration**: Register your company and create detailed company profiles
- **Job Posting**: Post new job opportunities with comprehensive details
- **Application Management**: Review and manage job applications
- **Company Dashboard**: Overview of posted jobs and received applications

### General Features
- **Responsive Design**: Modern, mobile-friendly interface using Bootstrap 5
- **Search & Filter**: Advanced job search with multiple filter options
- **User Authentication**: Secure login/logout system
- **Admin Panel**: Full Django admin interface for system management
- **File Upload**: Support for resume and company logo uploads
- **Pagination**: Efficient browsing of job listings

## Technology Stack

- **Backend**: Django 5.2.3
- **Database**: SQLite (can be easily changed to PostgreSQL/MySQL)
- **Frontend**: Bootstrap 5, Font Awesome, jQuery
- **File Storage**: Django's built-in file handling
- **Authentication**: Django's built-in authentication system

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd job-portal
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Populate with sample data (optional)**
   ```bash
   python manage.py populate_data
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
job/
├── job/                    # Main Django project
│   ├── settings.py        # Project settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── jobportal/            # Main application
│   ├── models.py         # Database models
│   ├── views.py          # View functions
│   ├── forms.py          # Form classes
│   ├── admin.py          # Admin configuration
│   └── urls.py           # App URL patterns
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── jobportal/        # App-specific templates
│   └── registration/     # Authentication templates
├── static/               # Static files (CSS, JS)
├── media/                # User-uploaded files
└── manage.py            # Django management script
```

## Models

### Core Models
- **User**: Extended Django User model with profile information
- **Company**: Company information and details
- **Job**: Job postings with comprehensive details
- **Application**: Job applications with status tracking
- **Category**: Job categories for organization
- **UserProfile**: Extended user profile information
- **JobBookmark**: User bookmarks for jobs

## Key Features Explained

### Job Search & Filtering
The system provides advanced search functionality with filters for:
- Keywords (job title, description, company name)
- Location
- Job category
- Employment type (Full-time, Part-time, Contract, etc.)
- Experience level (Entry, Mid, Senior, Executive)
- Remote work options

### Application System
- Users can apply to jobs with cover letters and resume uploads
- Application status tracking (Pending, Reviewed, Shortlisted, etc.)
- Prevention of duplicate applications
- File upload support for resumes

### User Management
- Separate registration flows for job seekers and employers
- Profile management with skills, experience, and education
- Company profiles with detailed information
- User authentication and authorization

## Admin Panel

The Django admin panel provides comprehensive management capabilities:
- User and company management
- Job posting management
- Application review and status updates
- Category management
- System-wide statistics

## Customization

### Adding New Features
1. Create new models in `models.py`
2. Add corresponding views in `views.py`
3. Create forms in `forms.py`
4. Add URL patterns in `urls.py`
5. Create templates in the `templates/` directory

### Styling
- The system uses Bootstrap 5 for responsive design
- Custom CSS can be added to `static/css/`
- Font Awesome icons are used throughout the interface

### Database
- Currently uses SQLite for development
- For production, consider using PostgreSQL or MySQL
- Update `settings.py` DATABASES configuration

## Deployment

### Production Considerations
1. **Security**: Update `SECRET_KEY` and set `DEBUG = False`
2. **Database**: Use a production database (PostgreSQL recommended)
3. **Static Files**: Configure static file serving
4. **Media Files**: Set up proper media file storage
5. **HTTPS**: Enable HTTPS for security
6. **Environment Variables**: Use environment variables for sensitive settings

### Recommended Deployment Stack
- **Web Server**: Nginx
- **Application Server**: Gunicorn
- **Database**: PostgreSQL
- **File Storage**: AWS S3 or similar (for media files)

## Sample Data

The system includes a management command to populate the database with sample data:
```bash
python manage.py populate_data
```

This creates:
- 8 job categories
- 4 sample companies
- 6 sample job postings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## Future Enhancements

Potential features for future versions:
- Email notifications
- Advanced analytics and reporting
- Integration with external job boards
- Resume parsing and matching
- Interview scheduling
- Video interviews
- Mobile app development
- API for third-party integrations 