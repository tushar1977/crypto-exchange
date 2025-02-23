import bcrypt
from flask import Blueprint, jsonify
import secrets
from eth_account import Account
from flask_login.utils import request, current_user
from . import db
from server.models import User_Wallet
import web3


app_main = Blueprint("app_main", __name__)

Account.enable_unaudited_hdwallet_features()


def create_wallet():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    print("SAVE BUT DO NOT SHARE THIS:", private_key)
    acct = Account.from_key(private_key)
    print("Address:", acct.address)
    return private_key, acct.address


@app_main.route("/mainnet/create_wallet", methods=["POST", "GET"])
def wallet():
    if current_user.is_authenticated:
        password = request.form.get("password")
        user = User_Wallet.query.filter_by(user_id=current_user.id).first()

        private_key, account = create_wallet()
        salt = bcrypt.gensalt(rounds=20)
        hashed_mnemonic = bcrypt.hashpw(private_key.encode("utf-8"), salt)
        wallet = User_Wallet(
            user_id=current_user.id,
            account_add=account,
            account_private=hashed_mnemonic,
        )

        db.session.add(wallet)
        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "account": account,
                "private_key": private_key,  # Only include this if you are sure it is secure to do so.
            }
        )
    else:
        return jsonify({"status": "error", "message": "User not authenticated"}), 401
