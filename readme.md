# Minecraft collect tropical fishes

Just a simple PostgreSQL database with python scripts to store minecraft tropical fishes with minecraft owner (i'm trying to collecting all of them! There are 2,700 combinations...)

## Instruction

1. install postgreSQL [(download here)](https://www.postgresql.org/download/)

2. run `make build` in order to:
    - install all the necessary python packages in a virtual environment (you can see them in _requirements.txt_)
    - clean log files

3. run `make run` to run the program. It will ask you to select an option, please do it (otherwise why are you using it??).

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