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
        # TODO: invalid username
        pass
    else:
        hash_value = user[0]
        if check_password_hash(hash_value, password):
            # TODO: correct username & password
            pass
        else:
            # TODO: invalid password     
            pass

def hae_ravintola(id):
    sql = "SELECT * FROM ravintolat WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    ravintola = result.fetchall()
    return ravintola