from sqlalchemy import select, update, text, func
from sqlalchemy.orm import sessionmaker
from database.models import User, engine
from datetime import date


class UserService:
    def __init__(self):
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def get_user(self, user_id: int) -> User:
        result = self.session.execute(
            select(User).where(User.user_id == user_id)
        )
        return result.scalar_one_or_none()

    def create_user(self, user_data: dict) -> User:
        full_name = f"{user_data['first_name']} {user_data['last_name']}" if user_data['last_name'] else user_data['first_name']
        user = User(
            user_id=user_data['user_id'],
            username=user_data.get('username'),
            full_name=full_name
        )
        self.session.add(user)
        self.session.commit()
        return user

    def update_activity(self, user_id: int):
        self.session.execute(
            update(User)
            .where(User.user_id == user_id)
            .values(
                conversion_count=User.conversion_count + 1
            )
        )
        self.session.commit()

    def get_or_create_user(self, user_data: dict):
        created = False
        result = self.session.execute(
            select(User).where(User.user_id == user_data['user_id'])
        )
        user = result.scalar_one_or_none()
        if not user:
            full_name = f"{user_data['first_name']} {user_data['last_name']}" if user_data['last_name'] else user_data['first_name']
            user = User(
                user_id=user_data['user_id'],
                username=user_data.get('username'),
                full_name=full_name
            )
            self.session.add(user)
            self.session.commit()
            created = True
        return user, created

    def get_user_count(self):
        session = self.Session()
        count = session.query(User).count()
        return count

    def get_today_joined_user_count(self):
        count = self.session.query(User).filter(User.joined_date == date.today()).count()
        return count

    def get_top_5_user(self):
        users = self.session.query(User).order_by(text('-conversion_count')).limit(5)
        return users

    def get_conversion_count(self):
        count = self.session.query(func.sum(User.conversion_count)).scalar()
        return count    
