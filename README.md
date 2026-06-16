# Auth + Message Board

A full-stack web application built with Django, Python, and SQLite featuring user authentication, a social message board, and an admin panel.

## Features

- User registration and login with secure authentication
- Session management and protected routes
- Message board with post creation, comments, and likes
- User profile pages
- Follow system and notifications
- Admin panel for managing users and content

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite
- **Frontend:** HTML, CSS
- **Auth:** Django built-in authentication system

## Getting Started

### Prerequisites

- Python 3.x
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/swills123/loginReg.git
cd loginReg
```

2. Install dependencies:
```bash
pip install django
```

3. Navigate to the app directory:
```bash
cd apps
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

6. Open your browser and go to `http://localhost:8000`

## Project Structure

```
apps/
├── accounts/          # User registration, login, and authentication
├── messageboard/      # Posts, comments, likes, follows, notifications
└── config/            # Project settings and URL configuration
```

## Screenshots

Coming soon.

## Author

Scott Wills
[github.com/swills123](https://github.com/swills123)
