import mysql.connector

# Komento, jolla luodaan tietokanta Dockeriin:
# docker run --name RPS-MYSQL -e MYSQL_ROOT_PASSWORD=RPS-ROOT -e MYSQL_DATABASE=RPS -e MYSQL_USER=RPS-USER -e MYSQL_PASSWORD=RPS-PASS -p 3307:3306 -d mysql:latest
# Komento, jolla luodaan taulu Dockerissa pyörivään tietokantaan.
# CREATE TABLE TOP10 (
#     ID INT NOT NULL AUTO_INCREMENT,
#     NIMI CHAR(10),
#     PISTEET INT NOT NULL,
#     PRIMARY KEY (ID)
# );
# Ota yhteys tietokantaan komentoriviltä:
# mysql -h 127.0.0.1 -P 3307 -u RPS-USER -p
# MYSQL_ROOT_PASSWORD=RPS-ROOT


# Funktio tietokantayhteyden luomiseen ja kursorin palauttamiseen.
def yhteys_tietokantaan():
    # Tietokannan palvelimen osoite.
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        # Portti.
        port=3307,
        # Käytettävä tietokanta.
        database="RPS",
        # Käyttäjätunnus tietokantaan.
        user="RPS-USER",
        # Käyttäjän salasana.
        password="RPS-PASS",
    )
    # Kursorin luominen tietokantakyselyjä varten.
    mycursor = mydb.cursor()
    # Palautetaan yhteys ja kursori.
    return mydb, mycursor


# Funktio, joka lisää pelaajan tiedot tietokantaan.
def lisää_tietokantaan(nimimerkki, pelaaja_voitot):
    # Avataan tietokantayhteys.
    mydb, mycursor = yhteys_tietokantaan()
    sql = "INSERT INTO TOP10 (NIMI, PISTEET) VALUES (%s, %s)"
    # Valmistellaan SQL-lause ja arvot.
    val = (nimimerkki, pelaaja_voitot)
    # Suoritetaan tietojen lisääminen.
    mycursor.execute(sql, val)
    # Vahvistetaan muutokset tietokannassa.
    mydb.commit()
    # Tulostetaan lisättyjen rivien määrä.
    print(mycursor.rowcount, "row added to database.")
    # Suljetaan yhteys ja kursori.
    sulje_yhteys(mydb, mycursor)


# Funktio, joka lukee top 10 -pelaajien tiedot tietokannasta.
def lue_tietokanta_top10():
    # Avataan tietokantayhteys.
    mydb, mycursor = yhteys_tietokantaan()
    sql = "SELECT NIMI, PISTEET FROM TOP10 ORDER BY PISTEET DESC LIMIT 10"
    # Suoritetaan SQL-lause.
    mycursor.execute(sql)
    # Haetaan tulokset.
    top_10 = mycursor.fetchall()
    # Suljetaan yhteys ja kursori.
    sulje_yhteys(mydb, mycursor)
    # Palautetaan top 10 pelaajaa.
    return top_10


# Funktio, joka tulostaa tietokannasta top 10 -pelaajat tulostauluna.
def lue_tietokanta_taulu():
    # Avataan tietokantayhteys.
    mydb, mycursor = yhteys_tietokantaan()
    sql = "SELECT NIMI, PISTEET FROM TOP10 ORDER BY PISTEET DESC LIMIT 10"
    # Suoritetaan SQL-lause.
    mycursor.execute(sql)
    # Haetaan tulokset.
    taulu = mycursor.fetchall()
    # Tulostetaan tulostaulu.
    print("--- SCOREBOARD ---")
    sijoitus = 1
    for row in taulu:  # Tulostetaan jokainen pelaaja ja hänen pisteensä.
        print(f"{sijoitus}) | {row[0]} | Wins: {row[1]}")
        sijoitus += 1
    # Suljetaan yhteys ja kursori.
    sulje_yhteys(mydb, mycursor)


# Funktio, joka poistaa tietokannasta pelaajat, joiden pisteet ovat alle kynnysarvon.
def poista_tietokannasta(kynnys):
    # Avataan tietokantayhteys.
    mydb, mycursor = yhteys_tietokantaan()
    sql = "DELETE FROM TOP10 WHERE PISTEET < %s"
    # Valmistellaan SQL-lause ja arvot.
    val = (kynnys,)
    # Suoritetaan poisto-operaatio.
    mycursor.execute(sql, val)
    # Vahvistetaan muutokset tietokannassa.
    mydb.commit()
    # Tulostetaan poistettujen rivien määrä.
    print(mycursor.rowcount, "row deleted from database.")
    # Suljetaan yhteys ja kursori.
    sulje_yhteys(mydb, mycursor)


# Funktio, joka sulkee tietokantayhteyden ja kursorin.
def sulje_yhteys(mydb, mycursor):
    # Suljetaan tietokantayhteys.
    mydb.close()
    # Suljetaan kursori.
    mycursor.close()
