import os
from os.path import exists
import logging

from configparser import ConfigParser


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


# create config file getting data from user input
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
