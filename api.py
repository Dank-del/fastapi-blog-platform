from fastapi import APIRouter, Depends
from auth_handler import create_jwt_token
from models import Comment, Post, User
from schemas import CommentCreate, PostCreate, PostUpdate
from crud import create_post, get_comments_by_post_id, update_post, delete_post
from auth import get_current_user
from fastapi import HTTPException
from fastapi.security import HTTPBasic
from schemas import UserCreate
from database import SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext

router = APIRouter()
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/posts", tags=["posts"])
async def create_post_api(post: PostCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_post(db, post, current_user)

# Define other CRUD endpoints for posts and comments

@router.put("/posts/{post_id}", tags=["posts"])
async def update_post_api(post_id: int, post: PostUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return update_post(db, post_id, post, current_user)

# Define other CRUD endpoints for posts and comments

@router.delete("/posts/{post_id}", tags=["posts"])
async def delete_post_api(post_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_post(db, post_id, current_user)

@router.get("/posts/{post_id}/comments", tags=["posts"])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    if comments := get_comments_by_post_id(db, post_id):
        return comments
    else:
        raise HTTPException(status_code=404, detail="Post not found")

# Define other CRUD endpoints for posts and comments

@router.post("/register", tags=["user"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    new_user = User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@router.post("/login", tags=["user"])
def login(credentials: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_jwt_token(user.id)
    return {"message": "Login successful", "token": token}

@router.get("/comments", tags=["comments"])
def get_comments(db: Session = Depends(get_db)):
    return db.query(Comment).all()

@router.post("/comments", tags=["comments"])
def create_comment(comment: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    new_comment = Comment(content=comment.content, author_id=current_user.id, post_id=comment.post_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return {"message": "Comment created"}

@router.put("/comments/{comment_id}", tags=["comments"])
def update_comment(comment_id: int, comment: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if existing_comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to update this comment")
    
    existing_comment.content = comment.content
    db.commit()
    return {"message": f"Comment {comment_id} updated"}

@router.delete("/comments/{comment_id}", tags=["comments"])
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if existing_comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this comment")
    
    db.delete(existing_comment)
    db.commit()
    return {"message": f"Comment {comment_id} deleted"}

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)