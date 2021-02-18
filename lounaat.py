from db import db
from datetime import date, datetime, timedelta

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

def hae_paivat():
    tanaan = date.today()
    huomenna = tanaan + timedelta(days=1)
    maanantai = tanaan + timedelta(days=-tanaan.weekday())
    tiistai = maanantai + timedelta(days=1)
    keskiviikko = maanantai + timedelta(days=2)
    torstai = maanantai + timedelta(days=3)
    perjantai = maanantai + timedelta(days=4)

    return tanaan,huomenna,maanantai,tiistai,keskiviikko,torstai,perjantai    

def hae_ravintolan_lounaat(id):
    sql = "SELECT * FROM lounaat WHERE ravintola_id=:id"
    result = db.session.execute(sql, {"id":id})
    lounaat = result.fetchall()

    tanaan, huomenna, maanantai, tiistai, keskiviikko, torstai, perjantai = hae_paivat()
   
    lounaat_tanaan = []
    lounaat_huomenna = []
    lounaat_maanantai = []
    lounaat_tiistai = []
    lounaat_keskiviikko = []
    lounaat_torstai = []
    lounaat_perjantai = []

    for lounas in lounaat:

        if lounas[2]==tanaan:
            lounaat_tanaan.append(lounas)
        if lounas[2]==huomenna:
            lounaat_huomenna.append(lounas)
        if lounas[2]==maanantai:
            lounaat_maanantai.append(lounas)
        if lounas[2]==tiistai:
            lounaat_tiistai.append(lounas)
        if lounas[2]==keskiviikko:
            lounaat_keskiviikko.append(lounas)
        if lounas[2]==torstai:
            lounaat_torstai.append(lounas)
        if lounas[2]==perjantai:
            lounaat_perjantai.append(lounas)

    print(torstai)
    print(lounaat_torstai)

    return lounaat_tanaan,lounaat_huomenna,lounaat_maanantai,lounaat_tiistai,lounaat_keskiviikko,lounaat_torstai,lounaat_perjantai