from db import db

#define tietokantakomennot

def hae_ravintolat():
    result = db.session.execute("SELECT * FROM ravintolat")
    ravintolat = result.fetchall()
    return ravintolat

def hae_lounaat_tanaan():
    result = db.session.execute("SELECT * from lounaat WHERE pvm = CURRENT_DATE")
    lounaat_tanaan = result.fetchall()
    return lounaat_tanaan

def hae_ravintola(id):
    sql = "SELECT * FROM ravintolat WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    ravintola = result.fetchall()
    return ravintola

def hae_ravintolan_lounaat(id):
    sql = "SELECT * FROM lounaat WHERE ravintola_id=:id"
    result = db.session.execute(sql, {"id":id})
    lounaat = result.fetchall()
    return lounaat
