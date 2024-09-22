import psycopg2
import sys
from database.config import load_config
import database.queries as sql

import logging

NONE_FIELD = None

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename="database/utils.log",
    encoding="utf-8",
    level=logging.DEBUG,
)


# insert data
def insert_user(username):
    """insert a new minecraft user into users table"""

    config = load_config("/database")

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    sql.Q_SEARCH_USER,
                    [
                        username,
                    ],
                )

                if cur.rowcount == 0:  # no results
                    cur.execute(sql.Q_INSERT_USER, (username,))

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)


# search data
def search_tropical_fish_variant(
    is_unique,
    fish_name=None,
    fish_type=None,
    fish_base_color=None,
    fish_pattern_color=None,
):

    fishvariant_id = None
    
    config = load_config("/database")

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # get id of the tp fish
                
                if is_unique:
                    cur.execute(
                        sql.Q_GET_ID_NAME,
                        (
                            fish_name,
                            fish_name,
                        ),
                    )

                    # get the result id
                    fishname_id = cur.fetchone()[0]
               
                    cur.execute(
                        sql.Q_GET_ID_VARIANT_UNIQUE22,
                        (

                            fishname_id,
                        ),
                    )

                    if cur.rowcount != 0:
                        fishvariant_id = cur.fetchone()[0]

                else:
                    cur.execute(
                        sql.Q_GET_ID_TYPE,
                        (
                            fish_type,
                            fish_type,
                        ),
                    )

                    fishtype_id = cur.fetchone()[0]

                    # search for base and pattern color id
                    cur.execute(
                        sql.Q_GET_ID_COLOR,
                        (
                            fish_base_color,
                            fish_base_color,
                        ),
                    )
                    basecolor_id = cur.fetchone()[0]

                    cur.execute(
                        sql.Q_GET_ID_COLOR,
                        (
                            fish_pattern_color,
                            fish_pattern_color,
                        ),
                    )
                    patterncolor_id = cur.fetchone()[0]

                    cur.execute(
                        sql.Q_GET_ID_VARIANT,
                        (
                            fishtype_id,
                            basecolor_id,
                            patterncolor_id,
                        ),
                    )

                    if cur.rowcount != 0:
                        fishvariant_id = cur.fetchone()[0]

                # commit the changes to the database
                conn.commit()

                return fishvariant_id
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)


def insert_tropical_fish_variant(
    is_unique,
    new_fish_name=None,
    new_fish_type=None,
    new_fish_base_color=None,
    new_fish_pattern_color=None,
):
    """Insert new tropical fish with type in the tropical_fishes table"""
    fishvariant_id = None
  
    config = load_config("/database")

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                if is_unique:
                    cur.execute(
                        sql.Q_GET_ID_NAME,
                        (
                            new_fish_name,
                            new_fish_name,
                        ),
                    )

                    if cur.rowcount != 0:
                        # get the result id
                        fishname_id = cur.fetchone()[0]

                        # insert into tp fish table
                        cur.execute(
                            sql.Q_INSERT_VARIANT_UNIQUE22,
                            (
                                True,
                                fishname_id,
                            ),
                        )

                        if cur.rowcount != 0:
                            fishvariant_id = cur.fetchone()[0]
                else:
                    cur.execute(
                        sql.Q_GET_ID_TYPE,
                        (
                            new_fish_type,
                            new_fish_type,
                        ),
                    )

                    if cur.rowcount != 0:
                        fishtype_id = cur.fetchone()[0]
                        # search for base and pattern color id
                        cur.execute(
                            sql.Q_GET_ID_COLOR,
                            (
                                new_fish_base_color,
                                new_fish_base_color,
                            ),
                        )
                        basecolor_id = cur.fetchone()[0]

                        cur.execute(
                            sql.Q_GET_ID_COLOR,
                            (
                                new_fish_pattern_color,
                                new_fish_pattern_color,
                            ),
                        )
                        patterncolor_id = cur.fetchone()[0]
                        # execute the INSERT statement
                        cur.execute(
                            sql.Q_INSERT_VARIANT,
                            (
                                False,
                                fishtype_id,
                                basecolor_id,
                                patterncolor_id,
                            ),
                        )

                        if cur.rowcount != 0:
                            fishvariant_id = cur.fetchone()[0]

                # commit the changes to the database
                conn.commit()

                return fishvariant_id
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)


def owner_and_tropical_fish(
    is_unique,
    owner,
    fish_name=None,
    fish_type=None,
    fish_base_color=None,
    fish_pattern_color=None,
):

    fishvariant_id = search_tropical_fish_variant(
        is_unique,
        fish_name,
        fish_type,
        fish_base_color,
        fish_pattern_color,
    )

    # not found, insert a new variant of fish
    if fishvariant_id == None:
        fishvariant_id = insert_tropical_fish_variant(
            is_unique,
            fish_name,
            fish_type,
            fish_base_color,
            fish_pattern_color,
        )

    config = load_config("/database")

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                cur.execute(sql.Q_INSERT_FISH_OWNER, (owner, fishvariant_id))

                # commit the changes to the database
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)

    return fishvariant_id
