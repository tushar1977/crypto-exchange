from sqlalchemy.orm import relationship
from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    total_balance = db.Column(db.Integer, default=100000)
    stocks = relationship("User_Stocks", backref="User")


class User_Stocks(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Define the primary key
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    stock = db.Column(db.String(100))
    quantity = db.Column(db.Integer)

    price = db.Column(db.Integer)
    date = db.Column(db.String)


class Stocks(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Add this line
    stock_name = db.Column(db.String(100))
    stock_price = db.Column(db.Integer)
