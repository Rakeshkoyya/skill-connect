# SkillConnect - Simple POC Platform 🚀

A minimal platform where users can share their skills, post startup ideas, and connect with others.

## 🌟 Features

✅ **Simple Authentication** - Login with username/phone + password  
✅ **User Profiles** - Add your skills and bio  
✅ **Post Ideas** - Share startup concepts and required resources  
✅ **Browse Feed** - View all ideas on the home page  
✅ **Zero Configuration** - SQLite database, no external setup

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite (embedded)
- **ORM**: SQLAlchemy
- **Auth**: JWT + Bcrypt
- **Package Manager**: UV

## 🏗️ Project Structure

```
skill-connect/
├── main.py                # Main app with all routes and HTML
├── app/
│   ├── config.py         # Settings and configuration
│   ├── auth/
│   │   └── auth.py       # Authentication logic
│   ├── database/
│   │   └── connection.py # Database setup
│   └── models/
│       └── __init__.py   # User and Post models
├── pyproject.toml        # Dependencies
├── env.template          # Environment variables template
├── skillconnect.db       # SQLite database (auto-created)
└── .env                  # Your environment config
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Copy environment template
copy env.template .env

# Install dependencies
uv sync
```

### 2. Run the Application

```bash
# Start the server
uv run python main.py
```

### 3. Open Browser

Visit: **http://localhost:8000**

## � Usage

1. **Register** - Create account with username/phone + password
2. **Add Skills** - Enter your skills (e.g., "Python, Design, Marketing")
3. **Post Ideas** - Share your startup idea and required resources
4. **Browse Feed** - View all ideas on the home page
5. **View Profile** - See your info and posts

## 🗄️ Database

- **Type**: SQLite (no setup required)
- **Location**: `./skillconnect.db`
- **Auto-created**: On first run
- **Schema**:
  - **users**: username, phone, password_hash, skills, bio
  - **posts**: title, description, required_skills, author_id

## 🔑 Environment Variables

Edit `.env` file:

```env
# Database
DATABASE_URL=sqlite:///./skillconnect.db

# Security (change in production!)
SECRET_KEY=change-this-to-a-random-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# App
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

## � Documentation

- **GETTING_STARTED.md** - Quick start guide
- **DEVELOPMENT_GUIDE.md** - How to add features
- **CHANGES.md** - What was changed/simplified

## 🎯 Next Steps

Ready to enhance? Check `DEVELOPMENT_GUIDE.md` for:
- Adding search and filters
- Implementing comments
- User messaging
- File uploads
- Better UI with CSS frameworks

## 🐳 Alternative: Run with Docker (Optional)

If you prefer Docker:

```bash
docker build -t skillconnect .
docker run -p 8000:8000 skillconnect
```

## 🤝 Contributing

This is a POC project. Feel free to:
1. Fork the repo
2. Add features incrementally
3. Keep it simple!

## 📄 License

MIT License - feel free to use for your projects!

---

**Built with ❤️ for simplicity and rapid prototyping**