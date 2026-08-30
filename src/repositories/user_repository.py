from ..models import User
from ..db.session import Session

def create_user(user: User) -> User:
    try:
        with Session() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
        return user
    except Exception as e:
        raise e
    
def get_user(id: int) -> User:
    try:
        with Session() as session:
            user = session.get(User, id)
        return user
    except Exception as e:
        raise e
    
def delete_user(id: int):
    try:
        with Session() as session:
            user = session.get(User, id)
            if user:
                session.delete(user)
                session.commit()
            else:
                raise Exception("User not found.")
    except Exception as e:
        raise e
    
def update_user(id: int, user: User) -> User:
    try:
        with Session() as session:
            existing_user = session.get(User, id)
            
            if existing_user:
                existing_user.username = user.username
                session.commit()
                session.refresh(existing_user)
                return existing_user
            else:
                raise Exception("User not found.")
    except Exception as e:
        raise e