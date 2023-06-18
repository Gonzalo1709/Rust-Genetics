from functions import *

class Menu:
    def __init__(self, title, options):
        self.title = title
        self.options = options
        self.selection = None

    def show(self):
        print("")
        print(self.title)
        print("")
        for i, option in enumerate(self.options):
            print(f"{i + 1}. {option}")
        print("")
        while True:
            try:
                self.selection = int(input("Input menu selection (1-4): "))
                if self.selection > len(self.options) or self.selection < 1:
                    raise ValueError
                print("")
                break
            except ValueError:
                print("Your input is invalid.")
                continue

    def get_selection(self):
        return self.selection
    
# create gui for menu
menu = Menu("-- Crossbreeding helper menu --", ["Add clone", "Calculate crossbreed", "Change goal", "Help and information"])

# main loop

while True:
    menu.show()
    selection = menu.get_selection()
    if selection == 1:
        store_clone()
    elif selection == 2:
        iterate_over_current_list()
    elif selection == 3:
        change_goal()
    else:
        print_help()