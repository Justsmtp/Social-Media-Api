# Social Media API - Capstone Project

## 🌐 Live Deployment
**Production API Base URL**: `https://justsmtp.pythonanywhere.com`

## Project Overview

This is a Django REST Framework (DRF) based social media API designed as a capstone project. It supports user registration, authentication (JWT), posting content, commenting, liking posts, following/unfollowing users, and notifications. The project is production-ready and follows best practices for API development with Django.

## 🚀 Features

### User Management
- Custom user model with profile picture and bio
- JWT-based authentication (access & refresh tokens)
- User registration and login endpoints
- Follow and unfollow other users
- View lists of followers and following

### Posts & Comments
- Users can create, update, and delete posts
- Each post supports text content and optional media uploads
- Commenting on posts with author association
- List all comments for a post
- View posts from users you follow (Feed)

### Likes
- Like and unlike posts
- Notifications sent to post authors when liked

### Notifications
- Real-time notifications for actions like likes, comments, and follows
- Mark notifications as read/unread

### Security
- JWT Authentication for secure API access
- Permissions: Only authors can edit/delete posts or comments
- Non-authenticated users have read-only access

## 🛠️ Tech Stack
- Python 3.12
- Django 4.x
- Django REST Framework
- Django Filter
- PostgreSQL or SQLite (development)
- JWT Authentication (djangorestframework-simplejwt)
- **Deployed on**: PythonAnywhere

## 📁 Project Structure
```
social_media_api/
├── users/                  # Custom User model and authentication
├── posts/                  # Posts, comments, likes
├── notifications/          # Notification system
├── social_media_api/       # Django project settings
├── manage.py
├── requirements.txt
└── README.md
```

## 📚 API Endpoints Documentation

### 👤 User Endpoints
| Method | Endpoint | Description | Live URL |
|--------|----------|-------------|----------|
| POST | `/api/users/register/` | Register new user | `https://justsmtp.pythonanywhere.com/api/users/register/` |
| POST | `/api/users/login/` | Obtain JWT access and refresh tokens | `https://justsmtp.pythonanywhere.com/api/users/login/` |
| GET | `/api/users/profile/` | Get logged-in user profile | `https://justsmtp.pythonanywhere.com/api/users/profile/` |
| POST | `/api/users/follow/<user_id>/` | Follow a user | `https://justsmtp.pythonanywhere.com/api/users/follow/1/` |
| POST | `/api/users/unfollow/<user_id>/` | Unfollow a user | `https://justsmtp.pythonanywhere.com/api/users/unfollow/1/` |
| GET | `/api/users/following/` | List users you follow | `https://justsmtp.pythonanywhere.com/api/users/following/` |
| GET | `/api/users/followers/` | List users following you | `https://justsmtp.pythonanywhere.com/api/users/followers/` |

### 📝 Post Endpoints
| Method | Endpoint | Description | Live URL |
|--------|----------|-------------|----------|
| GET | `/api/posts/` | List all posts | `https://justsmtp.pythonanywhere.com/api/posts/` |
| POST | `/api/posts/` | Create a post | `https://justsmtp.pythonanywhere.com/api/posts/` |
| GET | `/api/posts<id>/` | Retrieve a post | `https://justsmtp.pythonanywhere.com/api/posts/1/` |
| PUT/PATCH | `/api/posts/<id>/` | Update a post | `https://justsmtp.pythonanywhere.com/api/posts/1/` |
| DELETE | `/api/posts/<id>/` | Delete a post | `https://justsmtp.pythonanywhere.com/api/posts/1/` |
| GET | `/api/posts/feed/` | Feed from users you follow | `https://justsmtp.pythonanywhere.com/api/posts/feed/` |
| POST | `/api/posts/<id>/like/` | Like a post | `https://justsmtp.pythonanywhere.com/api/posts/1/like/` |
| POST | `/api/posts/<id>/unlike/` | Unlike a post | `https://justsmtp.pythonanywhere.com/api/posts/1/unlike/` |

### 💬 Comment Endpoints
| Method | Endpoint | Description | Live URL |
|--------|----------|-------------|----------|
| GET | `/api/posts/comments/` | List all comments | `https://justsmtp.pythonanywhere.com/api/posts/comments/` |
| POST | `/api/posts/comments/` | Create a comment | `https://justsmtp.pythonanywhere.com/api/posts/comments/` |

### 🔔 Notification Endpoints
| Method | Endpoint | Description | Live URL |
|--------|----------|-------------|----------|
| GET | `/api/notifications/` | List notifications | `https://justsmtp.pythonanywhere.com/api/notifications/` |

## 🧪 Testing the Live API

### Quick Start Testing Guide

#### 1. Register a New User
```bash
curl -X POST https://justsmtp.pythonanywhere.com/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepass123",
    "bio": "Test user bio"
  }'
```

#### 2. Login and Get JWT Token
```bash
curl -X POST https://justsmtp.pythonanywhere.com/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepass123"
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### 3. Create a Post (Authentication Required)
```bash
curl -X POST https://justsmtp.pythonanywhere.com/api/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{
    "title": "My First Post",
    "content": "Hello, this is my first post on the social media API!"
  }'
```

#### 4. Get All Posts (Public)
```bash
curl -X GET https://justsmtp.pythonanywhere.com/api/posts/
```

#### 5. Create a Comment
```bash
curl -X POST https://justsmtp.pythonanywhere.com/api/posts/comments/ \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "post": 1,
    "content": "Great post!"
  }'
```

#### 6. Like a Post
```bash
curl -X POST https://justsmtp.pythonanywhere.com/api/posts/1/like/ \
  -H "Authorization: Bearer <your_access_token>"
```

### 🔐 Authentication Note
- Most endpoints require JWT authentication
- Include `Authorization: Bearer <access_token>` in request headers
- Access tokens expire after a certain time (use refresh token to get new ones)

### 🌐 Browser Testing
You can also test GET endpoints directly in your browser:
- View all posts: `https://justsmtp.pythonanywhere.com/api/posts/`
- DRF Browsable API: Visit any endpoint URL in browser for interactive testing

## 🛠️ Local Development Setup

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Justsmtp/social_media_api.git
cd social_media_api
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
Create a `.env` file with:
```env
SECRET_KEY=<your-secret-key>
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. **Apply migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create a superuser:**
```bash
python manage.py createsuperuser
```

7. **Run the development server:**
```bash
python manage.py runserver
```

## 🚀 Production Deployment

This project is successfully deployed on **PythonAnywhere** with the following configurations:

### Production Settings
- **DEBUG**: False
- **ALLOWED_HOSTS**: Configured for justsmtp.pythonanywhere.com
- **Database**: PostgreSQL/MySQL (production-grade)
- **Static Files**: Properly configured for production
- **Security**: HTTPS enabled, secure headers configured

### Deployment Features
- ✅ Live API endpoints accessible via HTTPS
- ✅ JWT authentication working
- ✅ Database migrations applied
- ✅ Static files served correctly
- ✅ CORS configured for frontend integration
- ✅ Error logging and monitoring

## 📊 Testing Tools & Resources

### Recommended Testing Tools
- **Postman**: Import endpoint collection for comprehensive testing
- **cURL**: Use provided examples above
- **DRF Browsable API**: Visit endpoints in browser
- **HTTPie**: Alternative to cURL for API testing

### Example Postman Collection
```json
{
  "info": { "name": "Social Media API" },
  "variable": [
    {
      "key": "base_url",
      "value": "https://justsmtp.pythonanywhere.com"
    }
  ]
}
```

## 🔮 Future Improvements
- [ ] Add image/video upload support
- [ ] Add real-time notifications using WebSockets  
- [ ] Enhanced pagination for comments and posts
- [ ] Comprehensive unit tests for all endpoints
- [ ] Rate-limiting to prevent abuse
- [ ] Advanced search and filtering
- [ ] Email notifications
- [ ] Social features (stories, direct messaging)

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support & Contact
- **Repository**: https://github.com/Justsmtp/social_media_api
- **Live API**: https://justsmtp.pythonanywhere.com
- **Issues**: Report bugs or request features via GitHub Issues

---

**🎉 The API is live and ready for integration!** 

Use the provided endpoints to build your frontend application or integrate with existing systems.