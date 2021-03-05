CREATE TABLE ravintolat (id SERIAL PRIMARY KEY, nimi TEXT, osoite TEXT, puh TEXT, email TEXT, lounashinta TEXT);
CREATE TABLE lounaat (id SERIAL PRIMARY KEY, nimi TEXT, pvm DATE, peukut INTEGER, ravintola_id INTEGER REFERENCES ravintolat(id) NOT NULL);
CREATE TABLE kayttajat (id SERIAL PRIMARY KEY, tunnus TEXT, salasana TEXT, ravintola_id INTEGER REFERENCES ravintolat(id));
CREATE TABLE favorites (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES kayttajat(id), restaurant_id INTEGER REFERENCES ravintolat(id));
CREATE TABLE reviews (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES kayttajat(id), restaurant_id INTEGER REFERENCES ravintolat(id), star INTEGER, title TEXT, review TEXT, today DATE DEFAULT CURRENT_DATE);