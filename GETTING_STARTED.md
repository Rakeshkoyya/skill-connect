# Quick Start Guide

## Getting Started in 3 Steps

### Step 1: Setup Environment
```bash
# Copy the environment template
copy env.template .env
```

### Step 2: Install Dependencies
```bash
uv sync
```

### Step 3: Run the Application
```bash
uv run python main.py
```

Then open your browser to: **http://localhost:8000**

## What You Can Do

1. **Register** - Create a new account
   - Username (required)
   - Phone number (optional)
   - Password (required)
   - Skills (e.g., "Python, Design, Marketing")
   - Bio

2. **Login** - Access your account
   - Use your username or phone
   - Enter your password

3. **Browse Ideas** - View all startup ideas on the home page

4. **Post Your Idea** - Share your startup concept
   - What's your idea?
   - What skills/resources do you need?

5. **View Profile** - See your info and all your posts

## Features

✅ Simple username/phone + password authentication  
✅ User profiles with skills and bio  
✅ Post startup ideas and required resources  
✅ Browse feed of all ideas  
✅ SQLite database (no external setup needed)  
✅ Clean, responsive UI  

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Lightweight database
- **JWT** - Secure authentication
- **Bcrypt** - Password hashing

## Next Steps

Once you're comfortable with the basics, you can:
- Add search and filtering
- Implement user messaging
- Add skill matching recommendations
- Enable post comments
- Upload profile pictures

Enjoy building with SkillConnect! 🚀
