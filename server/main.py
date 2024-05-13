from flask import Blueprint, render_template
from flask.helpers import url_for
from werkzeug.utils import redirect
from .models import User_Stocks, User
from . import create_app
from flask_login import current_user

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/profile")
def profile():
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
        balance = user.total_balance
        user_stocks = User_Stocks.query.filter_by(user_id=current_user.id).all()
        print(user_stocks)
        return render_template("profile.html", balance=balance, user_stocks=user_stocks)
    else:
        return redirect(url_for("auth.login"))
