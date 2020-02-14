import os

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo

app = Flask(__name__)
bcrypt = Bcrypt(app=app)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)


@app.route('/', methods=["GET"])
def homepage():
    return render_template('index.html')


@app.route('/', methods=["POST"])
def process():
    user_inp = request.get_json()
    if user_inp and "hash" in user_inp.keys():
        letter = hash_to_letter(user_inp["hash"])
        if letter:
            return jsonify({"msg": "ok", "letter": letter})
    return jsonify({"msg": "failed"})


# $2b$12$ must be added before using the check hash function
def letter_to_hash(letter):
    return bcrypt.generate_password_hash(letter, 14).decode().split("$")[1:][2]


def hash_to_letter(hash_inp):
    hacker = mongo.db.hackers.find_one_or_404({"hash": hash_inp})
    if bcrypt.check_password_hash(f"$2b$12${hash_inp}", hacker["letter"]):
        return hacker["letter"]
    return ""


if __name__ == '__main__':
    app.run(host="0.0.0.0")
