from app import app
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def create_user(username, password):
    hash_value = generate_password_hash(password)
    sql = "SELECT name FROM users WHERE name=:username"
    result = db.session.execute(sql, {"username":username})
    if result.fetchone() == None: 
        sql = "INSERT INTO users (name, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        return True

def check(username, password):
    sql = "SELECT password FROM users WHERE name=:username"
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

def restaurateur_id(username):
    sql = "SELECT restaurant_id FROM users WHERE name=:username"
    result = db.session.execute(sql, {"username":username})
    restaurant_id = result.fetchone()

    if restaurant_id[0] == None:
        return 0
    else:
        return restaurant_id[0]

def get_user_id(username):
    sql = "SELECT id FROM users WHERE name=:username"
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
    sql = "SELECT R.name FROM restaurants R, favorites F WHERE F.user_id=:user_id AND F.restaurant_id=R.id"
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