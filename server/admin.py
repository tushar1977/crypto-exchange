from flask import Blueprint, redirect, render_template, request
from flask.helpers import url_for
from .models import User
from . import db

ad = Blueprint("admin", __name__)


@ad.route("/server")
def admin():
    users = User.query.all()

    return render_template("admin.html", users=users)


@ad.route("/server", methods=["POST", "GET"])
def admin_panel():
    new_balance = request.form.get("total_balance")
    user_id = request.args.get("user_id")
    if user_id and new_balance:
        user = User.query.get(user_id)
        if user:
            user.total_balance = new_balance
            db.session.commit()
    return redirect(url_for("admin.admin"))
