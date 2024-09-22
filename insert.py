import psycopg2

from database.utils import insert_user
from database.utils import owner_and_tropical_fish

import sys
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename="insert.log", encoding="utf-8", level=logging.ERROR)


# TODO: find out if i can integrate this with carpet

if __name__ == "__main__":

    argv = sys.argv
    username = argv[1].lower()
    filename = argv[2]

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

        print(
            "Something went wrong! Please fix your grammar on the text file, then try again!\nList of wrong lines:"
        )

        r = 0
        for l in bad_lines:
            r = r + 1
            str_r = str(r)
            print(str_r + " " + l.replace("\n", ""))
