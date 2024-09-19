from configparser import ConfigParser
import os

# TODO: generate file ini given parameter from console
def load_config(folder = None, section="postgresql"):

    if folder != None:
        ini_path = os.path.join(os.getcwd() + folder,'database.ini')
    else:
        ini_path = os.path.join(os.getcwd(),'database.ini')

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


if __name__ == "__main__":
    config = load_config()
    print(config)
