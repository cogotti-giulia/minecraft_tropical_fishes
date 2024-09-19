import psycopg2
from config import load_config

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename="init_db.log", encoding="utf-8", level=logging.DEBUG)


# TODO: add type of the 22 uniquely-named tropical fish


def insert_color(color, color_eng):
    """insert a new color into colors table"""

    sql = "INSERT INTO colors(color, color_eng) VALUES(%s, %s)"

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(
                    sql,
                    (
                        color,
                        color_eng,
                    ),
                )

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_tropical_fish_type(type, type_eng):
    """Insert new tropical fish type into the tropical_fishes_type table"""

    sql = "INSERT INTO tropical_fishes_type(type, type_eng) VALUES(%s, %s) RETURNING *"

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(
                    sql,
                    (
                        type,
                        type_eng,
                    ),
                )

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)


def insert_tropical_fish_name(name, name_eng):
    """Insert unique 22 tropical fishes name type into the tropical_fishes_name table"""

    sql = "INSERT INTO tropical_fishes_name(name, name_eng) VALUES(%s, %s) RETURNING *"

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(
                    sql,
                    (
                        name,
                        name_eng,
                    ),
                )

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)


if __name__ == "__main__":

    colors = [
        "nero",
        "blu",
        "marrone",
        "ciano",
        "verde",
        "azzurro",
        "grigio chiaro",
        "grigio",
        "lime",
        "magenta",
        "arancione",
        "rosa",
        "viola",
        "rosso",
        "bianco",
        "giallo",
    ]

    colors_eng = [
        "black",
        "blue",
        "brown",
        "cyan",
        "green",
        "light blue",
        "light gray",
        "gray",
        "lime",
        "magenta",
        "orange",
        "pink",
        "purple",
        "red",
        "white",
        "yellow",
    ]

    for c, c_eng in zip(colors, colors_eng):
        insert_color(c, c_eng)

    # betty
    # kob
    # clayfish = pesce creta
    # blockfish = pesce blocco
    # sunstreak = pesce raggio di sole
    # snooper = ficcanaso
    # flooper = pesce salterino
    # brinely = pesce pelagico
    # spotty = pesce macchia
    # glitter = pesce scintilla
    # stripey= pesce striato
    # dasher = pesce scatto
    fish_types = [
        "pesce creta",
        "pesce striato",
        "pesce scintilla",
        "pesce salterino",
        "pesce raggio di sole",
        "pesce blocco",
        "pesce macchia",
        "betty",
        "kob",
        "pesce pelagico",
        "pesce ficcanaso",
        "pesce scatto",
    ]

    fish_types_eng = [
        "clayfish",
        "stripey",
        "glitter",
        "flopper",
        "sunstreak",
        "blockfish",
        "spotty",
        "betty",
        "kob",
        "brinely",
        "snooper",
        "dasher",
    ]

    for f, f_eng in zip(fish_types, fish_types_eng):
        insert_tropical_fish_type(f, f_eng)

    fish_name = [
        "anfiprione",
        "pesce chirurgo blu",
        "pesce chirurgo nero",
        "pesce chirurgo giallo",
        "pesce farfalla",
        "pesce farfalla ornato",
        "ciclide",
        "pesce pagliaccio",
        "pesce combattente rosa",
        "pseudocromide",
        "azzannatore rosso",
        "triglia",
        "idolo moresco",
        "pesce pappagallo",
        "pesce angelo regina",
        "ciclide rosso",
        "bavosa rossa",
        "dentice rosso",
        "pesce capitano",
        "pesce pagliaccio pomodoro",
        "pesce balestra",
        "pesce pappagallo a pinna gialla",
    ]

    fish_name_eng = [
        "anemone",
        "blue tang",
        "black tang",
        "yellow tang",
        "butterflyfish",
        "ornate butterflyfish",
        "cichlid",
        "clownfish",
        "cotton candy betta",
        "dottyback",
        "emperor red snapper",
        "goatfish",
        "moorish idol",
        "parrotfish",
        "queen angelfish",
        "red cichlid",
        "red lipped blenny",
        "red snapper",
        "threadfin",
        "tomato clownfish",
        "triggerfish",
        "yellowtail parrotfish",
    ]

    for f, f_eng in zip(fish_name, fish_name_eng):
        insert_tropical_fish_name(f, f_eng)
