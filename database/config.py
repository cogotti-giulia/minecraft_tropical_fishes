import os
from os.path import exists
import logging
import pandas as pd

import psycopg2
import psycopg2.sql as sql

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from database.queries import Q_CHECK_IF_DB_EXISTS
from database.queries import Q_CHECK_IF_ROLE_EXISTS
from database.queries import Q_INSERT_COLOR
from database.queries import Q_INSERT_TYPE
from database.queries import Q_INSERT_NAME

from configparser import ConfigParser


# TODO: FIX GRANT PERMISSION ON CRATED USER :/

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename="database/config.log",
    encoding="utf-8",
    level=logging.DEBUG,
)


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
                sql.SQL("CREATE ROLE {0} LOGIN PASSWORD {1}").format(
                    sql.Identifier(db_user),
                    sql.Literal(db_psw),
                )
            )

            con.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


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

    with con.cursor() as cur:
        try:
            cur.execute(
                Q_CHECK_IF_ROLE_EXISTS,
                (db_user,),
            )
        except (Exception, psycopg2.DatabaseError) as error:
            logging.debug(error)

    if cur.rowcount == 0:
        create_user_role(db_user, db_psw)

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- ADD THIS LINE

    with con.cursor() as cur:
        try:

            cur.execute(sql.SQL("CREATE DATABASE {0}").format(sql.Identifier(db_name)))
            con.commit()
            print("\n*** Successfully connected to the database ***\n")

        except (Exception, psycopg2.DatabaseError) as error:
            logging.debug(error)

    con.close()


def write_config_ini():
    # get input data
    db_name = input("Insert database name\n==> [minecraft] ")
    db_name = "minecraft" if db_name == "" else db_name
    db_user = input("Insert database user\n==> [postgres] ")
    db_user = "postgres" if db_user == "" else db_user
    db_psw = input("Insert database user password\n==> [] ")
    db_host = input("Insert database host\n==> [localhost] ")
    db_host = "localhost" if db_host == "" else db_host

    # write info in ini file
    ini_path = os.path.join("database/database.ini")

    with open(ini_path, "w") as file:
        line1 = "[postgresql]"
        line2 = "host=" + db_host
        line3 = "database=" + db_name
        line4 = "user=" + db_user
        line5 = "password=" + db_psw

        file.write("{}\n{}\n{}\n{}\n{}\n".format(line1, line2, line3, line4, line5))


def load_config(section="postgresql"):

    ini_path = os.path.join("database/database.ini")

    file_exists = exists(ini_path)
    if not file_exists or os.stat(ini_path).st_size == 0:

        print(
            "\n*** Oops the database configuration file doesn't exists, please follow the next instructions.***\n"
        )
        write_config_ini()

    parser = ConfigParser()
    parser.read(ini_path)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, ini_path)
        )

    return config


######################## INIT DB TABLES ###############################À


def init_db():
    config = load_config()
    db_user = config.get("user")

    try:
        with psycopg2.connect(**config) as con:
            with con.cursor() as cur:

                cur.execute(
                    sql.SQL("GRANT CREATE ON SCHEMA public TO {0};").format(
                        sql.Identifier(db_user)
                    )
                )

                con.commit()

                cur.execute(
                    sql.SQL(
                        "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO {0};"
                    ).format(sql.Identifier(db_user))
                )
                con.commit()

    except (psycopg2.DatabaseError, Exception) as error:
        logger.debug(error)
    # create tables!
    create_tables()
    # fill table color with default ita/eng values
    df_color = pd.read_csv("database/default_values/colors.csv")
    arr_color_ita = df_color["ITA"].values
    arr_color_eng = df_color["ENG"].values
    insert_many_color(arr_color_ita, arr_color_eng)

    # fill type table with default ita/eng values
    df_type = pd.read_csv("database/default_values/types.csv")
    arr_type_ita = df_type["ITA"].values
    arr_type_eng = df_type["ENG"].values
    insert_many_tropical_fish_type(arr_type_ita, arr_type_eng)

    # fill name table with default ita/eng values
    df_name = pd.read_csv("database/default_values/names.csv")
    arr_name_ita = df_name["ITA"].values
    arr_name_eng = df_name["ENG"].values
    insert_many_tropical_fish_name(arr_name_ita, arr_name_eng)

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


def insert_one_color(color_ita, color_eng):

    config = load_config()

    try:
        with psycopg2.connect(**config) as con:
            with con.cursor() as cur:
                cur.execute(
                    INSERT_COLOR,
                    (
                        color_ita,
                        color_eng,
                    ),
                )

                con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)


def insert_many_color(arr_color_ita, arr_color_eng):
    config = load_config()

    try:
        with psycopg2.connect(**config) as con:
            with con.cursor() as cur:

                for c_ita, c_eng in zip(arr_color_ita, arr_color_eng):
                    cur.execute(
                        Q_INSERT_COLOR,
                        (
                            c_ita,
                            c_eng,
                        ),
                    )

                con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)


def insert_one_tropical_fish_type(type_ita, type_eng):
    """Insert new tropical fish type into the tropical_fishes_type table"""

    config = load_config()

    try:
        with psycopg2.connect(**config) as con:
            with con.cursor() as cur:
                cur.execute(
                    Q_INSERT_TYPE,
                    (
                        type_ita,
                        type_eng,
                    ),
                )

                con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)


def insert_many_tropical_fish_type(arr_type_ita, arr_type_eng):

    config = load_config()

    try:
        with psycopg2.connect(**config) as con:
            with con.cursor() as cur:

                for t_ita, t_eng in zip(arr_type_ita, arr_type_eng):
                    cur.execute(
                        Q_INSERT_TYPE,
                        (
                            t_ita,
                            t_eng,
                        ),
                    )

                # commit the changes to the database
                con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)


def insert_one_tropical_fish_name(name_ita, name_eng):
    """Insert unique 22 tropical fishes name type into the tropical_fishes_name table"""

    config = load_config()

    try:
        with psycopg2.connect(**config) as con:
            with con.cursor() as cur:
                cur.execute(
                    Q_INSERT_NAME,
                    (
                        name_ita,
                        name_eng,
                    ),
                )

                con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)


def insert_many_tropical_fish_name(arr_name_ita, arr_name_eng):

    config = load_config()

    try:
        with psycopg2.connect(**config) as con:
            with con.cursor() as cur:
                for n_ita, n_eng in zip(arr_name_ita, arr_name_eng):
                    cur.execute(
                        Q_INSERT_NAME,
                        (
                            n_ita,
                            n_eng,
                        ),
                    )

                con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)
