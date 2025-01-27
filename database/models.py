from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    username = Column(String, nullable=True)
    full_name = Column(String)
    joined_date = Column(Date, default=date.today)
    is_active = Column(Boolean, default=True)
    conversion_count = Column(Integer, default=0)


engine = create_engine('sqlite:///bot_users.db')
session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
