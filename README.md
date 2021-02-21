# tsoha-lounaslarussa
tsoha k2021

# Heroku-sovelluksen testaus
https://tsoha-lounaslarussa.herokuapp.com/

Tällä hetkellä toimii etusivu, Puhuri, Borneo, Makers ja Casa Mare. Etusivu näyttää lounaat tänään. Ravintolan oma sivu näyttää tämän viikon lounaat. 

Käyttäjät voivat luoda tilin ja kirjautua. Käyttäjät voivat yrittää lisätä lounaita siinä kuitenkaan onnistumatta.

Jos haluaa ravintoloitsija-tilin, ylläpitäjän pitää käydä tämä erikseen muuttamassa tietokantataulussa. Tätä voi testata tunnuksilla Puhuri, salasana ravintola. Ravintoloitsija voi lisätä lounaita.

## Aihe: Lounas Larussa
Näe kätevästi kaikki Lauttasaaren lounaspaikat yhdestä paikkaa!
Voit myös peukuttamalla ilmoittaa, minne olet menossa tänään. Näin voidaan välttyä ruuhkilta ja pystymme helpommin pitämään turvaväleistä huolta.

Lounailijana voit luoda itsellesi tunnukset sivustolle ja arvioida lounaskokemuksesi.

Ravintoloitsijana voit luoda omat tunnukset ja päivittää ravintolasi lounaat. 

### Keskeiset toiminnot

**Etusivulta** löydät kartan kaikista Lauttasaaren lounaspaikoista.
Kartan alla näkyvät ravintolat ja niiden lounaat listana allekkain. 

**Ravintolakohtaiselta** sivulta löydät ravintolan tiedot ja näet koko viikon lounaslistan. Täältä löytyy myös ravintola kartalta. Täältä näet ravintolan lounaiden suosion tähtinä/peukkuina.

Jatkossa tänne voi myös kirjoittaa oman arvion ravintolan lounaskokemuksesta.

**SQL-taulut**
- ravintolat
- lounaat
- kayttajat

Pitää vielä lisätä
- Arvostelut ravintoloille
- peukut/tähdet annoksille, onnistuu kirjautumatta
- käyttäjän oma sivu, jolla näkyy omat arvostelut
- navigaation haku ravintolat-taulun mukaan
