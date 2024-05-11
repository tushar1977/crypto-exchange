import json
from os import wait3
from flask import Blueprint, redirect, request, render_template, flash, url_for
from flask.json import jsonify
from flask_login import current_user
from sqlalchemy.sql import false
from .models import User, User_Stocks
from . import create_app, db
from datetime import datetime

main = Blueprint("stock", __name__)


@main.route("/stock", methods=["GET"])
def stock_panel():
    stock_name = "AAPL"  # Replace with your stock name
    current_price = get_current_price(stock_name)
    return render_template("stock_panel.html", price=current_price)


def get_current_price(stock_name):
    with open("stock2.json", "r") as f:
        stock_data = json.load(f)
    for item in stock_data:
        if item["stock"] == stock_name:
            return item["price"]
    return 3000  # If the stock is not found, return the initial price of 3000


@main.route("/stock", methods=["POST"])
def stock_post():
    if current_user.is_authenticated:
        stock_name = request.form.get("stock_name")
        stock_quantity = int(request.form.get("quantity"))
        price_str = request.form.get("price")
        action = request.form["action"]
        market_cap = 100000
        user = User.query.filter_by(id=current_user.id).first()
        balance = user.total_balance
        with open("stock2.json", "r") as f:
            stock_data = json.load(f)

        for item in stock_data:
            if item["stock"] == stock_name:
                if item["price"] == "":
                    curr_rate = 0.0
                curr_rate = float(item["price"])
                break
        else:
            curr_rate = 3000.00  # Set a default price if the stock is not found

        old_price = float(price_str) if price_str else float(curr_rate)

        if action == "buy":
            sell_amt = old_price * stock_quantity
            if balance < sell_amt:
                flash("Not enought USDT")
            total_supply = market_cap * old_price
            percent_change = (sell_amt / total_supply) * 100
            new_price = old_price + ((percent_change * old_price) / 100)
            balance -= sell_amt
            print(balance)
            db.session.commit()
            for item in stock_data:
                if item["stock"] == stock_name:
                    item["price"] = str(new_price)
                    break
        elif action == "sell":
            sell_amt = old_price * stock_quantity
            total_supply = market_cap * old_price
            percent_change = (sell_amt / total_supply) * 100
            new_price = old_price - ((percent_change * old_price) / 100)
            balance += sell_amt
            print(balance)
            db.session.commit()
            for item in stock_data:
                if item["stock"] == stock_name:
                    item["price"] = str(new_price)
                    break

        with open("stock2.json", "w") as f:
            json.dump(stock_data, f, indent=2)

        price = get_current_price(stock_name)
        new_stock = User_Stocks(
            user_id=current_user.id,
            stock=stock_name,
            quantity=stock_quantity,
            price=price,
            date=datetime.now(),
        )
        db.session.add(new_stock)
        db.session.commit()

        return render_template("stock_panel.html", price=new_price)
    else:
        return render_template("error.html")
