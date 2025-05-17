Blog-App
Blog-App is a RESTful API built with Django 5.1 and Django REST Framework, designed for creating and managing blogs, comments, and notifications. It supports user authentication via JSON Web Tokens (JWT) and provides a Swagger UI for API documentation and testing.
Features

Blog Management: Create, read, update, and delete (CRUD) blogs with titles, descriptions, and optional photos.
Comments: Add and manage comments on blogs, with support for nested replies.
Notifications: Receive notifications for likes and comments on your blogs.
Authentication: Secure JWT-based authentication using access and refresh tokens.
Filtering & Ordering: Filter blogs by author or title and order by creation date or like count.
Swagger UI: Interactive API documentation for testing endpoints.

Prerequisites

Python 3.13+
Virtualenv
SQLite (default database)

Installation

Clone the repository:
git clone <repository-url>
cd blog-app


Set up a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate


Install dependencies:
pip install -r requirements.txt


Set up environment variables:Create a .env file in the project root:
SECRET_KEY=your-secret-key
ACCESS_TOKEN_LIFETIME=5
REFRESH_TOKEN_LIFETIME=1440


Apply migrations:
python manage.py migrate


Create a test user:
python manage.py shell

from django.contrib.auth.models import User
user = User.objects.create_user(username='testuser', password='testpass123', email='test@example.com')
user.is_active = True
user.save()



Running the Application

Start the development server:python manage.py runserver


Access the API at http://127.0.0.1:8000 and Swagger UI at http://127.0.0.1:8000/swagger/.

Testing the REST API with Swagger UI

Open Swagger UI:Navigate to http://127.0.0.1:8000/swagger/.

Obtain a JWT Token:

Go to POST /api/token/.
Click Try it out.
Enter:{
  "username": "testuser",
  "password": "testpass123"
}


Click Execute and copy the access token from the response.


Authenticate:

Click Authorize in Swagger UI.
Enter Bearer <your_access_token> (e.g., Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...).
Click Authorize.


Test Endpoints:

Create a Blog: Use POST /api/blogs/ with:{
  "title": "My Blog",
  "description": "A test blog."
}


List Blogs: Use GET /api/blogs/ with filters like ?title=My or ?ordering=-like_count.
Add Comment: Use POST /api/comments/ with:{
  "blog_id": 1,
  "text": "Great blog!"
}


View Notifications: Use GET /api/notifications/.


Refresh Token:If the access token expires (default: 5 minutes), use POST /api/token/refresh/ with:
{
  "refresh": "<your_refresh_token>"
}



Example curl Commands

Get Token:curl -X POST http://127.0.0.1:8000/api/token/ -H 'Content-Type: application/json' -d '{"username": "testuser", "password": "testpass123"}'


Create Blog:curl -X POST http://127.0.0.1:8000/api/blogs/ -H 'Content-Type: application/json' -H 'Authorization: Bearer <access_token>' -d '{"title": "Test", "description": "Blog"}'




