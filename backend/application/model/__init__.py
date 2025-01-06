from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    """Intializing the database"""
    
    from . import model
    return db