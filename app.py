from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from datetime import date, datetime, timedelta

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute("SELECT * FROM ravintolat")
    ravintolat = result.fetchall()
    result = db.session.execute("SELECT * FROM lounaat WHERE pvm = CURRENT_DATE")
    lounaat = result.fetchall()
    return render_template("index.html",ravintolat=ravintolat, lounaat=lounaat)

@app.route("/ravintola/<int:id>")
def ravintolat(id):
    sql = "SELECT * FROM ravintolat WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    ravintola = result.fetchall()
    sql = "SELECT * FROM lounaat WHERE ravintola_id=:id"
    result = db.session.execute(sql, {"id":id})
    lounaat = result.fetchall()
    tanaan = date.today().strftime("%Y-%m-%d")
    huomenna = date.today() + timedelta(days=1)
    huomenna = huomenna.strftime("%Y-%m-%d")
    return render_template("ravintola.html", id=id, ravintola=ravintola, lounaat=lounaat, tanaan=tanaan, huomenna=huomenna)

