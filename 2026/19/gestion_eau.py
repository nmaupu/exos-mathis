# ------------------------------------
# gestion_eau.py
# Programme de contrôle des réservoirs
# ------------------------------------
from donnees import reservoirs

# Question 1 : écrire la fonction est_en_penurie


def est_en_penurie(reservoirs, nom_reservoir):
    """
    Renvoie True si le réservoir nommé nom_reservoir a un taux
    de remplissage strictement inférieur à 20 %, False sinon.
    """
    for r in reservoirs:
        if r["nom"] == nom_reservoir:
            taux = r["volume"] / r["capacite"]
            return taux < 0.20

# Question 2 : écrire la fonction volume_par_district


def volume_par_district(reservoirs):
    """
    Renvoie un dictionnaire associant chaque district au volume
    total d'eau (en litres) disponible dans ce district.
    """
    volumes = {}
    for r in reservoirs:
        district = r["district"]
        if district not in volumes:
            volumes[district] = 0
        volumes[district] += r["volume"]
    return volumes

# Question 3


def volume_moyen(reservoirs):
    """
    Renvoie le volume moyen d'eau disponible dans les réservoirs.
    """
    somme_totale = 0
    for r in reservoirs:
        somme_totale += r["volume"]
    moyenne = somme_totale / len(reservoirs)
    return moyenne


# Tests Question 3 :
# Test 1 : la liste contient au moins un réservoir
test1 = [{"nom": "A", "capacite": 1000, "volume": 500, "district": "X"}]
assert len(test1) >= 1

# Test 2 : la moyenne doit être <= la plus grande capacité
moyenne = volume_moyen(reservoirs)
capacite_max = max(r["capacite"] for r in reservoirs)
assert moyenne <= capacite_max

# Test 3 : deux réservoirs avec le même volume
test3 = [
    {"nom": "A", "capacite": 1000, "volume": 400, "district": "X"},
    {"nom": "B", "capacite": 2000, "volume": 400, "district": "Y"}
]
assert volume_moyen(test3) == 400


# Question 4


def liste_districts(reservoirs):
    """
    Renvoie la liste des districts présents dans les données.
    """
    liste = []
    for r in reservoirs:
        if (r["district"] not in liste):
            liste.append(r["district"])
    return liste


def reservoirs_par_district(reservoirs):
    """
    Renvoie un dictionnaire associant chaque district à la liste
    des réservoirs qui s’y trouvent.
    """
    liste_rpd = {}
    for r in reservoirs:
        district = r["district"]
        if district not in liste_rpd:
            liste_rpd[district] = []
        liste_rpd[district].append(r)
    return liste_rpd


def districts_vulnerables(reservoirs):
    """
    Renvoie la liste des districts dont le volume moyen est
    inférieur à 80 % du volume moyen global.
    """
    moyenne_globale = volume_moyen(reservoirs)
    seuil = 0.80 * moyenne_globale
    rpd = reservoirs_par_district(reservoirs)
    vulnerables = []
    for district in liste_districts(reservoirs):
        moyenne_district = volume_moyen(rpd[district])
        if moyenne_district < seuil:
            vulnerables.append(district)
    return vulnerables
