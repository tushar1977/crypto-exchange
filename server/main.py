from flask import Blueprint, render_template
from flask.helpers import url_for
from werkzeug.utils import redirect
from .models import User_Stocks
from . import create_app
from flask_login import current_user

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/profile")
def profile():
    if current_user.is_authenticated:
        user_stocks = User_Stocks.query.filter_by(user_id=current_user.id).all()

        stocks = []
        quantities = []

        for stock in user_stocks:
            stocks.append(stock.stock)
            quantities.append(stock.quantity)

        return render_template("profile.html", stocks=stocks, quantities=quantities)
    else:
        return redirect(url_for("auth.login"))
