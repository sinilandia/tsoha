from app import app
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def luo_kayttaja(username, password):
    hash_value = generate_password_hash(password)
    sql = "SELECT tunnus FROM kayttajat WHERE tunnus=:username"
    result = db.session.execute(sql, {"username":username})
    if result.fetchone() == None: 
        sql = "INSERT INTO kayttajat (tunnus, salasana) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        return True

def onko_oikein(username, password):
    sql = "SELECT salasana FROM kayttajat WHERE tunnus=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return "Käyttäjää ei ole olemassa"
    else:
        hash_value = user[0]
        if check_password_hash(hash_value, password):
            return "Kirjautuminen onnistui"
        else:
            return "Väärä salasana"

def kayttajan_ravintola_id(username):
    sql = "SELECT ravintola_id FROM kayttajat WHERE tunnus=:username"
    result = db.session.execute(sql, {"username":username})
    ravintola_id = result.fetchone()

    if ravintola_id[0] == None:
        return 0
    else:
        return ravintola_id[0]

def get_user_id(username):
    sql = "SELECT id FROM kayttajat WHERE tunnus=:username"
    result = db.session.execute(sql, {"username":username})
    user_id = result.fetchone()
    return user_id[0]        

def add_favorite(username, restaurant_id):
    user_id = get_user_id(username)

    #check if restaurant is already in favorites
    sql = "SELECT DISTINCT restaurant_id FROM favorites WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    restaurants = result.fetchall()
    for restaurant in restaurants:
        if (str(restaurant[0])==restaurant_id):
            return False

    #add restaurant into favorites
    sql = "INSERT INTO favorites (user_id, restaurant_id) VALUES (:user_id, :restaurant_id)"
    db.session.execute(sql, {"user_id":user_id, "restaurant_id":restaurant_id})
    db.session.commit()
    return True

def get_favorites(username):
    user_id = get_user_id(username)
    sql = "SELECT R.nimi FROM ravintolat R, favorites F WHERE F.user_id=:user_id AND F.restaurant_id=R.id"
    result = db.session.execute(sql, {"user_id":user_id})
    favorites = result.fetchall()
    return favorites
    
def delete_favorite(username, restaurant_id):
    user_id = get_user_id(username)
    sql = "DELETE FROM favorites WHERE user_id=:user_id AND restaurant_id=:restaurant_id"
    result = db.session.execute(sql, {"user_id":user_id, "restaurant_id":restaurant_id})
    db.session.commit()
    return True

def add_review(username,restaurant_id, star, title, review):
    user_id = get_user_id(username)
    sql = "INSERT INTO reviews (user_id, restaurant_id, star, title, review) VALUES (:user_id, :restaurant_id, :star, :title, :review)"
    db.session.execute(sql, {"user_id":user_id, "restaurant_id":restaurant_id, "star":star, "title":title, "review":review})
    db.session.commit()
    return True