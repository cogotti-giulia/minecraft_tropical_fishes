import psycopg2
from config import load_config

import sys
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename="insert.log", encoding="utf-8", level=logging.DEBUG)

import utils 

#TODO: sistemare le query con gli id
#TODO: svuota file
#TODO: vedere se posso scrivere su file da comando carpet


if __name__ == "__main__":

    argv = sys.argv
    username = argv[1].lower()
    filename = argv[2]

    # check if user already exists
    # otherwise add to db
    utils.insert_user(username)

    r = 0
    with open(filename) as file:
        for line in file:
            r = r + 1

            line_no_eol = line.replace("\n", "")  # to remove newlines '\n'
            words = line_no_eol.split("-")  # split line on '-'
            # print(len(words))
            # print(words)

            if len(words) == 1:  # unique fishes
                utils.owner_and_tropical_fish(True, username, words[0].lower())
            elif len(words) == 2:  # fish with same base and patter color
                # words.append(words[-1])
                utils.owner_and_tropical_fish(
                    False,
                    username,
                    None,
                    words[0].lower(),
                    words[1].lower(),
                    words[1].lower(),
                )
            elif len(words) == 3:  # default fishing name
                utils.owner_and_tropical_fish(
                    False,
                    username,
                    None,
                    words[0].lower(),
                    words[1].lower(),
                    words[2].lower(),
                )
            else:
                logger.error(
                    "*** Skipping row {}. ***\nFile is bad formatted.\nPlease check your file.".format(
                        r
                    )
                )
