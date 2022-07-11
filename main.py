from functions import *

while True:
    print("")
    print("-- Crossbreeding helper menu --")
    print("")
    print("1. Add clone.")
    print("2. Calculate crossbreed.")
    print("3. Change goal.")
    print("4. Help and information.")
    print("")
    try:
        selection = int(input("Input menu selection (1-4): "))
        if selection > 4 or selection < 1:
            raise ValueError
        print("")
    except ValueError:
        print("Your input is invalid.")
        continue
    if selection == 1:
        store_clone()
    elif selection == 2:
        iterate_over_current_list()
    elif selection == 3:
        change_goal()
    else:
        print_help()