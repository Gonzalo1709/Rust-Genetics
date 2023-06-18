import json
import itertools
import os

weighting = {"red": 0.9, "green": 0.5}
gene_types = {"red": ["x", "w"], "green": ["y","g","h"]}
valid_genes = "wxghy"
stored_clones = []
save_route = "data.txt"
goal_file = "goal.txt"

if not os.path.exists(save_route):
	file = open(save_route, 'w')
	file.close
if not os.path.exists(goal_file):
    file = open(goal_file, 'w')
    file.close
    goal = {"w":0, "x":0, "y":4, "g":2, "h":0}
    with open(goal_file, "w", encoding='utf-8') as f:
        json.dump(goal, f, ensure_ascii=False, indent=4)

goal = {}
with open(goal_file, "r") as f:
    goal = json.load(f)

def change_goal():
    global goal
    ordered_goal = []
    for gene in goal:
        if goal[gene] > 0:
            for repetition in range(goal[gene]):
                ordered_goal.append(gene)
    ordered_goal.sort()
    print(f"Current goal is {ordered_goal}")
    global valid_genes
    while True:
        try:
            new_goal = input("Input new goal in the same format (6 genes, order doens't matter ie. GGYYYY): ")
            new_goal = new_goal.lower()
            clone = []
            for gene in new_goal:
                if gene not in valid_genes:
                    raise ValueError
                else:
                    clone.append(gene)
            if len(clone) != 6:
                raise ValueError
            else:
                break
        except ValueError:
            print("Invalid clone format.")
            print('Input goal as 6 letters ie. GGYYYY')
    new_goal = {"w":0, "x":0, "y":0, "g":0, "h":0}
    for gene in clone:
        new_goal[gene] += 1
    with open(goal_file, "w") as f:
        json.dump(new_goal, f, ensure_ascii=False, indent=4)
    goal = new_goal

def print_help():
    print("This is a tool meant to store your available Rust plant genes and attempt to get an ideal clone.")
    print("")
    print("The ideal clone is by default any clone with 4 y's and 2 g's. Order doesn't matter.")
    print("")
    print("This currently works with any crop as genetics work the same for them all.")
    print("To get more genes just plant seeds from the desired crop and when it grows hold e on it and there should be an option to clone the plant.")
    print("")
    print("It is recommended only to clone plants with 4 or more green clones.")
    print("Once you've gotten around 10 clones you can start calculating the crossbreed and hopefully get a desired clone.")
    print("")
    print("Sometimes you'll get a 50/50 chance to get a specific gene, you'll have to crossbreed over and over again until you get the desired gene.")
    print("This program attempts to give you the combination of clones with the least possible 50/50's.")

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def read_file():
    global stored_clones
    try:
        with open(save_route, "r") as f:
            stored_clones = json.load(f)
    except json.decoder.JSONDecodeError:
        print("Your save file is empty!")

def save_to_file():
    global stored_clones
    with open(save_route, "w", encoding='utf-8') as f:
        json.dump(stored_clones, f, ensure_ascii=False, indent=4)

def store_clone():
    global stored_clones
    global valid_genes
    print('Input clone as 6 letters ie. GGYYYY')
    while True:
        try:
            to_save = str(input("Enter clone genetics to store: "))
            to_save = to_save.lower()
            clone = []
            for gene in to_save:
                if gene not in valid_genes:
                    raise ValueError
                else:
                    clone.append(gene)
            if len(clone) != 6:
                raise ValueError
            else:
                break
        except ValueError:
            print("Invalid clone format.")
            print('Input clone as 6 letters ie. GGYYYY')
    stored_clones.append(clone)
    save_to_file()

def check_result(clones_to_check, should_print = False):

    possible_failures = 0
    def choose_gene(clone_to_choose):
        possible_failures_inside = 0
        global goal
        clone_result = clone_to_choose
        amounts = base_dict.copy()
        priority = ["y", "g", "h", "x", "w"]
        for index, gene in enumerate(clone_to_choose):
            if "/" not in gene:
                amounts[gene] += 1
        for index, gene in enumerate(clone_to_choose):
            if "/" in gene:
                genes_to_choose = gene.split("/")
                for item in range(5):
                    if priority[item] in genes_to_choose and amounts[priority[item]] < goal[priority[item]]:
                        selected_gene = priority[item]
                        amounts[priority[item]] += 1
                        clone_result[index] = selected_gene
                        if should_print != False:
                            print(f"You will have to attempt the cross breed until gene {index+1} comes out as {priority[item]}.")
                        possible_failures_inside += 1
                        break
        missing_result = False
        for index, gene in enumerate(clone_to_choose):
            if "/" in gene:
                missing_result = True
        if missing_result == True:
            for index, gene in enumerate(clone_to_choose):
                if "/" in gene:
                    genes_to_choose = gene.split("/")
                    for item in range(5):
                        if priority[item] in genes_to_choose:
                            selected_gene = priority[item]
                            amounts[priority[item]] += 1
                            clone_result[index] = selected_gene
                            if should_print != False:
                                print(f"You will have to attempt the cross breed until gene {index+1} comes out as {priority[item]}.")
                            possible_failures_inside += 1
                            break
        return(clone_result, possible_failures_inside)

    global weighting
    global gene_types
    base_dict = {"w": 0, "x": 0, "y": 0, "g": 0, "h": 0}
    gene_sum = {
        0: base_dict.copy(),
        1: base_dict.copy(),
        2: base_dict.copy(),
        3: base_dict.copy(),
        4: base_dict.copy(),
        5: base_dict.copy()
        }
    for clone in clones_to_check:
        for index, gene in enumerate(clone):
            for type in gene_types:
                current_type = ""
                current_weight = 0
                if gene in gene_types[type]:
                    current_type = type
                if current_type != "":
                    current_weight = weighting[current_type]
                    break
            gene_sum[index][f"{gene}"] += current_weight
    
    result = []
    need_to_choose = False
    for gene_to_append in range(6):
        all_weights = list(gene_sum[gene_to_append].values())
        max_weight = max(gene_sum[gene_to_append].values())
        all_weights.remove(max_weight)
        multiple_max = False
        if max_weight == max(all_weights):
            multiple_max = True
        if multiple_max == False:
            result.append(max(gene_sum[gene_to_append], key=gene_sum[gene_to_append].get))
        else:
            need_to_choose = True
            to_add = ""
            highest_genes = [k for k, v in gene_sum[gene_to_append].items() if v == max_weight]
            for possbile_gene in highest_genes:
                to_add += f"{possbile_gene}/"
            to_add = to_add[:-1]
            result.append(to_add)
    if need_to_choose == True:
        result, possible_failures = choose_gene(result)
    if should_print == False:
        return(result, possible_failures)
    else:
        return(result)

#print(check_result([["g", "w", "w", "y", "h", "h"], ["y", "w", "g", "y", "h", "y"], ["h", "y", "g", "x", "g", "x"]]))
# should return ['y/g/h', 'w', 'g', 'y', 'h', 'x']
# with priority check result is ['y', 'w', 'g', 'y', 'h', 'x']

def iterate_over_current_list():
    global goal
    read_file()
    combinations_to_check = []
    for clone_amount in range(1, 6):
        for combination in itertools.combinations(stored_clones, clone_amount):
            combinations_to_check.append(combination)
    if len(combinations_to_check) == 0:
        print("You can't calculate the results of an empty save file.")
        return
    ordered_goal = []
    for gene in goal:
        if goal[gene] > 0:
            for repetition in range(goal[gene]):
                ordered_goal.append(gene)
    ordered_goal.sort()
    achieved_goal_with = []
    number_of_failures = []
    good_combinations = []
    print(f"Checking {len(combinations_to_check)} possible combinations...")
    for index, combination in enumerate(combinations_to_check):
        printProgressBar(index + 1, len(combinations_to_check), prefix = 'Progress:', suffix = 'Complete', length=20, printEnd="\r")
        current_result, current_amount_of_failures = check_result(combination)
        current_result.sort()
        if current_result == ordered_goal:
            achieved_goal_with.append(combination)
            number_of_failures.append(current_amount_of_failures)
        else:
            score = 0
            for gene in current_result:
                if gene in gene_types["green"]:
                    score += 1
            if score > 5:
                good_combinations.append(combination)
        if  current_result == ordered_goal and current_amount_of_failures == 0:
            print("")
            print("Ideal clone found early.")
            break
    print()
    if len(achieved_goal_with) == 0:
        print("Couldn't achieve an ideal clone with current stored clones. Keep storing more.")
        if len(good_combinations) > 0:
            print("However, these combinations are good enough to be crossbred and stored: ")
            for combination in good_combinations:
                print(combination, end=" => ")
                print(check_result(combination, should_print=True))
        return
    print("Best results found with clones:")
    min_failures = min(number_of_failures)
    index_of_min_failures = number_of_failures.index(min_failures)
    for clones in achieved_goal_with[index_of_min_failures]:
        print(clones)
    print("Cross-breeding result: ")
    print(check_result(achieved_goal_with[index_of_min_failures], should_print=True))

def view_current_list():
    read_file()
    print("Current stored clones: ")
    for clone in stored_clones:
        print(clone)