from app import app
import lounaat
import users
from flask import redirect, render_template, request, session, flash
from datetime import date, datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
import os
from os import urandom



@app.route("/")
def index():
    ravintolat = lounaat.hae_ravintolat()
    session["restaurants"] = lounaat.fetch_restaurant_names()
    print("INDEX")
    print(session["restaurants"])
    lounaat_tanaan= lounaat.hae_lounaat_tanaan()
    return render_template("index.html",ravintolat=ravintolat, lounaat=lounaat_tanaan)

@app.route("/ravintola/<int:id>")
def ravintolan_sivu(id):
    print("RAVINTOLAN_SIVU:")
    print(session["restaurants"])
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
        session["ravintola_id"] = users.kayttajan_ravintola_id(session["username"])
        session["csrf_token"] = os.urandom(16).hex()
        return redirect("/kirjautuminen")
    else:
        return render_template("error.html", viesti=viesti)   

@app.route("/newuser",methods=["POST"])
def uusi_kayttaja():
    username = request.form["username"]
    password = request.form["password"]
    if (users.luo_kayttaja(username,password)):
        message = "Tili luotu käyttäjälle " + username
        flash(message, 'success')
    else: 
        flash("Tiliä ei voitu luoda. Käyttäjätunnus on jo käytössä.", 'danger')  
    return redirect("/kirjautuminen")

@app.route("/logout")
def logout():
    flash('Kirjauduit ulos.', 'success')
    del session["username"]
    del session["ravintola_id"]
    del session["csrf_token"] 
    return redirect("/")   

@app.route("/lunch")
def lunch():
    return render_template("addlunch.html")

@app.route("/addlunch",methods=["POST"])
def add_lunch():
    ravintola_id = session["ravintola_id"]
    nimi = request.form["lounas"]
    pvm = request.form["paivamaara"]
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    if len(nimi) < 1 or len(nimi)>150:
        return render_template("error.html", viesti="Lounaan nimi ei voi olla tyhjä eikä yli 150 merkkiä")
    if pvm=='':
        return render_template("error.html", viesti="Lounaalta puuttuu päivämäärä")
    if ravintola_id!=0: 
        lounaat.lisaa_lounas(nimi, pvm, ravintola_id)
        return redirect("/lunch")
    if ravintola_id==0:
        return render_template("error.html", viesti="Sinulla ei ole oikeuksia lisätä lounaita.")
    else:
        return render_template("error.html", viesti="Lounaan lisäys ei onnistunut")