from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute("SELECT * FROM ravintolat")
    ravintolat = result.fetchall()
    return render_template("index.html",ravintolat=ravintolat)



