import json
import itertools

weighting = {"red": 0.9, "green": 0.5}
gene_types = {"red": ["x", "w"], "green": ["y","g","h"]}
goal = {"w":0, "x":0, "y":4, "g":2, "h":0}
valid_genes = "wxghy"
stored_clones = []
save_route = "data.txt"

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def store_clone():
                
    global stored_clones
    global valid_genes
    while True:
        try:
            to_save = str(input("Enter clone genetics to store: "))
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

def save_to_file():
    global stored_clones
    with open(save_route, "w", encoding='utf-8') as f:
        json.dump(stored_clones, f, ensure_ascii=False, indent=4)

def read_file():
    global stored_clones
    with open(save_route, "r") as f:
        stored_clones = json.load(f)

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
        if should_print != False:
            print(clone_result)
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
    for clone_amount in range(2, 6):
        for combination in itertools.combinations(stored_clones, clone_amount):
            combinations_to_check.append(combination)
    ordered_goal = []
    for gene in goal:
        if goal[gene] > 0:
            for repetition in range(goal[gene]):
                ordered_goal.append(gene)

    ordered_goal.sort()
    achieved_goal_with = []
    number_of_failures = []
    print(f"Checking {len(combinations_to_check)} possible combinations...")

    for index, combination in enumerate(combinations_to_check):
        printProgressBar(index + 1, len(combinations_to_check), prefix = 'Checked combinations:', suffix = 'Complete', length=20, printEnd="\r")
        current_result, current_amount_of_failures = check_result(combination)
        current_result.sort()
        if current_result == ordered_goal:
            achieved_goal_with.append(combination)
            number_of_failures.append(current_amount_of_failures)
    
    print()
    print("Best result foound with clones:")
    min_failures = min(number_of_failures)
    index_of_min_failures = number_of_failures.index(min_failures)
    for clones in achieved_goal_with[index_of_min_failures]:
        print(clones)
    print("Cross-breeding result: ")
    print(check_result(achieved_goal_with[index_of_min_failures], True))