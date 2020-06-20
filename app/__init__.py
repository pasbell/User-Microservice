import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Initialize application
app = Flask(__name__)

# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

db = SQLAlchemy(app)

from app import views

from app.views import user_blueprint
app.register_blueprint(user_blueprint,url_prefix="/api/")


"""
class Base(db.Model):
    id = db.Column(Integer, primary_key=True)
    db_config = "1"
 
    @classmethod
    def db_cxn(cls):
        engine = create_engine(cls.db_config)
        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        return session

    @classmethod
    def create(cls, **kw):
        obj = cls(**kw)
        session = cls.db_cxn()
        session.add(obj)
        session.commit()


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(cls=Base)
"""