############################ USER ############################
# search user by username
Q_SEARCH_USER = "SELECT * FROM users WHERE username = %s"
# insert new user
Q_INSERT_USER = "INSERT INTO users(username) VALUES(%s)"


###################### TROPICAL FISH NAME ####################

Q_INSERT_NAME = "INSERT INTO tropical_fish_name(name, name_eng)\
                    VALUES(%s, %s)\
                        RETURNING *"

# get id from table tropical fish name given the name
Q_GET_ID_NAME = "SELECT id FROM tropical_fish_name\
                    WHERE (name = %s OR name_eng = %s)"


###################### TROPICAL FISH TYPE ####################

Q_INSERT_TYPE = "INSERT INTO tropical_fish_type(type, type_eng)\
                    VALUES(%s, %s)\
                        RETURNING *"

# get id from table tropical fish type given the type
Q_GET_ID_TYPE = "SELECT id FROM tropical_fish_type\
                    WHERE (type = %s OR type_eng = %s)"


#################### TROPICAL FISH VARIANT ####################

Q_GET_ID_VARIANT_UNIQUE22 = "SELECT id FROM tropical_fish_variant\
                                WHERE (is_unique AND name_id = %s)"


Q_GET_ID_VARIANT = "SELECT id FROM tropical_fish_variant\
                        WHERE not is_unique AND\
                        (type_id = %s AND base_color_id = %s AND pattern_color_id = %s)"

Q_INSERT_VARIANT_UNIQUE22 = "INSERT INTO tropical_fish_variant(is_unique, name_id)\
                                VALUES(%s, %s)\
                                    RETURNING id"


Q_INSERT_VARIANT = "INSERT INTO tropical_fish_variant(is_unique, type_id, base_color_id, pattern_color_id)\
                        VALUES(%s, %s, %s, %s)\
                            RETURNING id"


###################### OWNER AND FISH #########################

# reference to the owner of the fish

Q_INSERT_FISH_OWNER = "INSERT INTO owner_and_tropical_fish(owner, tropical_fish)\
                        VALUES(%s, %s)\
                            RETURNING id"


############################ COLOR ############################

Q_INSERT_COLOR = "INSERT INTO color(color, color_eng)\
                    VALUES(%s, %s)"

# get id from table color given the color
Q_GET_ID_COLOR = "SELECT id FROM color\
                    WHERE (color = %s OR color_eng = %s)"
