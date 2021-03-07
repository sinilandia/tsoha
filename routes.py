from app import app
import lunches
import users
from flask import redirect, render_template, request, session, flash, url_for
from datetime import date, datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
import os
from os import urandom

@app.route("/")
def index():
    restaurants_avgs = lunches.restaurants_avgs()
    session["restaurants"] = lunches.fetch_restaurant_names()
    lunches_today = lunches.fetch_lunches_today()
    return render_template("index.html",restaurants_avgs=restaurants_avgs, lunches=lunches_today)

@app.route("/restaurant/<int:id>")
def restaurant(id):
    restaurant = lunches.fetch_restaurant(id)

    lunches_today,lunches_tomorrow,lunches_monday,lunches_tuesday,lunches_wednesday,lunches_thursday,lunches_friday = lunches.fetch_restaurant_lunches(id)

    today,tomorrow,monday,tuesday,wednesday,thursday,friday=lunches.fetch_dates()

    reviews = lunches.fetch_reviews(id)
    average = lunches.restaurant_average(id)

    return render_template("restaurant.html", id=id, 
    restaurant=restaurant, 
    lunches_today=lunches_today,
    lunches_tomorrow=lunches_tomorrow,
    lunches_monday=lunches_monday,
    lunches_tuesday=lunches_tuesday,
    lunches_wednesday=lunches_wednesday,
    lunches_thursday=lunches_thursday,
    lunches_friday=lunches_friday, 
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
    try:
        if "username" in session:
            username = session["username"]
            favorites = users.get_favorites(username)
    except:
        pass        
    return render_template("login.html", favorites=favorites)  

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    message = users.check(username,password)  
    if message == "Kirjautuminen onnistui":            
        session["username"] = username
        session["restaurant_id"] = users.restaurateur_id(session["username"])
        print("RESTAURATEUR ID")
        print(session["restaurant_id"])
        session["csrf_token"] = os.urandom(16).hex()
        flash(message,'success')
    else:
        flash(message, 'danger')
    return redirect("/user")

@app.route("/newuser",methods=["POST"])
def new_user():
    username = request.form["username"]
    password = request.form["password"]
    if (users.create_user(username,password)):
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
        del session["restaurant_id"]
        del session["csrf_token"] 
        return redirect("/")   
    except:
        flash('Et ole kirjautunut sisään etkä täten voi kirjautua ulos.', 'danger')
        return redirect("/user")

@app.route("/lunch")
def lunch():
    id = session["restaurant_id"]
    try:
        lunches_today,lunches_tomorrow,lunches_monday,lunches_tuesday,lunches_wednesday,lunches_thursday,lunches_friday = lunches.fetch_restaurant_lunches(id)
        today,tomorrow,monday,tuesday,wednesday,thursday,friday=lunches.fetch_dates()
        return render_template("addlunch.html", 
        lunches_today=lunches_today,
        lunches_tomorrow=lunches_tomorrow,
        lunches_monday=lunches_monday,
        lunches_tuesday=lunches_tuesday,
        lunches_wednesday=lunches_wednesday,
        lunches_thursday=lunches_thursday,
        lunches_friday=lunches_friday, 
        today=today, 
        tomorrow=tomorrow,
        monday=monday,
        tuesday=tuesday,
        wednesday=wednesday,
        thursday=thursday,
        friday=friday)
    except:    
        flash("Jotain meni vikaan ravintolasi lounaiden lataamisessa.", 'danger')
    

@app.route("/addlunch",methods=["POST"])
def add_lunch():
    restaurant_id = session["restaurant_id"]
    name = request.form["lunch"]
    ondate = request.form["ondate"]
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    if len(name) < 1 or len(name)>150:
        flash("Lounaan nimi ei voi olla tyhjä eikä yli 150 merkkiä", 'danger')
    elif ondate=='':
        flash("Lounaalta puuttuu päivämäärä", 'danger') 
    elif restaurant_id==0:
        flash("Sinulla ei ole oikeuksia lisätä lounaita.", 'danger') 
    elif restaurant_id!=0:  
        lunches.add_lunch(name, ondate, restaurant_id)
        flash("Lounaan lisäys onnistui", 'success')
    else:
        flash("Lounaan lisäys ei onnistunut.", 'danger') 

    return redirect("/lunch")

@app.route("/deletelunch",methods=["POST"])
def delete_lunch():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    lunch_id = request.form["lunch_id"]

    if (lunches.delete_lunch(lunch_id)):
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

    try:
        if(users.add_favorite(username,id)):
            message = restaurant_name + " lisätty suosikkeihin!"
            flash(message, 'success')
    except: 
        flash("Ravintola on jo suosikeissa.",'success')  

    return redirect(request.referrer)

@app.route("/deletefavorite",methods=["POST"])
def delete_favorite():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    name = request.form["restaurant_name"]
    id = lunches.fetch_restaurant_id(name)

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

@app.route("/search")
def search():
    query = request.args["query"]
    results = lunches.search(query)
    today,tomorrow,monday,tuesday,wednesday,thursday,friday=lunches.fetch_dates()
    return render_template("result.html", results=results,
    today=today, 
    tomorrow=tomorrow,
    monday=monday,
    tuesday=tuesday,
    wednesday=wednesday,
    thursday=thursday,
    friday=friday)