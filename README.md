# Zlores

Zlores is a social blog platform developed with Django. Users can register, create posts, view posts by others, and leave comments. Additionally, the platform features user profiles, a follow system, and like/dislike functionalities.

## Features

- ✅ User registration, login, and password reset
- 👤 Profile creation and update
- 🧑‍🤝‍🧑 Follow and unfollow users
- 📝 Create, update, and delete posts
- 💬 Comment on posts and delete comments
- 👍👎 Like and dislike posts
- 🏠 Featured posts on the homepage

## Technologies

- Python 3 & Django 5.2.1
- SQLite (default database)
- HTML, CSS (Static files)
- Django Template Engine

## Installation

```bash
# Create a virtual environment
python -m venv env
source env/bin/activate  # For Windows: env\\Scripts\\activate

# Install required packages
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start the development server
python manage.py runserver
