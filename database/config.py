import os
from os.path import exists
import logging

from colorama import init, Style, Fore

from configparser import ConfigParser

from getpass import getpass

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename="database/config.log",
    encoding="utf-8",
    level=logging.DEBUG,
)


# load config from ini file
# if file not exists or if it's empty ask user to write config data
def load_config(section="postgresql"):
    
    ini_path = os.path.join("database/database.ini")

    file_exists = exists(ini_path)
    if not file_exists or os.stat(ini_path).st_size == 0:
        msg ="\n*** Oops the database configuration file doesn't exists, please follow the next instructions.***\n"
        print(Style.BRIGHT + Fore.RED + msg)

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


# create config file getting data from user input
def write_config_ini():

    msg = "If you're not sure about what are you really doing, please leave everything blank to use the default database configuration!\n"
    print(Style.DIM + Fore.YELLOW + msg)
  
    # get input data

    db_name = input("Insert database name\n==>" + Style.DIM + Fore.WHITE + "[minecraft] " + Style.RESET_ALL)
    db_name = "minecraft" if db_name == "" else db_name
    db_user = input("Insert database user\n==>" + Style.DIM + Fore.WHITE + "[postgres] " + Style.RESET_ALL)
    db_user = "postgres" if db_user == "" else db_user
    db_psw =  getpass("Insert database user password\n==>" + Style.DIM + Fore.WHITE + "[] " + Style.RESET_ALL)
    db_host = input("Insert database host\n==>" + Style.DIM + Fore.WHITE + "[localhost] " + Style.RESET_ALL)
    db_host = "localhost" if db_host == "" else db_host

    # write info in ini file
    ini_path = os.path.join("database/database.ini")

    with open(ini_path, "w") as file:
        line1 = "[postgresql]"
        line2 = "host=" + db_host
        line3 = "database=" + db_name
        line4 = "user=" + db_user
        line5 = "password=" + db_psw

        file.write("{}\n{}\n{}\n{}\n{}".format(line1, line2, line3, line4, line5))
