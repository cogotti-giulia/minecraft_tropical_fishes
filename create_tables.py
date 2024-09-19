import psycopg2
from config import load_config


#TODO: in tropical_fishes_variant table set as not null type and base and pattern color when added to the unique name fishes

def create_tables():
    """create tables in postgreSQL db"""
    commands = (
        """
            CREATE TABLE users (
                username VARCHAR(255) PRIMARY KEY
            )
        """,
        """
            CREATE TABLE colors (
                id SERIAL NOT NULL PRIMARY KEY,
                color VARCHAR(255) UNIQUE NOT NULL,
                color_eng VARCHAR(255) UNIQUE NOT NULL
            )
        """,
        """
            CREATE TABLE tropical_fishes_type (
                id SERIAL NOT NULL PRIMARY KEY,
                type VARCHAR(255) UNIQUE NOT NULL,
                type_eng VARCHAR(255) UNIQUE NOT NULL
            )
        """,
        """
            CREATE TABLE tropical_fishes_name (
                id SERIAL NOT NULL PRIMARY KEY,
                name VARCHAR(255) UNIQUE NOT NULL,
                name_eng VARCHAR(255) UNIQUE NOT NULL,
                type_id INTEGER,

                FOREIGN KEY (type_id) REFERENCES tropical_fishes_type (id)
            )
        """,
        """
            CREATE TABLE tropical_fishes_variants(
                id SERIAL NOT NULL PRIMARY KEY,
                is_unique BOOLEAN NOT NULL,

                name_id INTEGER UNIQUE,
                type_id INTEGER,

                base_color_id  INTEGER,
                pattern_color_id INTEGER,
            
                UNIQUE(type_id, base_color_id, pattern_color_id),

                FOREIGN KEY (base_color_id) REFERENCES colors (id),
                FOREIGN KEY (pattern_color_id) REFERENCES colors (id),
                FOREIGN KEY (type_id) REFERENCES tropical_fishes_type (id),
                FOREIGN KEY (name_id) REFERENCES tropical_fishes_name (id)
                
            )
        """,
        """
            CREATE TABLE owner_and_tropical_fishes(
                id SERIAL NOT NULL PRIMARY KEY,
                owner VARCHAR(255) NOT NULL,
                tropical_fish INTEGER NOT NULL,

                FOREIGN KEY (owner) REFERENCES users (username) ON DELETE CASCADE,
                FOREIGN KEY (tropical_fish) REFERENCES tropical_fishes_variants (id) ON DELETE CASCADE
            )
        """
    )
    
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the CREATE TABLE statement
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    create_tables()