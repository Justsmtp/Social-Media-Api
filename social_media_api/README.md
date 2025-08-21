# 📱 Social Media API – Django REST Framework

A backend API for a social media platform built with **Django** and **Django REST Framework (DRF)**.  
It supports **user authentication (JWT)**, **CRUD for posts & comments**, **likes**, **follow system**, and a personalized **feed**.

---

## 🚀 Features

### **Authentication**
- User registration with secure password hashing.
- JWT authentication (login & token refresh).
- Only authenticated users can create, update, or delete their own content.

### **Post Management (CRUD)**
- Create, read, update, and delete posts.
- Supports text content and optional media uploads.
- Counts total likes & comments for each post.

### **Comments (CRUD)**
- Add comments to posts.
- Update or delete only your own comments.

### **Likes**
- Toggle like/unlike for posts with a single endpoint.
- Prevents duplicate likes from the same user.

### **Follow System**
- Toggle follow/unfollow other users.
- Cannot follow yourself.

### **Feed**
- Personalized feed of posts from users you follow.
- Ordered by most recent posts.
- Paginated for efficiency.

---

## 🗂 API Endpoints

| Endpoint                     | Method | Description |
|------------------------------|--------|-------------|
| `/api/register/`             | POST   | Create a new user |
| `/api/login/`                | POST   | Authenticate and return JWT token |
| `/api/token/refresh/`        | POST   | Refresh JWT token |
| `/api/posts/`                | GET, POST | List all posts / Create a new post |
| `/api/posts/<id>/`           | GET, PUT, DELETE | Retrieve, update, or delete a post |
| `/api/comments/`             | GET, POST | List all comments / Create a new comment |
| `/api/comments/<id>/`        | GET, PUT, DELETE | Retrieve, update, or delete a comment |
| `/api/likes/`                | POST   | Like or unlike a post |
| `/api/follow/`               | POST   | Follow or unfollow a user |
| `/api/feed/`                 | GET    | View posts from followed users |

---

## 🛠 Installation & Setup

### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/Justsmtp/social-media-api.git
cd social-media-api

2️⃣ Create a Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Database & Settings
Create a .env file in the root directory:

SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=*

In settings.py, ensure:

AUTH_USER_MODEL = 'api.User'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

5️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Create Superuser
python manage.py createsuperuser

7️⃣ Run the Server
python manage.py runserver

📦 Requirements
Django >= 5.0

djangorestframework >= 3.15

djangorestframework-simplejwt >= 5.3

Pillow >= 10.0

🔑 Authentication
This project uses JWT (JSON Web Token) for authentication.

Login Example
Request

POST /api/login/
{
  "username": "john",
  "password": "123456"
}

Response
{
  "refresh": "your_refresh_token",
  "access": "your_access_token"
}
Include the access token in headers for protected endpoints:

Authorization: Bearer your_access_token
📤 Media Uploads
Posts and profile pictures support image uploads.

Files are stored in the /media/ directory (configurable in settings.py).

📜 Pagination
Feed results are paginated:

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
🧪 Example Workflow
Register a user → /api/register/

Login to get JWT token → /api/login/

Create a post → /api/posts/ (Authenticated)

Comment on a post → /api/comments/

Like/unlike a post → /api/likes/

Follow/unfollow a user → /api/follow/

View your feed → /api/feed/

📌 Next Improvements (Stretch Goals)
Notifications (likes, comments, follows).

Hashtags & mentions.

Repost & share features.

AWS S3 for media storage.

Trending posts.

👨‍💻 Author
Oladimeji Toba

GitHub: Justsmtp

LinkedIn: Oladimeji Toba