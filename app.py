import sys
import time
import logging
import numpy as np

from tabulate import tabulate
from colorama import init, Style, Fore

from database.utility_init_db import check_if_db_exists

from database.utility_interact_db import insert_data_from_file
from database.utility_interact_db import count_variant_user
from database.utility_interact_db import count_name_and_list_user


logger = logging.getLogger(__name__)
logging.basicConfig(filename="app.log", encoding="utf-8", level=logging.ERROR)

# TODO: add compatibility with windows like systems
# TODO: maybe add an help for user

if __name__ == "__main__":
    init(autoreset=True)

    print(
        Style.BRIGHT
        + Fore.YELLOW
        + "\n\nHi, thank you for using this program! Hope it helps you collecting minecraft tropical fishes!\n"
    )
    check_if_db_exists()

    exit = False
    while not exit:
        print(
            "1 Insert new fishes from file\
                    \n2 Get some data \
                    \n3 Exit\
                    \n==> Select one option"
            + Style.DIM
            + Fore.WHITE
            + "(es:1)"
            + Style.RESET_ALL
        )
        action = input("==> ")
        match (action):
            case "1":

                username = input("Enter minecraft username: ").lower()
                filename = input("Enter filename of tropical fishes: ")
                insert_data_from_file(username, filename)

                input(
                    Style.NORMAL
                    + Fore.YELLOW
                    + "\n==> Press Enter to continue..."
                    + Style.RESET_ALL
                )
                print("", end="\n")
            case "2":
                exit_action_get = False

                print("", end="\n")

                while not exit_action_get:

                    print(
                        Style.DIM
                        + Fore.WHITE
                        + "(2) "
                        + Style.RESET_ALL
                        + "1 Total number of distinct variants"
                        + Style.DIM
                        + Fore.WHITE
                        + " (requires username)\n"
                        + "(2) "
                        + Style.RESET_ALL
                        + "2 List of all variants"
                        + Style.DIM
                        + Fore.WHITE
                        + " (requires username)\n"
                        + "(2) "
                        + Style.RESET_ALL
                        + "3 Go back\
                        \n==> Select one option "
                        + Style.DIM
                        + Fore.WHITE
                        + " (es: 1)"
                        + Style.RESET_ALL
                    )

                    action_get = input("==> ")

                    match (action_get):
                        case "1":
                            username = input("Enter minecraft username: ").lower()
                            total = count_variant_user(username)

                            if total is None:
                                print(
                                    Style.NORMAL
                                    + Fore.RED
                                    + "\n==> Something went wrong... Please check if user",
                                    username,
                                    "exists" + Style.RESET_ALL,
                                )

                            else:
                                print(
                                    Style.BRIGHT
                                    + Fore.WHITE
                                    + "\nWOW! "
                                    + username
                                    + " has discoverd "
                                    + str(total)
                                    + " of 2700 variants of tropical fishes!\n"
                                    + Style.RESET_ALL
                                )

                            input(
                                Style.NORMAL
                                + Fore.YELLOW
                                + "\n==> Press Enter to continue..."
                                + Style.RESET_ALL
                            )
                            print("", end="\n")

                        case "2":
                            username = input("Enter minecraft username: ")
                            username.lower()
                            np_variants, total = count_name_and_list_user(username)

                            if np_variants is None:
                                print(
                                    Style.NORMAL
                                    + Fore.RED
                                    + "\n==> Something went wrong... Please check if user"
                                    + username
                                    + "exists"
                                    + Style.RESET_ALL
                                )
                            else:
                                print(
                                    Style.BRIGHT
                                    + Fore.WHITE
                                    + "\nList of the "
                                    + str(count_variant_user(username))
                                    + " of 2700 variants of tropical fishes discovered by"
                                    + username
                                    + "\n"
                                    + Style.RESET_ALL
                                )

                                print(
                                    tabulate(
                                        np_variants,
                                        headers=["Variant", "Total"],
                                        tablefmt="grid",
                                    )
                                )

                            input(
                                Style.NORMAL
                                + Fore.YELLOW
                                + "\n==> Press Enter to continue..."
                                + Style.RESET_ALL
                            )
                            print("", end="\n")

                        case "3":
                            if (
                                input(
                                    "Are you sure?"
                                    + Style.DIM
                                    + Fore.WHITE
                                    + " [y/N]"
                                    + Style.RESET_ALL
                                )
                                == "y"
                            ):
                                exit_action_get = True

                            print("", end="\n")

                        case _:
                            print(
                                Style.BRIGHT
                                + Fore.YELLOW
                                + "*** You should select an option :( ***"
                                + Style.RESET_ALL,
                                end="\n\n",
                            )

                            time.sleep(0.7)
            case "3":
                if (
                    input(
                        "Are you sure?"
                        + Style.DIM
                        + Fore.WHITE
                        + " [y/N]"
                        + Style.RESET_ALL
                    )
                    == "y"
                ):
                    exit = True

                print("", end="\n")

            case _:
                print(
                    Style.BRIGHT
                    + Fore.YELLOW
                    + "*** You should select an option :( ***"
                    + Style.RESET_ALL,
                    end="\n\n",
                )

                time.sleep(0.7)

    print(Style.BRIGHT + Fore.YELLOW + "Thank you, bye!")
