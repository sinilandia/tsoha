from db import db
from datetime import date, datetime, timedelta

def fetch_restaurants():
    result = db.session.execute("SELECT * FROM restaurants ORDER BY name ASC")
    restaurants = result.fetchall()
    return restaurants

def fetch_restaurant_names():
    result = db.session.execute("SELECT id, name FROM restaurants ORDER BY name ASC")
    restaurant_names = result.fetchall()
    names = {}
    for restaurant in restaurant_names:
        names[restaurant[1]] = restaurant[0]
    return names

def fetch_restaurant_id(name):
    sql = "SELECT id FROM restaurants WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    id = result.fetchone()
    return id[0]

def fetch_lunches_today():
    result = db.session.execute("SELECT * FROM lunches WHERE ondate = CURRENT_DATE")
    lunches_today = result.fetchall()
    return lunches_today

def fetch_restaurant(id):
    sql = "SELECT * FROM restaurants WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    restaurant = result.fetchall()
    return restaurant

def fetch_dates():
    today = date.today()
    tomorrow = today + timedelta(days=1)
    monday = today + timedelta(days=-today.weekday())
    tuesday = monday + timedelta(days=1)
    wednesday = monday + timedelta(days=2)
    thursday = monday + timedelta(days=3)
    friday = monday + timedelta(days=4)

    return today,tomorrow,monday,tuesday,wednesday,thursday,friday    

def fetch_restaurant_lunches(id):
    sql = "SELECT * FROM lunches WHERE restaurant_id=:id"
    result = db.session.execute(sql, {"id":id})
    lunches = result.fetchall()

    today, tomorrows, monday, tuesday, wednesday, thursday, friday = fetch_dates()
   
    lunches_today = []
    lunches_tomorrows = []
    lunches_monday = []
    lunches_tuesday = []
    lunches_wednesday = []
    lunches_thursday = []
    lunches_friday = []

    for lunch in lunches:

        if lunch[2]==today:
            lunches_today.append(lunch)
        if lunch[2]==tomorrows:
            lunches_tomorrows.append(lunch)
        if lunch[2]==monday:
            lunches_monday.append(lunch)
        if lunch[2]==tuesday:
            lunches_tuesday.append(lunch)
        if lunch[2]==wednesday:
            lunches_wednesday.append(lunch)
        if lunch[2]==thursday:
            lunches_thursday.append(lunch)
        if lunch[2]==friday:
            print("PERJANTAIN LOUNAAT")
            print(lunch[1])
            lunches_friday.append(lunch)

    return lunches_today,lunches_tomorrows,lunches_monday,lunches_tuesday,lunches_wednesday,lunches_thursday,lunches_friday


def add_lunch(name, ondate, restaurant_id):
    sql = "INSERT INTO lunches (name, ondate, restaurant_id) VALUES (:name, :ondate, :restaurant_id)"
    result = db.session.execute(sql, {"name":name, "ondate":ondate, "restaurant_id":restaurant_id})
    db.session.commit()
    return True

def delete_lunch(id):
    sql = "DELETE FROM lunches WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    db.session.commit()
    return True

def fetch_reviews(restaurant_id):
    sql = "SELECT users.name, R.star, R.title, R.review, R.today FROM reviews R INNER JOIN users ON users.id=R.user_id WHERE R.restaurant_id=:restaurant_id"
    result = db.session.execute(sql,{"restaurant_id":restaurant_id})
    reviews = result.fetchall()
    return reviews    

def restaurant_average(restaurant_id):
    sql = "SELECT AVG(star)::numeric(10,2) FROM reviews WHERE restaurant_id=:restaurant_id"
    result = db.session.execute(sql, {"restaurant_id":restaurant_id})
    average = result.fetchone()
    return average

def restaurants_avgs():
    sql = ("SELECT \
	R.id, \
	R.name, \
	R.address, \
	R.phone, \
	R.email, \
	R.price, \
	COALESCE(AVG(A.star)::numeric(10,2),0) AS avg \
    FROM reviews A \
    RIGHT JOIN restaurants R \
    ON R.id=A.restaurant_id \
    GROUP BY R.id \
    ORDER BY R.name ASC")
    result = db.session.execute(sql)
    averages = result.fetchall()
    return averages


def search(query):
    sql = "SELECT L.name, L.ondate, R.name FROM lunches L INNER JOIN restaurants R ON L.restaurant_id = R.id AND L.name ILIKE :query ORDER BY L.ondate DESC"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    lunches = result.fetchall()
    return lunches

# TÄMÄ OSIO ETUSIVULLE KARUSELLIKSI?
# def fetch_reviews(restaurant_id):
#     sql = "SELECT R.user_id, ravintolat.nimi, R.star, R.title, R.review, R.today FROM reviews R INNER JOIN ravintolat ON ravintolat.id=R.restaurant_id WHERE R.restaurant_id=:restaurant_id"
#     result = db.session.execute(sql,{"restaurant_id":restaurant_id})
#     reviews = result.fetchall()
#     return reviews



        