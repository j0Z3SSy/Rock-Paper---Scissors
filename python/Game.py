# Game.py
import random
import Database


# Funktio tarkistaa, kuka voittaa yhden kierroksen pelaajan ja tietokoneen välillä.
def tarkista_voittaja(pelaaja, tietokone):
    # Jos pelaaja ja tietokone valitsevat saman liikkeen, kierros päättyy tasapeliin.
    if pelaaja == tietokone:
        return "tie"
    # Jos pelaaja voittaa tietokoneen klassisten sääntöjen mukaan, palautetaan "player".
    elif (
        (pelaaja == "Rock" and tietokone == "Scissors")
        or (pelaaja == "Scissors" and tietokone == "Paper")
        or (pelaaja == "Paper" and tietokone == "Rock")
    ):
        return "player"
    # Muutoin tietokone voittaa.
    else:
        return "computer"


# Funktio suorittaa yhden pelikierroksen ja palauttaa tuloksen.
def kierros():
    # Mahdolliset klassiset liikkeet.
    liikkeet = ["Rock", "Paper", "Scissors"]

    # Pelaajalta kysytään hänen liikkeensä ja tarkistetaan, että se on sallittu.
    while True:
        pelaaja_liike = input(
            "--- Choose your move (Rock, Paper, Scissors): ---"
        ).capitalize()
        # Jos pelaajan valinta on sallittu, jatketaan eteenpäin.
        if pelaaja_liike in liikkeet:
            break
        else:
            # Jos pelaajan valinta on virheellinen, näytetään ohje uudelleen.
            print("Ref: Please choose Rock, Paper, or Scissors.")

    # Tietokone tekee satunnaisen valinnan kolmesta liikkeestä.
    tietokone_liike = random.choice(liikkeet)
    # Näytetään pelaajan valinta.
    print(f"Player: {pelaaja_liike}!")
    # Näytetään tietokoneen valinta.
    print(f"Computer: {tietokone_liike}!")

    # Selvitetään kierroksen voittaja.
    tulos = tarkista_voittaja(pelaaja_liike, tietokone_liike)

    # Tulostetaan tuomarin päätös ja palautetaan pelin tulos.
    if tulos == "tie":
        print("Ref: It's a tie!\n")
        return 0
    elif tulos == "player":
        print("Ref: You won!\n")
        return 1
    else:
        print("Ref: Game over!\n")
        return -1


# Funktio kysyy pelaajalta, haluaako hän jatkaa pelaamista.
def jatketaanko():
    while True:
        # Kysytään, jatkaako pelaaja.
        pelaa_uudestaan = input("Ref: Continue playing? [Y/N]: ").upper()
        # Pelaaja haluaa jatkaa.
        if pelaa_uudestaan == "Y":
            print("Ref: Let's continue!\n")
            return True
        # Pelaaja ei halua jatkaa.
        elif pelaa_uudestaan == "N":
            print("Ref: You decided to give up...\n")
            return False
        # Jos vastaus ei ole Y tai N, kysytään uudelleen.
        else:
            print("Ref: Make up your mind! Do you want to play (Y) or not (N)!")


# Funktio tarkistaa, pääseekö pelaaja top 10 -listalle (tietokantaan) voittojensa perusteella.
def top10(pelaaja_voitot):
    # Haetaan nykyinen top 10 -lista tietokannasta.
    top_10 = Database.lue_tietokanta_top10()

    # Jos top 10 -listalla on alle 10 pelaajaa, pelaaja pääsee automaattisesti listalle.
    if len(top_10) < 10:
        while True:
            # Kysytään pelaajalta nimimerkkiä ennätyksen tallentamiseksi.
            nimimerkki = input(
                "Def: Congratulations! You set a new record! Enter your nickname, which will be engraved on the scoreboard! [A-Z,0-9] (Max 10 characters): "
            ).upper()
            # Nimimerkin tulee sisältää vain sallittuja merkkejä ja olla enintään 10 merkkiä pitkä.
            if nimimerkki.isalnum() and len(nimimerkki) <= 10:
                print("--- Your nickname was accepted! ---")
                # Tallennetaan nimimerkki ja voitot tietokantaan.
                Database.lisää_tietokantaan(nimimerkki, pelaaja_voitot)
                # Näytetään päivitetty top 10 -lista.
                Database.lue_tietokanta_taulu()
                # Palauttaa Stringin jos lisättiin tietokantaan.
                return "You are in top 10!"
            else:
                print("Invalid nickname, try again! [A-Z,0-9]")

    # Haetaan 10. sijalla olevan pelaajan pisteet.
    kynnys = top_10[-1][1]

    # Jos pelaajan voitot ylittävät 10. sijan pisteet, pelaaja pääsee listalle.
    if pelaaja_voitot > kynnys:
        while True:
            # Kysytään pelaajan nimimerkki uuden ennätyksen tallentamiseksi.
            nimimerkki = input(
                "Def: Congratulations! You set a new record! Enter your nickname, which will be engraved on the scoreboard! [A-Z,0-9] (Max 10 characters): "
            ).upper()
            # Nimimerkin tulee sisältää vain sallittuja merkkejä ja olla enintään 10 merkkiä pitkä.
            if nimimerkki.isalnum() and len(nimimerkki) <= 10:
                print("--- Your nickname was accepted! ---")
                # Tallennetaan nimimerkki ja voitot tietokantaan.
                Database.lisää_tietokantaan(nimimerkki, pelaaja_voitot)
                # Poistetaan edellisen 10. sijan pelaajan nimerkki ja pisteet tietokannasta.
                Database.poista_tietokannasta(kynnys)
                # Näytetään päivitetty top 10 -lista.
                Database.lue_tietokanta_taulu()
                # Palauttaa Stringin jos lisättiin tietokantaan.
                return "You are in top 10!"
            else:
                print("Invalid nickname, try again! [A-Z,0-9]")
    # Pelaajan pisteet eivät riittäneet listalle.
    else:
        # Palauttaa Stringin jos pisteet eivät riittäneet listalle.
        return "You do not qualify for the top 10..."


# Pelin pääfunktio, joka hallinnoi koko peliä.
def peli():
    kierrokset = 1  # Kierros-laskuri.
    pelaaja_voitot = 0  # Voitto-laskuri.

    while True:
        # Näytetään nykyisen kierroksen numero.
        print(f"ROUND {kierrokset}.")
        # Näytetään pelaajan voitot.
        print(f"Total Wins: {pelaaja_voitot}")

        # Suoritetaan yksi pelikierros ja saadaan tulos.
        tulos = kierros()

        # Jos tulos on pelaajan voitto, jatketaan seuraavaan kierrokseen.
        if tulos == 1:
            # Lisätään voittojen määrää, jos pelaaja voittaa.
            pelaaja_voitot += 1
            # Lisätään kierrosten määrää, jos pelaaja voittaa.
            kierrokset += 1
        # Jos tulos on pelaajan tasapeli, jatketaan seuraavaan kierrokseen.
        elif tulos == 0:
            # Lisää kierros myös tasapelissä
            kierrokset += 1
        elif tulos == -1:
            # Tarkistetaan, pääseekö pelaaja top 10 -listalle.
            top10_tulos = top10(pelaaja_voitot)
            # Näytä pelaajalle tulos
            print(top10_tulos)

            if top10_tulos == "You are in top 10!":
                # Nollataan voitot, jos pelajaa häviää.
                pelaaja_voitot = 0
                # Nollataan kierrokset, jos pelaaja häviää.
                kierrokset = 1
                # Kysytään pelaajalta, haluaako hän jatkaa.
                if not jatketaanko():
                    break

            elif top10_tulos == "You do not qualify for the top 10...":
                # Nollataan voitot, jos pelajaa häviää.
                pelaaja_voitot = 0
                # Nollataan kierrokset, jos pelaaja häviää.
                kierrokset = 1
                # Kysytään pelaajalta, haluaako hän jatkaa.
                if not jatketaanko():
                    break

    # Lopuksi näytetään kiitosviesti.
    print("--- Thanks for playing! ---")
