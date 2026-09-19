from ..models import User
from ..db.session import db

def create_user(user: User) -> User:
    try:
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user
    except Exception as e:
        raise e
    
def get_user(id: int) -> User:
    try:
        user = db.session.get(User, id)
        return user
    except Exception as e:
        raise e
    
def delete_user(id: int):
    try:
        user = db.session.get(User, id)
        if user:
            db.session.delete(user)
            db.session.commit()
        else:
            raise Exception("User not found.")
    except Exception as e:
        raise e
    
def update_user(id: int, user: User) -> User:
    try:
        existing_user = db.session.get(User, id)
        
        if existing_user:
            existing_user.username = user.username
            db.session.commit()
            db.session.refresh(existing_user)
            return existing_user
        else:
            raise Exception("User not found.")
    except Exception as e:
        raise e