############################ USER ############################

Q_INSERT_USER = "INSERT INTO users(username) VALUES(%s)"
Q_SEARCH_USER = "SELECT * FROM users WHERE username = %s"


###################### TROPICAL FISH NAME ####################

Q_INSERT_NAME = "INSERT INTO tropical_fish_name(name, name_eng)\
                    VALUES(%s, %s)\
                        RETURNING *"
Q_GET_ID_NAME = "SELECT id FROM tropical_fish_name\
                    WHERE (name = %s OR name_eng = %s)"


###################### TROPICAL FISH TYPE ####################

Q_INSERT_TYPE = "INSERT INTO tropical_fish_type(type, type_eng)\
                    VALUES(%s, %s)\
                        RETURNING *"
Q_GET_ID_TYPE = "SELECT id FROM tropical_fish_type\
                    WHERE (type = %s OR type_eng = %s)"


#################### TROPICAL FISH VARIANT ####################

Q_INSERT_VARIANT_UNIQUE22 = "INSERT INTO tropical_fish_variant(is_unique, name_id)\
                                VALUES(%s, %s)\
                                    RETURNING id"
Q_GET_ID_VARIANT_UNIQUE22 = "SELECT id FROM tropical_fish_variant\
                                WHERE (is_unique AND name_id = %s)"

Q_INSERT_VARIANT = "INSERT INTO tropical_fish_variant(is_unique, type_id, base_color_id, pattern_color_id)\
                        VALUES(%s, %s, %s, %s)\
                            RETURNING id"
Q_GET_ID_VARIANT = "SELECT id FROM tropical_fish_variant\
                        WHERE not is_unique AND\
                        (type_id = %s AND base_color_id = %s AND pattern_color_id = %s)"


###################### OWNER AND FISH #########################

Q_INSERT_FISH_OWNER = "INSERT INTO owner_and_tropical_fish(owner, tropical_fish)\
                        VALUES(%s, %s)\
                            RETURNING id"


############################ COLOR ############################

Q_INSERT_COLOR = "INSERT INTO color(color, color_eng)\
                    VALUES(%s, %s)"
Q_GET_ID_COLOR = "SELECT id FROM color\
                    WHERE (color = %s OR color_eng = %s)"


########################### GET SOME DATA ######################
# get total number of tp fishes of a specific user
Q_COUNT_VARIANT_USER = "select count(*)\
                        from tropical_fish_variant tfv join owner_and_tropical_fish oatf\
                            on tfv.id = oatf.tropical_fish\
		                where oatf.owner = %s"

# TODO: finish queries
# contare il numero di pesci di un certo tipo dato il tipo e il giocatore
# contare il numero di pesci di ogni tipo
# visualizzare anche quali pesci sono!
