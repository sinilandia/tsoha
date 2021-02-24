CREATE TABLE ravintolat (id SERIAL PRIMARY KEY, nimi TEXT, osoite TEXT, puh TEXT, email TEXT, lounashinta TEXT);
CREATE TABLE lounaat (id SERIAL PRIMARY KEY, nimi TEXT, pvm DATE, peukut INTEGER, ravintola_id INTEGER REFERENCES ravintolat(id) NOT NULL);
CREATE TABLE kayttajat (id SERIAL PRIMARY KEY, tunnus TEXT, salasana TEXT, ravintola_id INTEGER REFERENCES ravintolat(id));
