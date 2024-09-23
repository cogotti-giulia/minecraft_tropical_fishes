from configparser import ConfigParser

import os


def config_ini(db_name='postgres', db_user='postgres', db_psw='', db_host = 'localhost',):
    ini_file = 'database/database.ini'
    
    config = configparser.ConfigParser()
    config.optionxform = str

    config.add_section('postgresql')
    config.set('postgresql', '; host is localhost by default', None)
    
    config['postgresql']['host'] = db_host
    config['postgresql']['database'] = db_name
    config['postgresql']['user'] = db_user
    config['postgresql']['password'] = db_psw


    with open(config_file, 'w') as cf:
        config.write(cf)

# TODO: generate file ini given parameter from console
def load_config(section="postgresql"):
    
    
    ini_path = os.path.join('database/database.ini')
    
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
