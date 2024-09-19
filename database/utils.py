import psycopg2
import sys
from database.config import load_config

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="utils.log",
    encoding="utf-8",
    level=logging.DEBUG,
)


def insert_user(username):
    """insert a new minecraft user into users table"""

    q_search_user = "SELECT * FROM users WHERE username = %s"

    q_insert_user = "INSERT INTO users(username) VALUES(%s)"

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(
                    q_search_user,
                    [
                        username,
                    ],
                )

                if cur.rowcount == 0:  # no results
                    cur.execute(q_insert_user, (username,))

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)


def search_tropical_fish_variant(
    is_unique,
    fish_name=None,
    fish_type=None,
    fish_base_color=None,
    fish_pattern_color=None,
):
    q_get_id_from_tpfishname = "SELECT id FROM tropical_fishes_name\
                                    WHERE (name = %s OR name_eng = %s)"

    q_get_id_from_tpfishvariant_22unique = "SELECT id FROM tropical_fishes_variants\
                                    WHERE (is_unique AND name_id = %s)"

    q_get_id_from_tpfishtype = "SELECT id FROM tropical_fishes_type\
                                    WHERE (type = %s OR type_eng = %s)"

    q_get_id_form_colors = "SELECT id FROM colors\
                            WHERE (color = %s OR color_eng = %s)"

    q_get_id_from_tpfishvariant = "SELECT id FROM tropical_fishes_variants\
                                    WHERE not is_unique AND\
                                    (type_id = %s AND base_color_id = %s AND pattern_color_id = %s)"

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # get id of the tp fish

                if is_unique:
                    cur.execute(
                        q_get_id_from_tpfishname,
                        (
                            fish_name,
                            fish_name,
                        ),
                    )

                    # get the result id
                    fishname_id = cur.fetchone()[0]
                    cur.execute(
                        q_get_id_from_tpfishvariant_22unique,
                        (fishname_id,),
                    )

                    if cur.rowcount != 0:
                        fishvariant_id = cur.fetchone()[0]

                else:
                    cur.execute(
                        q_get_id_from_tpfishtype,
                        (
                            fish_type,
                            fish_type,
                        ),
                    )

                    fishtype_id = cur.fetchone()[0]

                    # search for base and pattern color id
                    cur.execute(
                        q_get_id_form_colors,
                        (
                            fish_base_color,
                            fish_base_color,
                        ),
                    )
                    basecolor_id = cur.fetchone()[0]

                    cur.execute(
                        q_get_id_form_colors,
                        (
                            fish_pattern_color,
                            fish_pattern_color,
                        ),
                    )
                    patterncolor_id = cur.fetchone()[0]

                    cur.execute(
                        q_get_id_from_tpfishvariant,
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

    # UNIQUE
    q_get_id_from_tpfishname = "SELECT id FROM tropical_fishes_name\
                                    WHERE (name = %s OR name_eng = %s)"

    q_insert_variant_tpfish22 = "INSERT INTO tropical_fishes_variants(is_unique, name_id) VALUES(%s, %s) RETURNING *"

    # NOT UNIQUE
    q_get_id_from_tpfishtype = "SELECT id FROM tropical_fishes_type\
                                    WHERE (type = %s OR type_eng = %s)"

    q_get_id_form_colors = "SELECT id FROM colors\
                            WHERE (color = %s OR color_eng = %s)"

    q_insert_variant_tpfish = "INSERT INTO tropical_fishes_variants(is_unique, type_id, base_color_id, pattern_color_id)\
            VALUES(%s, %s, %s, %s) RETURNING id"

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                if is_unique:
                    cur.execute(
                        q_get_id_from_tpfishname,
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
                            q_insert_variant_tpfish22,
                            (
                                True,
                                fishname_id,
                            ),
                        )
                        fishvariant_id = cur.fetchone()[0]
                else:
                    cur.execute(
                        q_get_id_from_tpfishtype,
                        (
                            new_fish_type,
                            new_fish_type,
                        ),
                    )

                    if cur.rowcount != 0:
                        fishtype_id = cur.fetchone()[0]
                        # search for base and pattern color id
                        cur.execute(
                            q_get_id_form_colors,
                            (
                                new_fish_base_color,
                                new_fish_base_color,
                            ),
                        )
                        basecolor_id = cur.fetchone()[0]

                        cur.execute(
                            q_get_id_form_colors,
                            (
                                new_fish_pattern_color,
                                new_fish_pattern_color,
                            ),
                        )
                        patterncolor_id = cur.fetchone()[0]
                        # execute the INSERT statement
                        cur.execute(
                            q_insert_variant_tpfish,
                            (
                                False,
                                fishtype_id,
                                basecolor_id,
                                patterncolor_id,
                            ),
                        )

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

    # reference to the owner of the fish
    q_insert_fish_owner = "INSERT INTO owner_and_tropical_fishes(owner, tropical_fish) VALUES(%s, %s) RETURNING id"

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                cur.execute(q_insert_fish_owner, (owner, fishvariant_id))

                # commit the changes to the database
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)
