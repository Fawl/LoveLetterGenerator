from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from datetime import datetime
from generator import LoveLetterGenerator
from hashlib import md5

app = Flask(__name__, static_folder="static", static_url_path="")

def validate_name(in_name: str) -> bool:
    return ''.join(in_name.split()).isalpha()

@app.route("/", methods=["GET"])
@cross_origin()
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def get_love_letter():
    name = request.form.get("username")

    if name:
        if validate_name(name):
            timestamp = datetime.timestamp(datetime.now()) * 1000
            gen = LoveLetterGenerator(name=name, rand_seed=timestamp)

            return render_template("generate.html", love_letter=gen.get_loveletter())
        else:
            return render_template("generate.html", love_letter="INVALID NAME")

    else:
        # invalid request
        return render_template("generate.html", love_letter="NO NAME")



if __name__ == '__main__':
    cors = CORS(app)
    app.run()