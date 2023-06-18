from functions import *

while True:
    print("")
    print("-- Crossbreeding helper menu --")
    print("")
    print("1. Add clone.")
    print("2. Calculate crossbreed.")
    print("3. Change goal.")
    print("4. Help and information.")
    print("5. View currently stored clones.")
    print("")
    try:
        selection = int(input("Input menu selection (1-5): "))
        if selection >= 5 or selection < 1:
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
    elif selection == 4:
        print_help()
    elif selection == 5:
        view_current_list()
