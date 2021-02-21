from app import app
import lounaat
import users
from flask import redirect, render_template, request, session
from datetime import date, datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/")
def index():
    ravintolat = lounaat.hae_ravintolat()
    lounaat_tanaan= lounaat.hae_lounaat_tanaan()
    return render_template("index.html",ravintolat=ravintolat, lounaat=lounaat_tanaan)

@app.route("/ravintola/<int:id>")
def ravintolat(id):
    ravintola = lounaat.hae_ravintola(id)

    lounaat_tanaan,lounaat_huomenna,lounaat_maanantai,lounaat_tiistai,lounaat_keskiviikko,lounaat_torstai,lounaat_perjantai = lounaat.hae_ravintolan_lounaat(id)

    tanaan,huomenna,maanantai,tiistai,keskiviikko,torstai,perjantai=lounaat.hae_paivat()

    return render_template("ravintola.html", id=id, 
    ravintola=ravintola, 
    lounaat_tanaan=lounaat_tanaan,
    lounaat_huomenna=lounaat_huomenna,
    lounaat_maanantai=lounaat_maanantai,
    lounaat_tiistai=lounaat_tiistai,
    lounaat_keskiviikko=lounaat_keskiviikko,
    lounaat_torstai=lounaat_torstai,
    lounaat_perjantai=lounaat_perjantai, 
    tanaan=tanaan, 
    huomenna=huomenna,
    maanantai=maanantai,
    tiistai=tiistai,
    keskiviikko=keskiviikko,
    torstai=torstai,
    perjantai=perjantai)

@app.route("/kirjautuminen")
def kirjautuminen():
    return render_template("login.html")  

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    viesti = users.onko_oikein(username,password)
        
    if viesti == "Kirjautuminen onnistui":            
        session["username"] = username
        return redirect("/kirjautuminen")
    else:
        return render_template("error.html", viesti=viesti)   

@app.route("/newuser",methods=["POST"])
def uusi_kayttaja():
    username = request.form["username"]
    password = request.form["password"]
    users.luo_kayttaja(username,password)
    return redirect("/kirjautuminen")

@app.route("/logout")
def logout():
    del session["username"] 
    return redirect("/kirjautuminen")   