# Development Guide - Adding Features to SkillConnect

## Current State

You now have a simple, working POC with:
- User registration and login
- User profiles with skills
- Post creation and browsing
- SQLite database

## How to Add New Features

### 1. Adding a New Field to User Profile

**Example: Add "location" field**

1. Update the model (`app/models/__init__.py`):
```python
class User(Base):
    # ... existing fields ...
    location = Column(String(255), nullable=True)
```

2. Update the registration form in `main.py`:
```python
# In register_page function
<div class="form-group">
    <label>Location</label>
    <input type="text" name="location">
</div>

# In register function
location: str = Form(None),
# Then add to User creation:
location=location,
```

3. Display in profile (`profile` function):
```python
{f"<p><strong>Location:</strong> {user.location}</p>" if user.location else ""}
```

### 2. Adding Search Functionality

Add a search route in `main.py`:

```python
@app.get("/search", response_class=HTMLResponse)
async def search(
    q: str = None,
    user=Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    if q:
        posts = db.query(Post).filter(
            Post.title.contains(q) | Post.description.contains(q)
        ).all()
    else:
        posts = []
    
    # Render search results...
```

### 3. Adding Post Comments

1. Create Comment model:
```python
class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    post = relationship("Post", back_populates="comments")
    author = relationship("User")
```

2. Add relationship to Post:
```python
# In Post class
comments = relationship("Comment", back_populates="post")
```

3. Add comment form and display in post detail page

### 4. Adding User-to-User Messaging

1. Create Message model:
```python
class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

2. Add messaging routes
3. Add inbox/outbox views

### 5. Adding Image Upload for Profiles

1. Install Pillow: Add to `pyproject.toml`
```toml
dependencies = [
    # ... existing ...
    "pillow>=10.0.0",
]
```

2. Add file upload field and handling
3. Store images in `app/static/uploads/`

### 6. Adding Email Notifications

1. Install email library:
```toml
dependencies = [
    # ... existing ...
    "fastapi-mail>=1.4.0",
]
```

2. Configure email settings in `.env`
3. Add email sending functions

### 7. Better UI with CSS Framework

Add Tailwind CSS or Bootstrap:

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
```

Or use a local CSS file in `app/static/css/style.css`

### 8. Adding Skill Matching

```python
@app.get("/matches", response_class=HTMLResponse)
async def skill_matches(
    user=Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    if not user or not user.skills:
        return RedirectResponse("/")
    
    user_skills = [s.strip().lower() for s in user.skills.split(",")]
    
    # Find posts that match user's skills
    matching_posts = []
    for post in db.query(Post).all():
        if post.required_skills:
            post_skills = [s.strip().lower() for s in post.required_skills.split(",")]
            if any(skill in post_skills for skill in user_skills):
                matching_posts.append(post)
    
    # Render matches...
```

## Best Practices

1. **Database Changes**: Delete `skillconnect.db` and restart the app to recreate tables after model changes

2. **Testing**: Test each feature in the browser before moving to the next

3. **Incremental Changes**: Add one feature at a time

4. **Keep it Simple**: Don't over-complicate the code structure

5. **Use Forms**: FastAPI's Form handling makes it easy to process form data

6. **Error Handling**: Add try-except blocks for database operations

## Common Patterns

### Adding a New Page

```python
@app.get("/new-page", response_class=HTMLResponse)
async def new_page(user=Depends(get_current_user_optional)):
    content = """
    <div class="card">
        <h2>New Page</h2>
        <p>Content here</p>
    </div>
    """
    return render_html("New Page", content, user)
```

### Adding API Endpoint

```python
from fastapi.responses import JSONResponse

@app.get("/api/posts")
async def api_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return JSONResponse([{
        "id": p.id,
        "title": p.title,
        "description": p.description
    } for p in posts])
```

### Protecting Routes (Login Required)

```python
from app.auth.auth import get_current_user

@app.get("/protected")
async def protected_page(user=Depends(get_current_user)):
    # User must be logged in to access this
    pass
```

## Project Evolution Path

1. ✅ **Phase 1 (Current)**: Basic POC
   - User auth
   - Posts
   - Feed

2. **Phase 2**: Enhanced Discovery
   - Search
   - Filters
   - Skill matching

3. **Phase 3**: Interaction
   - Comments
   - Likes
   - Bookmarks

4. **Phase 4**: Communication
   - Messaging
   - Notifications
   - Email alerts

5. **Phase 5**: Polish
   - Better UI
   - Images
   - Analytics
   - Admin panel

## Useful Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pydantic Docs](https://docs.pydantic.dev/)

Happy coding! 🚀
