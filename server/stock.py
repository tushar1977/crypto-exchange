import json
from os import wait3
from flask import Blueprint, redirect, request, render_template, flash, url_for
from flask_login import current_user
from .models import User, User_Stocks
from . import create_app, db
from datetime import datetime

main = Blueprint("stock", __name__)


@main.route("/stock")
def stock():
    return render_template("stock_panel.html")


@main.route("/stock", methods=["POST"])
def stock_post():
    if current_user.is_authenticated:
        stock_name = "AAPL"
        stock_quantity = int(request.form.get("quantity"))
        old_price = 3000
        action = request.form["action"]

        user = User.query.filter_by(id=current_user.id).first()

        total_amt = old_price * stock_quantity

        if action == "buy":
            new_price = int(old_price * stock_quantity + total_amt / stock_quantity)

            print(new_price)

            new_stock = User_Stocks(
                user_id=current_user.id,
                stock=stock_name,
                quantity=stock_quantity,
                price=old_price,
                date=datetime.now(),
            )

            user.total_balance -= total_amt

            db.session.add(new_stock)

            db.session.commit()
        if action == "sell":
            sell_amt = old_price * stock_quantity

            user.total_balance += sell_amt

            new_price = (old_price * stock_quantity - total_amt) / stock_quantity

            print(new_price)
            print("balance" + user.balance)
            new_stock = User_Stocks(
                user_id=current_user.id,
                stock=stock_name,
                quantity=stock_quantity,
                price=old_price,
                date=datetime.now(),
            )
            user.total_balance -= total_amt
            db.session.add(new_stock)

            db.session.commit()

        return redirect(url_for("stock.stock"))
    else:
        return render_template("error.html")
