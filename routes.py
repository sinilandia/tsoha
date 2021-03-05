from app import app
import lounaat
import users
from flask import redirect, render_template, request, session, flash, url_for
from datetime import date, datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
import os
from os import urandom

@app.route("/")
def index():
    restaurants = lounaat.hae_ravintolat()
    session["restaurants"] = lounaat.fetch_restaurant_names()
    lunches_today = lounaat.hae_lounaat_tanaan()
    return render_template("index.html",restaurants=restaurants, lunches=lunches_today)

@app.route("/restaurant/<int:id>")
def restaurant(id):
    restaurant = lounaat.hae_ravintola(id)

    lounaat_tanaan,lounaat_huomenna,lounaat_maanantai,lounaat_tiistai,lounaat_keskiviikko,lounaat_torstai,lounaat_perjantai = lounaat.hae_ravintolan_lounaat(id)

    today,tomorrow,monday,tuesday,wednesday,thursday,friday=lounaat.hae_paivat()

    reviews = lounaat.fetch_reviews(id)
    average = lounaat.restaurant_average(id)

    return render_template("restaurant.html", id=id, 
    restaurant=restaurant, 
    lounaat_tanaan=lounaat_tanaan,
    lounaat_huomenna=lounaat_huomenna,
    lounaat_maanantai=lounaat_maanantai,
    lounaat_tiistai=lounaat_tiistai,
    lounaat_keskiviikko=lounaat_keskiviikko,
    lounaat_torstai=lounaat_torstai,
    lounaat_perjantai=lounaat_perjantai, 
    today=today, 
    tomorrow=tomorrow,
    monday=monday,
    tuesday=tuesday,
    wednesday=wednesday,
    thursday=thursday,
    friday=friday,
    reviews=reviews,
    average=average)

@app.route("/user")
def user():
    favorites = []
    if "username" in session:
        username = session["username"]
        favorites = users.get_favorites(username)
    return render_template("login.html", favorites=favorites)  

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    message = users.onko_oikein(username,password)  
    if message == "Kirjautuminen onnistui":            
        session["username"] = username
        session["ravintola_id"] = users.kayttajan_ravintola_id(session["username"])
        session["csrf_token"] = os.urandom(16).hex()
        flash(message,'success')
    else:
        flash(message, 'danger')
    return redirect("/user")

@app.route("/newuser",methods=["POST"])
def new_user():
    username = request.form["username"]
    password = request.form["password"]
    if (users.luo_kayttaja(username,password)):
        message = "Tili luotu käyttäjälle " + username
        flash(message, 'success')
    else: 
        flash("Tiliä ei voitu luoda. Käyttäjätunnus on jo käytössä.", 'danger')  
    return redirect("/user")

@app.route("/logout")
def logout():
    try: 
        flash('Kirjauduit ulos.', 'success')
        del session["username"]
        del session["ravintola_id"]
        del session["csrf_token"] 
        return redirect("/")   
    except:
        flash('Et ole kirjautunut sisään etkä täten voi kirjautua ulos.', 'danger')
        return redirect("/user")

@app.route("/lunch")
def lunch():
    id = session["ravintola_id"]
    try:
        lounaat_tanaan,lounaat_huomenna,lounaat_maanantai,lounaat_tiistai,lounaat_keskiviikko,lounaat_torstai,lounaat_perjantai = lounaat.hae_ravintolan_lounaat(id)
        today,tomorrow,monday,tuesday,wednesday,thursday,friday=lounaat.hae_paivat()
        return render_template("addlunch.html", 
        lounaat_tanaan=lounaat_tanaan,
        lounaat_huomenna=lounaat_huomenna,
        lounaat_maanantai=lounaat_maanantai,
        lounaat_tiistai=lounaat_tiistai,
        lounaat_keskiviikko=lounaat_keskiviikko,
        lounaat_torstai=lounaat_torstai,
        lounaat_perjantai=lounaat_perjantai, 
        today=today, 
        tomorrow=tomorrow,
        monday=monday,
        tuesday=tuesday,
        wednesday=wednesday,
        thursday=thursday,
        friday=friday,)
    except:    
        pass
    

@app.route("/addlunch",methods=["POST"])
def add_lunch():
    restaurant_id = session["ravintola_id"]
    name = request.form["lounas"]
    day = request.form["paivamaara"]
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    if len(name) < 1 or len(name)>150:
        flash("Lounaan nimi ei voi olla tyhjä eikä yli 150 merkkiä", 'danger')
    elif day=='':
        flash("Lounaalta puuttuu päivämäärä", 'danger') 
    elif restaurant_id==0:
        flash("Sinulla ei ole oikeuksia lisätä lounaita.", 'danger') 
    elif restaurant_id!=0:  
        lounaat.lisaa_lounas(name, day, restaurant_id)
        flash("Lounaan lisäys onnistui", 'success')
    else:
        flash("Lounaan lisäys ei onnistunut.", 'danger') 

    return redirect("/lunch")

@app.route("/deletelunch",methods=["POST"])
def delete_lunch():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    lunch_id = request.form["lunch_id"]

    if (lounaat.delete_lunch(lunch_id)):
        flash("Lounas poistettu.", 'success')
    else:
        flash("Poistaminen ei onnistunut.", 'danger')

    return redirect(request.referrer)

@app.route("/addfavorite",methods=["POST"])
def add_favorite():
    username = session["username"]
    id = request.form["restaurant_id"]
    restaurant_name = request.form["restaurant_name"]

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    if (users.add_favorite(username,id)):
        message = restaurant_name + " lisätty suosikkeihin!"
        flash(message, 'success')
    else: 
        flash("Ravintola on jo suosikeissa.",'success')  

    return redirect(request.referrer)

@app.route("/deletefavorite",methods=["POST"])
def delete_favorite():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    name = request.form["restaurant_name"]
    id = lounaat.fetch_restaurant_id(name)

    if (users.delete_favorite(session["username"],id)):
        flash(name + " poistettu lemppareista", 'success')
    else:
        flash("Poistaminen ei onnistunut.", 'danger')

    return redirect(request.referrer)

@app.route("/addreview",methods=["POST"])
def add_review():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    username = session["username"]
    restaurant_id = request.form["restaurant_id"]
    star = request.form["star"]
    title = request.form["title"]
    review = request.form["review"]

    if (users.add_review(username,restaurant_id, star, title, review)):
        flash("Arviosi on lisätty!", 'success')
    else: 
        flash("Arvion lisääminen ei onnistunut.",'danger')  

    return redirect(request.referrer)