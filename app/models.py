from app import db
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    is_admin = db.Column(db.Boolean, default= 0)
    reg_date = db.Column(db.DateTime,default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default= 0)

