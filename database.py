from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import config

Base = declarative_base()
engine = create_engine(config.Config.DATABASE_URL)
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    join_date = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False)
    notifications = Column(Boolean, default=True)
    language = Column(String(10), default='ru')
    city = Column(String(100))


class Reminder(Base):
    __tablename__ = 'reminders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    text = Column(String(500), nullable=False)
    reminder_time = Column(DateTime, nullable=False)
    is_completed = Column(Boolean, default=False)


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(200))
    content = Column(String(2000))
    created_at = Column(DateTime, default=datetime.utcnow)
    category = Column(String(100))


def init_db():
    Base.metadata.create_all(engine)


def get_or_create_user(session, telegram_id, username, first_name, last_name):
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        session.add(user)
        session.commit()
    return user