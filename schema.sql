CREATE TABLE restaurants (id SERIAL PRIMARY KEY, name TEXT, address TEXT, phone TEXT, email TEXT, price TEXT);
CREATE TABLE lunches (id SERIAL PRIMARY KEY, name TEXT, ondate DATE, restaurant_id INTEGER REFERENCES restaurants(id) NOT NULL);
CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT, password TEXT, restaurant_id INTEGER REFERENCES restaurants(id));
CREATE TABLE favorites (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users(id), restaurant_id INTEGER REFERENCES restaurants(id));
CREATE TABLE reviews (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users(id), restaurant_id INTEGER REFERENCES restaurants(id), star INTEGER, title TEXT, review TEXT, today DATE DEFAULT CURRENT_DATE);

INSERT INTO restaurants(name, address,phone,email,price) VALUES ('Casa Mare', 'Gyldenintie 6, 00200 Helsinki','020 7424260', 'casamare@ravintolakolmio.fi', '10,90€');
INSERT INTO restaurants(name, address,phone,email,price) VALUES ('Makers', 'Heikkiläntie 10, 00210 Helsinki','040-3608808','makers@makerskahvila.com', '9,90€');
INSERT INTO restaurants(name, address,phone,email,price) VALUES ('Borneo', 'Itälahdenkatu 20, 00210 Helsinki', '045 600 6354', 'ravintolaborneo@gmail.com','12,90€');
INSERT INTO restaurants(name, address,phone,email,price) VALUES ('Puhuri', 'Kauppaneuvoksentie 18, 00200 Helsinki', '50 5164365','puhuri@tartine.fi', '13€');