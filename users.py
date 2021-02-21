from app import app
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def luo_kayttaja(username, password):
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO kayttajat (tunnus, salasana) VALUES (:username, :password)"
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()

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
    sql = "SELECT ravintoloitsija FROM kayttajat WHERE tunnus=:username"
    result = db.session.execute(sql, {"username":username})
    ravintola_id = result.fetchone()

    if ravintola_id == None:
        return 0
    else:
        return ravintola_id[0]
    
