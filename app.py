import sys
import time
import logging

from database.utility import insert_data_from_file
from database.utility import count_variant_user

logger = logging.getLogger(__name__)
logging.basicConfig(filename="app.log", encoding="utf-8", level=logging.ERROR)

# TODO: add compatibility with windows like systems

if __name__ == "__main__":
    
    exit = False
    while not exit :
        action = input("1 Insert new fishes from file\
                    \n2 Get some data \
                    \n3 Exit\
                    \n==> Select one option (es: 1)\
                    \n==> ")
        match (action):
            case ('1'):
               
                username = input("Enter minecraft username: ").lower()
                filename = input("Enter filename of tropical fishes: ")
                insert_data_from_file(username, filename)

                iinput("\n==> Press Enter to continue...\n")

            case ('2'):
                username = input("Enter minecraft username: ").lower()
                print(count_variant_user(username))

                input("\n==> Press Enter to continue...\n")

            case ('3'):
                if (input("Are you sure? [y/N]") == 'y'):
                    exit = True
                    
                print('', end='\n')

            case (_):
                print('*** You should select an option :( ***', end='\n\n')
                time.sleep(0.7)
                
    
    print('Thank you, bye!')