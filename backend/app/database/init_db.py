"""Initial DB setup helper"""
from .session import engine
from ..database.base import Base


def init_db():
    Base.metadata.create_all(bind=engine)
