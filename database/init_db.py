import psycopg2
from config import load_config

import os

import logging

import pandas as pd
import queries as sql

from create_tables import create_tables

logger = logging.getLogger(__name__)
logging.basicConfig(filename="database/init_db.log", encoding="utf-8", level=logging.DEBUG)


def insert_one_color(color_ita, color_eng):

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    sql.Q_INSERT_COLOR,
                    (
                        color_ita,
                        color_eng,
                    ),
                )

                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)


def insert_many_color(arr_color_ita, arr_color_eng):
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                for c_ita, c_eng in zip(arr_color_ita, arr_color_eng):
                    cur.execute(
                        sql.Q_INSERT_COLOR,
                        (
                            c_ita,
                            c_eng,
                        ),
                    )

                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)


def insert_one_tropical_fish_type(type_ita, type_eng):
    """Insert new tropical fish type into the tropical_fishes_type table"""

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    sql.Q_INSERT_TYPE,
                    (
                        type_ita,
                        type_eng,
                    ),
                )

                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)


def insert_many_tropical_fish_type(arr_type_ita, arr_type_eng):

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                for t_ita, t_eng in zip(arr_type_ita, arr_type_eng):
                    cur.execute(
                        sql.Q_INSERT_TYPE,
                        (
                            t_ita,
                            t_eng,
                        ),
                    )

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)


def insert_one_tropical_fish_name(name_ita, name_eng):
    """Insert unique 22 tropical fishes name type into the tropical_fishes_name table"""

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    sql.Q_INSERT_NAME,
                    (
                        name_ita,
                        name_eng,
                    ),
                )

                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)


def insert_many_tropical_fish_name(arr_name_ita, arr_name_eng):

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for n_ita, n_eng in zip(arr_name_ita, arr_name_eng):
                    cur.execute(
                        sql.Q_INSERT_NAME,
                        (
                            n_ita,
                            n_eng,
                        ),
                    )

                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)


if __name__ == "__main__":

    # create tables!
    create_tables()
    # fill table color with default ita/eng values
    df_color = pd.read_csv(os.getcwd() + "/default_values/colors.csv")
    arr_color_ita = df_color["ITA"].values
    arr_color_eng = df_color["ENG"].values
    insert_many_color(arr_color_ita, arr_color_eng)

    # fill type table with default ita/eng values
    df_type = pd.read_csv(os.getcwd() + "/default_values/types.csv")
    arr_type_ita = df_type["ITA"].values
    arr_type_eng = df_type["ENG"].values
    insert_many_tropical_fish_type(arr_type_ita, arr_type_eng)

    # fill name table with default ita/eng values
    df_name = pd.read_csv(os.getcwd() + "/default_values/names.csv")
    arr_name_ita = df_name["ITA"].values
    arr_name_eng = df_name["ENG"].values
    insert_many_tropical_fish_name(arr_name_ita, arr_name_eng)

    # TODO: ADD INTO THE DATABASE TYPE AND COLOR OF THE 22 REAL LIFE SPECIES
    df_ntc = pd.read_csv(
        os.getcwd() + "/default_values/realLife_names_types_colors.csv"
    )
    print(df_ntc)
