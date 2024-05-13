import json
from os import wait3
from flask import Blueprint, redirect, request, render_template, flash, url_for
from flask.json import jsonify
from flask_login import current_user
from sqlalchemy import Date
from sqlalchemy.sql import false
from .models import User, User_Stocks
from . import create_app, db
from datetime import date

main = Blueprint("stock", __name__)

stock_data_list = [
    {"stock": "BTC", "price": 69000, "market_cap": 100000},
    {"stock": "ETH", "price": 2900, "market_cap": 10000},
]


@main.route("/stock")
def stock_panel():
    return render_template(
        "stock_panel.html",
        stock_data_list=stock_data_list,
        get_current_price=get_current_price,
    )


def get_current_price(stock_name):
    with open("stock2.json", "r") as f:
        stock_data = json.load(f)

    for item in stock_data:
        if item["stock"] == stock_name:
            return item["price"]

        # elif not item["stock"] == stock_name:
        # with open("stock2.json", "w") as f:
        # json.dump(stock_data_list, f)


def get_market_cap(stock_name):
    with open("stock2.json", "r") as f:
        data = json.load(f)

    for item in data:
        if item["stock"] == stock_name:
            if "market_cap" in item:
                return item["market_cap"]
            else:
                return None

    return None


@main.route("/stock", methods=["POST"])
def stock_post():
    if current_user.is_authenticated:
        global stock_name

        stock_name = request.form.get("stock_name")
        stock_quantity = int(request.form.get("quantity"))
        price_str = request.form.get("price")
        user = User.query.filter_by(id=current_user.id).first()

        action = request.form["action"]
        market_cap = int(get_market_cap(stock_name))
        print(market_cap)
        user_stock = User_Stocks.query.filter_by(
            user_id=current_user.id, stock=stock_name
        ).first()
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
            sell_amt = round(old_price * stock_quantity)
            if user.total_balance < sell_amt:
                print("not enought usdt")
                return redirect(url_for("stock.stock_panel"))
            total_supply = market_cap * old_price
            percent_change = (sell_amt / total_supply) * 100
            new_price = round(old_price + ((percent_change * old_price) / 100), 2)
            user.total_balance -= sell_amt
            db.session.commit()
            print(user.total_balance)
            for item in stock_data:
                if item["stock"] == stock_name:
                    item["price"] = str(new_price)
                    break

            if user_stock:
                user_stock.quantity += stock_quantity
                db.session.commit()
                print(user_stock.quantity)

            else:
                new_stock = User_Stocks(
                    user_id=current_user.id,
                    stock=stock_name,
                    quantity=stock_quantity,
                    price=get_current_price(stock_name),
                    date=date.today(),
                )

                db.session.add(new_stock)
                db.session.commit()
        elif action == "sell":
            sell_amt = old_price * stock_quantity

            if user_stock.quantity < stock_quantity:
                print("not enough crypto")

                return redirect(url_for("stock.stock_panel"))
            total_supply = market_cap * old_price
            percent_change = (sell_amt / total_supply) * 100
            new_price = round(old_price - ((percent_change * old_price) / 100), 2)
            user.total_balance += sell_amt
            db.session.commit()

            print(user.total_balance)
            for item in stock_data:
                if item["stock"] == stock_name:
                    item["price"] = str(new_price)
                    break

            if user_stock:
                user_stock.quantity -= stock_quantity
                db.session.commit()
                print(user_stock.quantity)
            else:
                new_stock = User_Stocks(
                    user_id=current_user.id,
                    stock=stock_name,
                    quantity=stock_quantity,
                    price=get_current_price(stock_name),
                    date=date.today(),
                )

                db.session.add(new_stock)
                db.session.commit()

        with open("stock2.json", "w") as f:
            json.dump(stock_data, f, indent=2)

        return render_template(
            "stock_panel.html",
            stock_data_list=stock_data_list,
            get_current_price=get_current_price,
        )

    else:
        return render_template("error.html")
