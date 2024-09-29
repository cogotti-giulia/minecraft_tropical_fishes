import psycopg2
import sys
import logging

import numpy as np

import database.queries as sql

from os.path import exists
from database.config import load_config

from colorama import init, Style, Fore

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename="database/utility.log",
    encoding="utf-8",
    level=logging.DEBUG,
)

# TODO: add something like getting more statistic

############################### INSERT DATA ###########################


def insert_user(username):
    """insert a new minecraft user into users table"""

    config = load_config()

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


def insert_tropical_fish_variant(
    is_unique,
    new_fish_name=None,
    new_fish_type=None,
    new_fish_base_color=None,
    new_fish_pattern_color=None,
):
    """Insert new tropical fish with type in the tropical_fishes table"""
    fishvariant_id = None

    config = load_config()

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

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                cur.execute(sql.Q_INSERT_FISH_OWNER, (owner, fishvariant_id))

                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)

    return fishvariant_id


def insert_data_from_file(username, filename):
    init(autoreset=True)

    if not exists(filename):
        msg = "*** Warning! The file " + filename + " doesn't exists.***"
        print(Style.BRIGHT + Fore.RED + msg)

    else:
        # check if user already exists
        # otherwise add to db
        insert_user(username)

        r = 0
        bad_lines = list()

        with open(filename, "r") as file:
            for line in file:
                r = r + 1

                line_no_eol = line.replace("\n", "")  # to remove newlines '\n'
                words = line_no_eol.split(",")  # split line on '-'
                # print(len(words))
                # print(words)

                if len(words) == 1:  # unique fishes
                    ris = owner_and_tropical_fish(True, username, words[0].lower())

                    if ris is None:
                        bad_lines.append(line)

                elif len(words) == 2:  # fish with same base and patter color
                    # words.append(words[-1])
                    ris = owner_and_tropical_fish(
                        False,
                        username,
                        None,
                        words[0].lower(),
                        words[1].lower(),
                        words[1].lower(),
                    )

                    if ris is None:
                        bad_lines.append(line)

                elif len(words) == 3:  # default fishing name
                    ris = owner_and_tropical_fish(
                        False,
                        username,
                        None,
                        words[0].lower(),
                        words[1].lower(),
                        words[2].lower(),
                    )
                    if ris is None:
                        bad_lines.append(line)

                else:
                    logger.error(
                        "*** Skipping row {}. ***\nFile is bad formatted.\nPlease check your file.".format(
                            r
                        )
                    )

        open(filename, "w").close()  # delete file

        if bad_lines:
            # delete all rows except the bad formattend (also print it for user)
            with open(filename, "r+") as file:
                for l in bad_lines[:-1]:
                    file.write(l)

                file.write(bad_lines[-1].replace("\n", ""))
                file.truncate()

            msg = "*** Something went wrong! Please fix your grammar on the text file, then try again! ***\n"
            print(Style.BRIGHT + Fore.RED + msg)

            print(Style.NORMAL + Fore.RED + "All tropical fishes are now stored in the database, except for:")
            r = 0
            for l in bad_lines:
                r = r + 1
                str_r = str(r)
                print(Style.DIM + Fore.RED + str_r + Style.RESET_ALL + " " + l.replace("\n", ""))
        else:
            msg = "\n*** Everything went well, all tropical fishes are now stored in the database! ***\n"
            print(Style.DIM + Fore.WHITE + msg)



############################### SEARCH DATA ###########################


def search_tropical_fish_variant(
    is_unique,
    fish_name=None,
    fish_type=None,
    fish_base_color=None,
    fish_pattern_color=None,
):

    fishvariant_id = None

    config = load_config()

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
                        (fishname_id,),
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


############################### GET DATA #############################


def get_data_from_db_given_user(username, query):
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                cur.execute(query, (username,))

                if cur.rowcount != 0:
                    return cur.fetchall()

                return None

                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)


def count_variant_user(username):

    search_user = get_data_from_db_given_user(username, sql.Q_SEARCH_USER)

    if search_user:
        result = get_data_from_db_given_user(username, sql.Q_COUNT_VARIANT_USER)

        return result[0][0]

    return None


def count_name_and_list_user(username):

    search_user = get_data_from_db_given_user(username, sql.Q_SEARCH_USER)

    if search_user:
        result_name = get_data_from_db_given_user(username, sql.Q_COUNT_NAME_LIST)
        result_type = get_data_from_db_given_user(username, sql.Q_COUNT_TYPE_LIST)

        # total rows just to show it
        total = (0 if result_name is None else len(result_name)) + (
            0 if result_type is None else len(result_type)
        )
        tmp_type = []
        tmp_tot = []
        for el in result_type:
            # concatenate type, base color and pattern color
            tmp = el[0] + " " + el[1] + " " + el[2]
            tmp_type.append(tmp)
            tmp_tot.append(el[3])

        list_type = []
        for i, j in zip(tmp_type, tmp_tot):
            list_type.append((i, j))

        list_variants = result_name + list_type
        list_variants.sort()

        # all variants with total of each ordered in alphabetic order
        np_variants = np.array(list_variants)

        return (np_variants, total)

    return None, None


############################ INSERT DATA ############################


def insert_one_color(color_ita, color_eng):

    config = load_config()

    try:
        with psycopg2.connect(**config) as con:
            with con.cursor() as cur:
                cur.execute(
                    sql.INSERT_COLOR,
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
                        sql.Q_INSERT_COLOR,
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
                    sql.Q_INSERT_TYPE,
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
                        sql.Q_INSERT_TYPE,
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
                    sql.Q_INSERT_NAME,
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
                        sql.Q_INSERT_NAME,
                        (
                            n_ita,
                            n_eng,
                        ),
                    )

                con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)
