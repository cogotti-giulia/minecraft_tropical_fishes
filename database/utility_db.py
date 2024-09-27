import os
from os.path import exists
import logging
import pandas as pd

import psycopg2
import psycopg2.sql as sql

import database.utility as utils
from configparser import ConfigParser

from database.config import load_config

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from database.queries import Q_CHECK_IF_DB_EXISTS
from database.queries import Q_CHECK_IF_ROLE_EXISTS
from database.queries import Q_INSERT_COLOR
from database.queries import Q_INSERT_TYPE
from database.queries import Q_INSERT_NAME

# TODO: FIX GRANT PERMISSION ON CRATED USER (now it's superuser, need to find a better way to grant only necessary privileges!) :/

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename="database/utility_db.log",
    encoding="utf-8",
    level=logging.DEBUG,
)


# create db from ini file if not exists
def check_if_db_exists():
    config = load_config()

    db_name = config.get("database")

    con = psycopg2.connect(
        user="postgres",
        host="127.0.0.1",
        port="5432",
        password="",
    )
    cur = con.cursor()
    cur.execute(
        Q_CHECK_IF_DB_EXISTS,
        (db_name,),
    )

    if cur.rowcount == 0:
        create_database(config)

    init_db()


# create role with superuser permission
def create_user_role(db_user, db_psw):
    con = psycopg2.connect(
        user="postgres",
        host="127.0.0.1",
        port="5432",
        password="",
    )

    with con.cursor() as cur:
        try:
            cur.execute(
                sql.SQL("CREATE ROLE {0} LOGIN PASSWORD {1} SUPERUSER").format(
                    sql.Identifier(db_user),
                    sql.Literal(db_psw),
                )
            )

            con.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


# create database getting user config
def create_database(config):

    db_name = config.get("database")
    db_user = config.get("user")
    db_psw = config.get("password")

    con = psycopg2.connect(
        user="postgres",
        host="127.0.0.1",
        port="5432",
        password="",
    )

    is_superuser = False
    with con.cursor() as cur:
        try:
            cur.execute(
                Q_CHECK_IF_ROLE_EXISTS,
                (db_user,),
            )

            if cur.rowcount == 0:
                create_user_role(db_user, db_psw)
                is_superuser = True

        except (Exception, psycopg2.DatabaseError) as error:
            logging.debug(error)

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- ADD THIS LINE

    with con.cursor() as cur:
        try:

            if not is_superuser:
                cur.execute(
                    sql.SQL("ALTER USER {0} WITH SUPERUSER").format(
                        sql.Identifier(db_user)
                    )
                )
                con.commit()

            cur.execute(sql.SQL("CREATE DATABASE {0}").format(sql.Identifier(db_name)))
            con.commit()
            print("\n*** Successfully connected to the database ***\n")

        except (Exception, psycopg2.DatabaseError) as error:
            logging.debug(error)

    con.close()


######################## INIT DB TABLES ###############################À


def init_db():

    # create tables!
    create_tables()
    # fill table color with default ita/eng values
    df_color = pd.read_csv("database/default_values/colors.csv")
    arr_color_ita = df_color["ITA"].values
    arr_color_eng = df_color["ENG"].values
    utils.insert_many_color(arr_color_ita, arr_color_eng)

    # fill type table with default ita/eng values
    df_type = pd.read_csv("database/default_values/types.csv")
    arr_type_ita = df_type["ITA"].values
    arr_type_eng = df_type["ENG"].values
    utils.insert_many_tropical_fish_type(arr_type_ita, arr_type_eng)

    # fill name table with default ita/eng values
    df_name = pd.read_csv("database/default_values/names.csv")
    arr_name_ita = df_name["ITA"].values
    arr_name_eng = df_name["ENG"].values
    utils.insert_many_tropical_fish_name(arr_name_ita, arr_name_eng)

    # TODO: ADD INTO THE DATABASE TYPE AND COLOR OF THE 22 REAL LIFE SPECIES
    df_ntc = pd.read_csv("database/default_values/realLife_names_types_colors.csv")
    # print(df_ntc)


def create_tables():
    commands = (
        """
            CREATE TABLE users (
                username VARCHAR(255) PRIMARY KEY
            )
        """,
        """
            CREATE TABLE color (
                id SERIAL NOT NULL PRIMARY KEY,
                color VARCHAR(255) UNIQUE NOT NULL,
                color_eng VARCHAR(255) UNIQUE NOT NULL
            )
        """,
        """
            CREATE TABLE tropical_fish_type (
                id SERIAL NOT NULL PRIMARY KEY,
                type VARCHAR(255) UNIQUE NOT NULL,
                type_eng VARCHAR(255) UNIQUE NOT NULL
            )
        """,
        """
            CREATE TABLE tropical_fish_name (
                id SERIAL NOT NULL PRIMARY KEY,
                name VARCHAR(255) UNIQUE NOT NULL,
                name_eng VARCHAR(255) UNIQUE NOT NULL,
                type_id INTEGER,

                FOREIGN KEY (type_id) REFERENCES tropical_fish_type (id)
            )
        """,
        """
            CREATE TABLE tropical_fish_variant (
                id SERIAL NOT NULL PRIMARY KEY,
                is_unique BOOLEAN NOT NULL,

                name_id INTEGER UNIQUE,
                type_id INTEGER,

                base_color_id  INTEGER,
                pattern_color_id INTEGER,
            
                UNIQUE(type_id, base_color_id, pattern_color_id),

                FOREIGN KEY (base_color_id) REFERENCES color (id),
                FOREIGN KEY (pattern_color_id) REFERENCES color (id),
                FOREIGN KEY (type_id) REFERENCES tropical_fish_type (id),
                FOREIGN KEY (name_id) REFERENCES tropical_fish_name (id)
                
            )
        """,
        """
            CREATE TABLE owner_and_tropical_fish (
                id SERIAL NOT NULL PRIMARY KEY,
                owner VARCHAR(255) NOT NULL,
                tropical_fish INTEGER NOT NULL,

                FOREIGN KEY (owner) REFERENCES users (username) ON DELETE CASCADE,
                FOREIGN KEY (tropical_fish) REFERENCES tropical_fish_variant (id) ON DELETE CASCADE
            )
        """,
    )

    config = load_config()

    try:
        with psycopg2.connect(**config) as con:
            with con.cursor() as cur:

                # execute the CREATE TABLE statement
                for command in commands:
                    cur.execute(command)

    except (psycopg2.DatabaseError, Exception) as error:
        logger.debug(error)
