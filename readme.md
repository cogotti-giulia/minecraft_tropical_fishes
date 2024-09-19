# Minecraft collect tropical fishes

Just a simple PostgreSQL database with python scripts to store minecraft tropical fishes with owner (i'm trying to collecting all of them! There are 2,700 combinations...)

## Instruction

1. create a postgreSQL database
2. create the file database.ini

```
[postgresql]
host=localhost
database=db_name
user=db_user
password=db_psw
```

3. run `python create_tables.py` to initialize the database tables
4. run `python init_db.py` to initialize the database with default types and names of tropical fishes

5. run `python insert.py "username" "filename"` to insert all of the tropical fishes in the "filename" file linked to the user "username"

**WARNING!**
The file must contain one fish for row. Type, base color and pattern color must be divided by '-'. For the 22 unique fish just write the name in a row. If a fish has the same color for base and patter, you can write it only one time.

To understand the name system have a look at [minecraft tropical fish](https://minecraft.fandom.com/wiki/Tropical_Fish)

```
pesce pagliaccio
pesce creta-marrone-giallo
pesce creta-arancione-rosso
triglia
pesce blocco-blu
pesce pappagallo pinna gialla
```
