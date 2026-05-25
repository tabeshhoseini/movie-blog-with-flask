# 🎬 Movie Blog Manager

A simple movie blog web application built with Flask to learn the fundamentals of web development, including database operations and HTTP methods.

> **Note:** The HTML templates, CSS styles, and frontend design were generated with the assistance of AI. The Python backend, Flask routes, database logic, and application structure were written as part of the learning process.

## 📚 About This Project

This is a **learning project** created to practice and understand:
- Working with **SQLite** database using SQLAlchemy ORM
- Implementing **CRUD operations** (Create, Read, Update, Delete)
- Understanding **HTTP methods** (GET, POST) in a Flask application
- Building **RESTful routes** for web applications
- Handling **form submissions** and data validation
- Implementing **search functionality**
- Working with **Jinja2 templates**
- Building responsive web interfaces with CSS

## ✨ Features

- 📝 Create new movie blog posts with title, director, year, and rating
- 📋 View all movie blogs on the home page
- ✏️ Edit existing blog posts
- 🗑️ Delete blog posts with confirmation
- 🔍 Search movies by title or director
- 🌐 RTL support for Farsi/Persian text in reviews
- 📱 Responsive design for mobile and desktop

## 🛠️ Technologies Used

- **Backend:** Python, Flask
- **Database:** SQLite with SQLAlchemy ORM
- **Frontend:** HTML, CSS, Jinja2 Templates (AI-assisted)
- **HTTP Methods:** GET, POST

## 🚀 Quick Start (No Manual Installation!)

### Windows Users
1. Extract the project folder
2. **Double-click `run.bat`**
3. Wait for dependencies to install automatically
4. Open your browser to `http://127.0.0.1:5000`

### Mac/Linux Users
1. Extract the project folder
2. Open Terminal in the project folder
3. Run: `chmod +x run.sh && ./run.sh`
4. Open your browser to `http://127.0.0.1:5000`

### Manual Installation (Alternative)
If the automatic scripts don't work, follow these steps:

1. **Make sure Python is installed (3.8 or higher)**
2. **Open terminal/command prompt in the project folder**
3. **Install dependencies:**
```bash
pip install -r requirements.txt