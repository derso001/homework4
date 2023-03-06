import re
from command import OPERATIONS
from input_error import input_error


#add Bob +380665597662

@input_error
def main():
    while True:

        command = input("command: ").lower().strip()
        command = re.sub("[^A-Za-z0-9+_ ]", "", command)
        pars_str = command.split(" ")

        if command in OPERATIONS["exit"]:
            break

        else:
            OPERATIONS[pars_str[0]](*pars_str)


main()