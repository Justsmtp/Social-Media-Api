# Social Media API

A comprehensive backend API for a social media platform built with Django and Django REST Framework. This project provides a complete foundation for building modern social media applications with user authentication, content management, and social interactions.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [API Endpoints](#api-endpoints)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Authentication](#authentication)
- [Media Handling](#media-handling)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

### Core Functionality

- **User Authentication & Authorization**
  - Secure user registration with password hashing
  - JWT-based authentication with token refresh
  - Role-based access control for content management

- **Content Management**
  - Full CRUD operations for posts and comments
  - Rich media support (images, videos)
  - Real-time engagement metrics (likes, comments count)

- **Social Features**
  - Follow/unfollow system with user relationships
  - Personalized feed algorithm
  - Like/unlike functionality with duplicate prevention

- **Performance & Scalability**
  - Paginated API responses
  - Optimized database queries
  - RESTful API design principles

## Technology Stack

- **Backend Framework**: Django 5.0+
- **API Framework**: Django REST Framework 3.15+
- **Authentication**: JWT (djangorestframework-simplejwt 5.3+)
- **Media Processing**: Pillow 10.0+
- **Database**: SQLite (default) / PostgreSQL (recommended for production)

## API Endpoints

### Authentication
| Endpoint | Method | Description | Authentication |
|----------|---------|-------------|----------------|
| `/api/register/` | POST | User registration | Public |
| `/api/login/` | POST | User login | Public |
| `/api/token/refresh/` | POST | Refresh JWT token | Public |

### Posts
| Endpoint | Method | Description | Authentication |
|----------|---------|-------------|----------------|
| `/api/posts/` | GET | List all posts | Optional |
| `/api/posts/` | POST | Create new post | Required |
| `/api/posts/<id>/` | GET | Retrieve specific post | Optional |
| `/api/posts/<id>/` | PUT | Update post | Required (Owner) |
| `/api/posts/<id>/` | DELETE | Delete post | Required (Owner) |

### Comments
| Endpoint | Method | Description | Authentication |
|----------|---------|-------------|----------------|
| `/api/comments/` | GET | List all comments | Optional |
| `/api/comments/` | POST | Create new comment | Required |
| `/api/comments/<id>/` | GET | Retrieve specific comment | Optional |
| `/api/comments/<id>/` | PUT | Update comment | Required (Owner) |
| `/api/comments/<id>/` | DELETE | Delete comment | Required (Owner) |

### Social Features
| Endpoint | Method | Description | Authentication |
|----------|---------|-------------|----------------|
| `/api/likes/` | POST | Toggle like/unlike post | Required |
| `/api/follow/` | POST | Toggle follow/unfollow user | Required |
| `/api/feed/` | GET | Personalized user feed | Required |

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Justsmtp/social-media-api.git
   cd social-media-api
   ```

2. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=sqlite:///db.sqlite3
   ```

5. **Database setup**
   ```bash
   # Create and apply migrations
   python manage.py makemigrations
   python manage.py migrate
   
   # Create superuser account
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`

## Configuration

### Django Settings

Ensure your `settings.py` includes:

```python
# Custom user model
AUTH_USER_MODEL = 'api.User'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

### JWT Configuration

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}
```

## Usage

### Authentication Flow

1. **Register a new user**
   ```bash
   curl -X POST http://localhost:8000/api/register/ \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "email": "john@example.com",
       "password": "secure_password123"
     }'
   ```

2. **Login to get JWT tokens**
   ```bash
   curl -X POST http://localhost:8000/api/login/ \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "password": "secure_password123"
     }'
   ```

3. **Use access token for authenticated requests**
   ```bash
   curl -X POST http://localhost:8000/api/posts/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "content": "My first post!"
     }'
   ```

### Example Workflow

1. Register and authenticate users
2. Create posts with text and media content
3. Add comments to engage with posts
4. Like posts to show appreciation
5. Follow other users to build connections
6. View personalized feed with posts from followed users

## Authentication

This API uses JWT (JSON Web Token) for stateless authentication:

- **Access tokens** are short-lived (1 hour default) for API requests
- **Refresh tokens** are longer-lived (7 days default) for obtaining new access tokens
- Include access token in request headers: `Authorization: Bearer <token>`

### Token Refresh Example

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

## Media Handling

- **Supported formats**: JPEG, PNG, GIF, MP4, MOV
- **Storage location**: `/media/` directory (configurable)
- **File validation**: Automatic format and size validation
- **Production recommendation**: Use cloud storage (AWS S3, Google Cloud Storage)

## Testing

Run the test suite:

```bash
# Run all tests
python manage.py test

# Run tests with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## Development

### Code Style

This project follows:
- PEP 8 Python style guide
- Django coding conventions
- RESTful API design principles

### Database Schema

Key models include:
- **User**: Extended Django user model
- **Post**: User-generated content with metadata
- **Comment**: Nested comments on posts
- **Like**: User-post relationship for likes
- **Follow**: User-user relationship for follows

## Future Enhancements

- [ ] Real-time notifications system
- [ ] Hashtag and mention functionality
- [ ] Advanced search and filtering
- [ ] Content moderation tools
- [ ] Analytics and reporting
- [ ] Mobile app integration
- [ ] Third-party OAuth integration
- [ ] Caching layer for improved performance

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Oladimeji Toba**
- GitHub: [@Justsmtp](https://github.com/Justsmtp)
- LinkedIn: [Oladimeji Toba](https://linkedin.com/in/oladimeji-toba)

## Support

If you have any questions or need help with setup, please:
1. Check the [Issues](https://github.com/Justsmtp/social-media-api/issues) page
2. Create a new issue with detailed information
3. Contact the author through GitHub or LinkedIn

---

⭐ **If you found this project helpful, please consider giving it a star!**