from app import app, db
from flask_sqlalchemy import SQLAlchemy


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(80))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    admin = db.Column(db.Boolean)
    #__table_args__ = (CheckConstraint(admin.in_([1, 2])), )

    #customers = db.relationship("Customer", secondary="user_customer", backref = 'customers')
    #password_hash = Column(String(128), nullable = False)

    def __init__(self, public_id, username, password, admin):
        self.public_id = public_id
        self.username = username
        self.password = password
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.admin = admin

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            "public_id" : self.public_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            "admin" : self.admin
        }

#admin_types = db.Table('admin_types', 
#    db.Column(db.Integer, primary_key=True)
#    db.Column(db.String(80)
#    )


