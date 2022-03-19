from chardet.universaldetector import UniversalDetector
# cook_book = {
#   'Омлет': [
#     {'ingredient_name': 'Яйцо', 'quantity': 2, 'measure': 'шт.'},
#     {'ingredient_name': 'Молоко', 'quantity': 100, 'measure': 'мл'},
#     {'ingredient_name': 'Помидор', 'quantity': 2, 'measure': 'шт'}
#     ]
#   }
class RecieptClass():
    def __init__(self, description):
        self.description = description.rstrip()
        self.ingred = []

    def add_ingred(self, ingredient_name, quantity, measure):
        ingred = {}
        ingred['ingredient_name'] = ingredient_name
        ingred['quantity'] = int(quantity)
        ingred['measure'] = measure
        self.ingred.append(ingred)

    def __str__(self):
        res = f"{self.description}: {self.ingred}"
        return res

def get_shop_list_by_dishes(dishes, person_count, cook_book):
    dict_recipes = {}
    for d in dishes:
        i = 0
        for ingred in cook_book[d]:
             if dict_recipes.get(ingred['ingredient_name']) is None:
                 dict_recipes[ingred['ingredient_name']] = {}
                 dict_recipes[ingred['ingredient_name']]['measure'] = ingred['measure']
                 dict_recipes[ingred['ingredient_name']]['quantity'] = 0
             dict_recipes[ingred['ingredient_name']]['quantity'] = dict_recipes[ingred['ingredient_name']]['quantity'] + ingred['quantity'] * person_count
    return dict_recipes

def get_cook_book(file_name):
    # count = 0
    with open(file_name, mode='r', encoding='utf-8') as file:
        line_type = 'description'
        i = 0
        list_rec = []
        for line in file:
            match line_type:
                case 'description':
                    list_rec.append(RecieptClass(description=line))
                    line_type = 'count_ingred'
                case 'count_ingred':
                    count_ingred = int(line)
                    line_type = 'ingred'
                case 'ingred':
                    ingred = line.rstrip().split("| ");
                    list_rec[i].add_ingred(ingredient_name=ingred[0], quantity=ingred[1], measure=ingred[2])
                    count_ingred -= 1
                    if count_ingred == 0:
                        line_type = 'space'
                case 'space':
                    line_type = 'description'
                    i += 1
                case _:
                    print("Code not found")

        cook_book = {}
        for r in list_rec:
            cook_book[r.description] = r.ingred
        return cook_book

def sort_files(directory):
    import os
    from pathlib import Path
    import operator

    list_files = []
    files = os.listdir(directory)
    i = 0
    for file_name in files:

        d = {}
        path = Path(directory, file_name)
        d['file_name'] = file_name
        d['path'] = path
        with open(path, mode='r', encoding='utf-8') as file:
            d['count_rows'] = len(file.readlines())
        list_files.append(d)
        # print(d)
    print(list_files)

    list_files.sort(key=operator.itemgetter('count_rows'))
    print(list_files)
    return list_files

def merge_files(list_files):
    with open('new_file.txt', mode='w') as new_file:
        for f in list_files:
            new_file.write( str(f['file_name']) + '\n')
            new_file.write(str(f['count_rows']) + '\n')

            with open(f['path'], mode='r', encoding='utf-8') as file:
                for line in file:
                    new_file.write(line)
            new_file.write('\n')
            return "Создан файл new_file.txt"

print("Задача №1\n", get_cook_book("recipes.txt"))
print("Задача №2\n", get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 5, get_cook_book("recipes.txt")) )
print("Задача №3\n", merge_files(sort_files("sorted")));
