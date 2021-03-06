# tsoha-lounaslarussa
tsoha k2021

# Heroku-sovelluksen testaus
https://tsoha-lounaslarussa.herokuapp.com/

Luo itsellesi tunnukset, joilla pääset testaamaan sovellusta.

Ravintoloitsijoiden tunnukset ovat muotoa Ravintolannimi, salasana ravintola, esim. Puhuri, ravintola.

## Aihe: Lounas Larussa
Näe kätevästi kaikki Lauttasaaren lounaspaikat yhdestä paikkaa!

Ruokailijana voit luoda itsellesi tunnukset sivustolle, lisätä ravintolan lemppareihin ja arvioida lounaskokemuksesi.

Ravintoloitsijana voit päivittää ja poistaa ravintolasi lounaat. 

### Keskeiset toiminnot

**Etusivulta** löydät top-listan ja lounaspaikat aakkosjärjestyksessä. Tähtiarvio on keskiarvo ravintolalle jätetyistä arvioista. Jos arvioita ei ole, tähdet näyttävät 0. Sivulla näkyy vain tämän päivän lounaat (eli jos testaat sovellusta viikonloppuna, lounaita ei välttämättä ole). Myös navigaatiopalkki on aakkosjärjestyksessä. 

**Ravintolakohtaiselta** sivulta löydät ravintolan tiedot ja näet koko viikon lounaslistan. Tämän lisäksi voit kirjautuneena käyttäjänä lisätä arvion ravintolasta ja merkata ravintolan lemppariksi. Käyttäjä ei voi poistaa arviotaan myöhemmin, kuten AirBnB:ssä. Tarkoituksena on lisätä arvioiden luotettavuutta. Arviointilomake näkyy tarkoituksella myös kirjautumattomille käyttäjille, koska haluan kannustaa käyttäjiä luomaan tunnukset palveluun. 

**Kirjautumissivulla** näkyy kirjautumattomalle käyttäjälle lomake luoda tunnukset tai kirjautua sisään.
Kirjautuneena käyttäjä näkee omat lemppariravintolansa, voi poistaa lempparin ja kirjautua ulos. 
Kirjautuneena ravintoloitsija näkee näiden lisäksi linkin Lounashallinnan sivulle, josta pääsee lisäämään lounaita ja tarvittaessa poistamaan lounaan tältä viikolta, jos sattuu typo. Täällä näkyy vain lounaat ma-pe eli jos testaat viikonloppuna la-su, et näe la-su lounaita. Tämä on realistinen ratkaisu, koska lounaita harvemmin on la-su. 

**Haku** hakee lounaiden nimistä, ei väliä onko iso vai pieni kirjain. Haku näyttää viimeisimmät lounaat ensin, sillä tämä on todennäköisesti tärkeä kriteeri hakijalle.

**SQL-taulut**
- restaurants
- lunches
- users
- favorites 
- reviews
