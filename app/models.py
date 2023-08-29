from app import db
from datetime import datetime


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String)
    document_date = db.Column(db.Date)
    forwarder = db.Column(db.String)
    client = db.Column(db.String)
    start = db.Column(db.String(length=2))
    target = db.Column(db.String(length=2))
    start_route_date = db.Column(db.Date) # date using to calculate currency
    currency = db.Column(db.String(length=3))
    exchange_rate = db.Column(db.Float)
    customer_rate = db.Column(db.Float)
    our_rate = db.Column(db.Float)
    profit = db.Column(db.Float)
    is_row_edit = db.Column(db.Boolean)

class Currency(db.Model):
    __tablename__ = 'currency'
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(length=3))
    date = db.Column(db.Date)
    exchange_rate = db.Column(db.Float)