from functions import *

while True:
    print("")
    print("-- Crossbreeding helper menu --")
    print("")
    print("1. Add clone.")
    print("2. Calculate crossbreed.")
    print("3. Help and information.")
    print("")
    try:
        selection = int(input("Input menu selection (1-3): "))
        if selection > 3 or selection < 1:
            raise ValueError
        print("")
    except ValueError:
        print("Your input is invalid.")
        continue
    if selection == 1:
        store_clone()
    elif selection == 2:
        iterate_over_current_list()
    else:
        print_help()