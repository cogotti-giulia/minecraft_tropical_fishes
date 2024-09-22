import psycopg2
from config import load_config

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename="create_tables.log", encoding="utf-8", level=logging.DEBUG)


# TODO: in tropical_fishes_variant table set as not null type and base and pattern color when added to the unique name fishes

def create_tables():
    """create tables in postgreSQL db"""
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

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the CREATE TABLE statement
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        logger.debug(error)
