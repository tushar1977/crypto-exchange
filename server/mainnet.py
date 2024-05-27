import bcrypt
from flask import Blueprint
from eth_account import Account
from flask_login.utils import request, current_user
from . import db
from server.models import User_Wallet


app_main = Blueprint("app_main", __name__)

Account.enable_unaudited_hdwallet_features()


def create_wallet(password):
    acc, phase = Account.create_with_mnemonic()
    encrypted = Account.encrypt(acc, password)

    return acc, phase, encrypted


def get_private_key(encrpted_key, password):
    Account.decrypt(encrpted_key, password)


@app_main.route("/mainnet/create_wallet")
def wallet():
    if current_user.is_authenticated:
        password = "tushar" or request.form.get("password")
        user = User_Wallet.query.filter_by(user_id=current_user.id).first()
        if user:
            return "Already wallet created"
        acc, phase, encrypted = create_wallet(password)
        salt = bcrypt.gensalt(rounds=20)
        hashed = bcrypt.hashpw(phase.encode("utf-8"), salt)
        wallet = User_Wallet(
            user_id=current_user.id, account_add=acc, account_memonic=hashed
        )
        db.session.add(wallet)
        db.session.commit()
