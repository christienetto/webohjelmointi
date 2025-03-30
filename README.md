# Homework Tracker
## Nyky Tilanne
Kirjautuneet käyttäjät voivat etsiä kotitehtäviään, ja tyhjä hakukenttä listaa kaikki kotitehtävät. Uloskirjautumisominaisuus on käytössä. Rekisteröityneet ja kirjautuneet käyttäjät näkevät vain omat lisäämänsä kotitehtävät, joita he voivat muokata ja poistaa. Rekisteröityminen toimii, kirjautuminen toimii, lisääminen ja poistaminen toimivat.
## Sovelluksen toiminnot
- Käyttäjä pystyy lisäämään uuden kotitehtävän.
- Käyttäjä näkee kaikki lisätyt kotitehtävät järjestettynä eräpäivän mukaan.
- Käyttäjä pystyy poistamaan kotitehtäviä listalta.
- Käyttäjä pystyy etsimään ilmoituksia hakusanalla.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät kotitehtävät.
- Käyttäjä pystyy valitsemaan ilmoitukselle yhden tai useamman luokittelun (esim. Aloitustila, Puolivälissä, Valmis (Poista ilmoituksen)).
## Sovelluksen asennus

1. Asenna Flask ja riippuvuudet:

   ```sh
   pip install flask flask-sqlalchemy flask-wtf
