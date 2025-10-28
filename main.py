from fastapi import FastAPI, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database.connection import init_db, get_db
from app.auth.auth import (
    get_password_hash, 
    authenticate_user, 
    create_access_token,
    get_user_by_username,
    get_current_user_optional
)
from app.models import User, Post
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - Create tables
    await init_db()
    yield
    # Shutdown


# Initialize FastAPI app
app = FastAPI(title="SkillConnect", description="Connect Skills with Opportunities", lifespan=lifespan)

# Mount static files if directory exists
try:
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
except:
    pass


def render_html(title: str, content: str, user=None) -> str:
    """Simple HTML template"""
    nav = f"""
    <nav style="background: #2563eb; color: white; padding: 1rem;">
        <div style="max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center;">
            <h1 style="margin: 0;"><a href="/" style="color: white; text-decoration: none;">SkillConnect</a></h1><h3>for yatris of 2025</h3>
            <div>
                <a href="/" style="color: white; margin: 0 1rem; text-decoration: none;">Home</a>
                {"<a href='/profile' style='color: white; margin: 0 1rem; text-decoration: none;'>Profile</a>" if user else ""}
                {"<a href='/logout' style='color: white; margin: 0 1rem; text-decoration: none;'>Logout</a>" if user else "<a href='/login' style='color: white; margin: 0 1rem; text-decoration: none;'>Login</a>"}
                {"" if user else "<a href='/register' style='color: white; margin: 0 1rem; text-decoration: none;'>Register</a>"}
            </div>
        </div>
    </nav>
    """
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title} - SkillConnect</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: Arial, sans-serif; background: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem; }}
            .card {{ background: white; padding: 2rem; border-radius: 8px; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .form-group {{ margin-bottom: 1rem; }}
            label {{ display: block; margin-bottom: 0.5rem; font-weight: bold; }}
            input, textarea {{ width: 100%; padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px; }}
            button, .btn {{ background: #2563eb; color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; }}
            button:hover, .btn:hover {{ background: #1e40af; }}
            .post {{ background: white; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .post h3 {{ color: #2563eb; margin-bottom: 0.5rem; }}
            .post-meta {{ color: #666; font-size: 0.9rem; margin-top: 0.5rem; }}
            .skills {{ background: #e0e7ff; color: #2563eb; padding: 0.25rem 0.75rem; border-radius: 12px; display: inline-block; margin: 0.25rem; font-size: 0.85rem; }}
        </style>
    </head>
    <body>
        {nav}
        <div class="container">
            {content}
        </div>
    </body>
    </html>
    """


@app.get("/", response_class=HTMLResponse)
async def home(user=Depends(get_current_user_optional), db: Session = Depends(get_db)):
    """Home page with post feed"""
    posts = db.query(Post).order_by(Post.created_at.desc()).limit(20).all()
    
    posts_html = ""
    for post in posts:
        skills_html = ""
        if post.required_skills:
            for skill in post.required_skills.split(","):
                skills_html += f'<span class="skills">{skill.strip()}</span>'
        
        posts_html += f"""
        <div class="post">
            <h3>{post.title}</h3>
            <p>{post.description}</p>
            <div>{skills_html}</div>
            <div class="post-meta">Posted by {post.author.username} • {post.created_at.strftime('%Y-%m-%d')}</div>
        </div>
        """
    
    if not posts_html:
        posts_html = "<p>No posts yet. Be the first to share an idea!</p>"
    
    content = f"""
    <div class="card">
        <h2>Welcome to SkillConnect</h2>
        <p>A platform where you can share your startup ideas and find skilled people to collaborate with.</p>
        {f"<a href='/new-post' class='btn' style='margin-top: 1rem;'>Post Your Idea</a>" if user else "<p style='margin-top: 1rem;'><a href='/login'>Login</a> or <a href='/register'>Register</a> to post ideas.</p>"}
    </div>
    <h2 style="margin: 2rem 0 1rem;">Recent Ideas</h2>
    {posts_html}
    """
    
    return render_html("Home", content, user)


@app.get("/login", response_class=HTMLResponse)
async def login_page():
    """Login page"""
    content = """
    <div class="card" style="max-width: 500px; margin: 2rem auto;">
        <h2>Login</h2>
        <form method="post" action="/login">
            <div class="form-group">
                <label>Username or Phone</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit">Login</button>
            <p style="margin-top: 1rem;">Don't have an account? <a href="/register">Register here</a></p>
        </form>
    </div>
    """
    return render_html("Login", content)


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """Handle login"""
    user = authenticate_user(db, username, password)
    if not user:
        content = """
        <div class="card" style="max-width: 500px; margin: 2rem auto;">
            <h2 style="color: red;">Login Failed</h2>
            <p>Invalid username or password.</p>
            <a href="/login" class="btn">Try Again</a>
        </div>
        """
        return render_html("Login Failed", content)
    
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
    )
    
    response = RedirectResponse("/", status_code=302)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response


@app.get("/register", response_class=HTMLResponse)
async def register_page():
    """Registration page"""
    content = """
    <div class="card" style="max-width: 500px; margin: 2rem auto;">
        <h2>Register</h2>
        <form method="post" action="/register">
            <div class="form-group">
                <label>Username *</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>Phone Number *</label>
                <input type="text" name="phone">
            </div>
            <div class="form-group">
                <label>Password *</label>
                <input type="password" name="password" required>
            </div>
            <div class="form-group">
                <label>Full Name</label>
                <input type="text" name="full_name">
            </div>
            <div class="form-group">
                <label>Your Skills (comma-separated)</label>
                <input type="text" name="skills" placeholder="Programmer, Designer, Marketing">
            </div>
            <div class="form-group">
                <label>Bio</label>
                <textarea name="bio" rows="3" placeholder="Tell us about yourself..."></textarea>
            </div>
            <button type="submit">Register</button>
            <p style="margin-top: 1rem;">Already have an account? <a href="/login">Login here</a></p>
        </form>
    </div>
    """
    return render_html("Register", content)


@app.post("/register")
async def register(
    username: str = Form(...),
    password: str = Form(...),
    phone: str = Form(None),
    full_name: str = Form(None),
    skills: str = Form(None),
    bio: str = Form(None),
    db: Session = Depends(get_db)
):
    """Handle registration"""
    # Check if username exists
    existing_user = get_user_by_username(db, username)
    if existing_user:
        content = """
        <div class="card" style="max-width: 500px; margin: 2rem auto;">
            <h2 style="color: red;">Registration Failed</h2>
            <p>Username already exists.</p>
            <a href="/register" class="btn">Try Again</a>
        </div>
        """
        return render_html("Registration Failed", content)
    
    # Create new user
    hashed_password = get_password_hash(password)
    new_user = User(
        username=username,
        phone=phone,
        password_hash=hashed_password,
        full_name=full_name,
        skills=skills,
        bio=bio,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Automatically log in the user after registration
    access_token = create_access_token(
        data={"sub": new_user.username},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
    )
    
    response = RedirectResponse("/", status_code=302)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response


@app.get("/logout")
async def logout():
    """Logout"""
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("access_token")
    return response


@app.get("/profile", response_class=HTMLResponse)
async def profile(user=Depends(get_current_user_optional), db: Session = Depends(get_db)):
    """User profile page"""
    if not user:
        return RedirectResponse("/login")
    
    # Get user's posts
    user_posts = db.query(Post).filter(Post.author_id == user.id).order_by(Post.created_at.desc()).all()
    
    posts_html = ""
    for post in user_posts:
        skills_html = ""
        if post.required_skills:
            for skill in post.required_skills.split(","):
                skills_html += f'<span class="skills">{skill.strip()}</span>'
        
        posts_html += f"""
        <div class="post">
            <h3>{post.title}</h3>
            <p>{post.description}</p>
            <div>{skills_html}</div>
            <div class="post-meta">{post.created_at.strftime('%Y-%m-%d')}</div>
        </div>
        """
    
    if not posts_html:
        posts_html = "<p>You haven't posted any ideas yet.</p>"
    
    skills_display = ""
    if user.skills:
        for skill in user.skills.split(","):
            skills_display += f'<span class="skills">{skill.strip()}</span>'
    
    content = f"""
    <div class="card">
        <h2>{user.full_name or user.username}</h2>
        <p><strong>Username:</strong> {user.username}</p>
        {f"<p><strong>Phone:</strong> {user.phone}</p>" if user.phone else ""}
        {f"<p><strong>Bio:</strong> {user.bio}</p>" if user.bio else ""}
        {f"<p><strong>Skills:</strong> {skills_display}</p>" if user.skills else ""}
        <a href="/new-post" class="btn" style="margin-top: 1rem;">Post New Idea</a>
    </div>
    <h2 style="margin: 2rem 0 1rem;">Your Posts</h2>
    {posts_html}
    """
    
    return render_html("Profile", content, user)


@app.get("/new-post", response_class=HTMLResponse)
async def new_post_page(user=Depends(get_current_user_optional)):
    """New post page"""
    if not user:
        return RedirectResponse("/login")
    
    content = """
    <div class="card" style="max-width: 800px; margin: 2rem auto;">
        <h2>Share Your Idea</h2>
        <form method="post" action="/new-post">
            <div class="form-group">
                <label>Title *</label>
                <input type="text" name="title" required>
            </div>
            <div class="form-group">
                <label>Description *</label>
                <textarea name="description" rows="5" required placeholder="Describe your startup idea and what you're looking for..."></textarea>
            </div>
            <div class="form-group">
                <label>Required Skills (comma-separated)</label>
                <input type="text" name="required_skills" placeholder="Python Developer, UI/UX Designer, Marketing Expert">
            </div>
            <button type="submit">Post Idea</button>
            <a href="/profile" style="margin-left: 1rem;">Cancel</a>
        </form>
    </div>
    """
    return render_html("New Post", content, user)


@app.post("/new-post")
async def create_post(
    title: str = Form(...),
    description: str = Form(...),
    required_skills: str = Form(None),
    user=Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Handle new post creation"""
    if not user:
        return RedirectResponse("/login")
    
    new_post = Post(
        title=title,
        description=description,
        required_skills=required_skills,
        author_id=user.id
    )
    
    db.add(new_post)
    db.commit()
    
    return RedirectResponse("/profile", status_code=302)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
