import sys
import time
import logging
import numpy as np

from database.utility import insert_data_from_file
from database.utility import count_variant_user
from database.utility import count_name_and_list_user

from tabulate import tabulate

logger = logging.getLogger(__name__)
logging.basicConfig(filename="app.log", encoding="utf-8", level=logging.ERROR)

# TODO: add compatibility with windows like systems

if __name__ == "__main__":

    exit = False
    while not exit:
        action = input(
            "1 Insert new fishes from file\
                    \n2 Get some data \
                    \n3 Exit\
                    \n==> Select one option (es: 1)\
                    \n==> "
        )
        match (action):
            case "1":

                username = input("Enter minecraft username: ").lower()
                filename = input("Enter filename of tropical fishes: ")
                insert_data_from_file(username, filename)

                input("\n==> Press Enter to continue...\n")

            case "2":
                exit_action_get = False

                print("", end="\n")

                while not exit_action_get:

                    action_get = input(
                        "(2) 1 Total number of distinct variants (requires username)\
                        \n(2) 2 List of all variants (requires username)\
                        \n(2) 3 Go back\
                        \n==> Select one option (es: 1)\
                        \n==> "
                    )

                    match (action_get):
                        case "1":
                            username = input("Enter minecraft username: ").lower()
                            
                            total = count_variant_user(username)

                            if(total is None):
                                print("\n==> Something went wrong... Pls check if ", username, "exists")
                            else:
                                print(
                                    "\nWOW! ",
                                    username,
                                    "has discoverd ",
                                    total,
                                    " of 2700 variants of tropical fishes!\n",
                                )

                            input("\n==> Press Enter to continue...\n")
                        case "2":
                            username = input("Enter minecraft username: ").lower()
                            np_variants, total = count_name_and_list_user(username)

                            if(np_variants is None):
                                print("\n==> Something went wrong... Pls check if ", username, "exists")
                            else:
                                print(
                                    "\nList of the ",
                                    count_variant_user(username),
                                    " of 2700 variants of tropical fishes discovered by",
                                    username,
                                    "\n",
                                )

                                print(
                                    tabulate(
                                        np_variants,
                                        headers=["Variant", "Total"],
                                        tablefmt="grid",
                                    )
                                )
                            input("\n==> Press Enter to continue...\n")

                        case "3":
                            if input("Are you sure? [y/N]") == "y":
                                exit_action_get = True

                            print("", end="\n")

                        case _:
                            print("*** You should select an option :( ***", end="\n\n")
                            time.sleep(0.7)

            case "3":
                if input("Are you sure? [y/N]") == "y":
                    exit = True

                print("", end="\n")

            case _:
                print("*** You should select an option :( ***", end="\n\n")
                time.sleep(0.7)

    print("Thank you, bye!")
