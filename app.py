import os

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo

app = Flask(__name__)
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


def hash_to_letter(hash_inp):
    hacker = mongo.db.hackers.find_one_or_404({"hash": hash_inp})
    return hacker["letter"]


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
