import psycopg2
from config import load_config

import logging

import queries as sql
import default_values as defv

logger = logging.getLogger(__name__)
logging.basicConfig(filename="init_db.log", encoding="utf-8", level=logging.DEBUG)


# TODO: add TYPE of the 22 uniquely-named tropical fish


def insert_color(color, color_eng):

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(
                    sql.Q_INSERT_COLOR,
                    (
                        color,
                        color_eng,
                    ),
                )

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)


def insert_tropical_fish_type(type, type_eng):
    """Insert new tropical fish type into the tropical_fishes_type table"""


    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(
                    sql.Q_INSERT_TYPE,
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

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(
                    sql.Q_INSERT_NAME,
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

   
    for c, c_eng in zip(defv.colors, defv.colors_eng):
        insert_color(c, c_eng)
    
    for f, f_eng in zip(defv.fish_types, defv.fish_types_eng):
        insert_tropical_fish_type(f, f_eng)

    for f, f_eng in zip(defv.fish_name, defv.fish_name_eng):
        insert_tropical_fish_name(f, f_eng)
