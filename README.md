# 📘 Blog-App

Blog-App is a RESTful API built with Django 5.1 and Django REST Framework, designed for creating and managing blogs, comments, and notifications. It supports JWT-based authentication and includes Swagger UI for interactive API documentation and testing.

## 🚀 Features

- Blog Management – Create, read, update, and delete blog posts with titles, descriptions, and optional photos.  
- Comments – Add and manage comments on blogs, with support for nested replies.  
- Notifications – Receive alerts when users comment on or like your blog posts.  
- Authentication – Secure login using JWT (access and refresh tokens).  
- Filtering & Ordering – Filter blogs by author or title, and sort by date or number of likes.  
- Swagger UI – Built-in interactive API documentation for easy testing.

## 📋 Prerequisites

- Python 3.13+  
- virtualenv  
- SQLite (default database)

## ⚙️ Installation

Clone the repository:  
git clone https://github.com/NikaL25/Blog_app_django.git  
cd blog-app

Create and activate a virtual environment:  
python -m venv venv  
source venv/bin/activate        # macOS/Linux  
.\venv\Scripts\activate         # Windows

Install dependencies:  
pip install -r requirements.txt

Configure environment variables by creating a `.env` file in the project root:  
SECRET_KEY=your-secret-key  
ACCESS_TOKEN_LIFETIME=5  
REFRESH_TOKEN_LIFETIME=1440

Apply database migrations:  
python manage.py migrate

Create a test user (optional):  
python manage.py shell  
from django.contrib.auth.models import User  
user = User.objects.create_user(username='testuser', password='testpass123', email='test@example.com')  
user.is_active = True  
user.save()

## ▶️ Running the App

Start the development server:  
python manage.py runserver

Visit the API root at http://127.0.0.1:8000/  
Visit the Swagger UI at http://127.0.0.1:8000/swagger/

## 🧪 API Testing with Swagger

Open Swagger UI at http://127.0.0.1:8000/swagger/  

Use POST /api/token/ with the following JSON to obtain a JWT token:  
{  
  "username": "testuser",  
  "password": "testpass123"  
}

Click “Authorize” in Swagger and enter:  
Bearer <your_access_token>

Test the endpoints:  

Create blog: POST /api/blogs/  
{  
  "title": "My Blog",  
  "description": "A test blog."  
}

List blogs: GET /api/blogs/?title=Test&ordering=-like_count

Add comment: POST /api/comments/  
{  
  "blog_id": 1,  
  "text": "Nice blog!"  
}

View notifications: GET /api/notifications/

Refresh token: POST /api/token/refresh/  
{  
  "refresh": "<your_refresh_token>"  
}

## 💻 Example curl Commands

Get JWT token:  
curl -X POST http://127.0.0.1:8000/api/token/ \  
     -H "Content-Type: application/json" \  
     -d '{"username": "testuser", "password": "testpass123"}'

Create a blog post:  
curl -X POST http://127.0.0.1:8000/api/blogs/ \  
     -H "Content-Type: application/json" \  
     -H "Authorization: Bearer <access_token>" \  
     -d '{"title": "Test Blog", "description": "My first blog"}'
