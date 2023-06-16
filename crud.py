from typing import List
from sqlalchemy.orm import Session
from models import Post, Comment, User
from schemas import PostCreate, PostUpdate, CommentCreate, CommentUpdate

def create_post(db: Session, post: PostCreate, current_user: User):
    # Create a new post record in the database
    new_post = Post(title=post.title, content=post.content, author_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_post(db: Session, post_id: int):
    # Retrieve a specific post record from the database
    return db.query(Post).filter(Post.id == post_id).first()

def update_post(db: Session, post_id: int, post: PostUpdate, current_user: User):
    # Update a specific post record in the database
    existing_post = get_post(db, post_id)
    existing_post.title = post.title
    existing_post.content = post.content
    db.commit()
    db.refresh(existing_post)
    return existing_post

def delete_post(db: Session, post_id: int, current_user: User):
    # Delete a specific post record from the database
    post = get_post(db, post_id)
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}

def create_comment(db: Session, comment: CommentCreate, current_user: User):
    # Create a new comment record in the database
    new_comment = Comment(content=comment.content, author_id=current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_comment(db: Session, comment_id: int):
    # Retrieve a specific comment record from the database
    return db.query(Comment).filter(Comment.id == comment_id).first()

def update_comment(db: Session, comment_id: int, comment: CommentUpdate, current_user: User):
    # Update a specific comment record in the database
    existing_comment = get_comment(db, comment_id)
    existing_comment.content = comment.content
    db.commit()
    db.refresh(existing_comment)
    return existing_comment

def delete_comment(db: Session, comment_id: int, current_user: User):
    # Delete a specific comment record from the database
    comment = get_comment(db, comment_id)
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted"}

def get_comments_by_post_id(db: Session, post_id: int) -> List[Comment]:
    return db.query(Comment).filter_by(post_id=post_id).all()