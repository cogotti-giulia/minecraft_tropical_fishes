# Minecraft collect tropical fishes

Just a simple PostgreSQL database with python scripts to store minecraft tropical fishes with owner (i'm trying to collecting all of them! There are 2,700 combinations...)

## Instruction

1. create a postgreSQL database
2. create the file database.ini inside the database folder

```
[postgresql]
host=localhost
database=db_name
user=db_user
password=db_psw
```

3. run `make build` in order to:
    - install all the necessary python packages in a virtual environment (you can see them in _requirements.txt_)
    - create the database 
    - initialize the database with default values (colors, types and names)

4. run `make run` to run the program. It will ask you to insert the **minecraft** username and the **filename** in which are stored the fishes names/types, then it'll insert all the data into the database.

**WARNING!**
The _file_ must contain one fish for row. Type, base color and pattern color must be divided by ','. For the 22 unique fish (the real life species) just write the name in a row. If a fish has the same color for base and patter, you can write it only one time.

To understand the name system have a look at [minecraft tropical fish](https://minecraft.fandom.com/wiki/Tropical_Fish)

```
clownfish
clayfish,brown,yellow
clayfish,orange,red
goatfish
blockfish,blue
yellowtail parrotfish
```

After insertion into the database the file will be cleaned to avoid inserting the same rows again and again. Except when there is something bad written (like grammar errors), those lines stays there to be fixed by the user!