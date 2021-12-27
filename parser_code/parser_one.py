
from obj_parser.pages import HttpQuery, ElementPageChild, ElementPageGrandchild
import csv
import os

# данные находящиеся на странице родителя, а так же адреса на этой страницы, будут называться родительскими!!!

import shutil
def delete_dir():
    if os.path.exists('../library/'):
        shutil.rmtree('../library/')
        os.mkdir('../library/')

def open_csv(path):
    """ """
    with open(path, 'r', newline="") as file:
        reader = csv.reader(file, delimiter=';')
        data_parent = list(reader)[0]
        print(data_parent)
    return data_parent
         #for row in reader:
         #   data_parent = row
         #   yield data_parent 

# del - удалить в случае провала
def create_parent_dir(data_parent):
    """ """
    path = '../library/'
    n = 1
    a = str(n)
    while True:
        new_path = path+a
        if os.path.exists(new_path):
            n += 1 
            a = str(n)
        else:
            os.mkdir(new_path)
            with open(new_path+'.txt', 'w', newline='') as file:
                file.write(data_parent[0])
            print(new_path)
            break
    return new_path

def query(data_parent):
    """ """
    short_url = data_parent[1]
    url = base_url + short_url 
    query = HttpQuery(url, params=None)
    html_child = query.get_page_html()
    return html_child

def element_child_page(html_child):
    """ """
    elements = ElementPageChild(html_child)
    data_child = elements.get_child_element()
    # print(data_child)
    return data_child
# ПРОДОЛЖИТЬ С ДАННОЙ ФУНКЦИИ!!!
def create_child_dir(new_path):
    """ """
    pass

def query_one(data_child):
    """ """
    print(data_child[0][1])
    url = data_child[0][1]
    query = HttpQuery(url, params=None)
    html_grandchild = query.get_page_html()
    return html_grandchild

def element_grandchild_page(html_grandchild):
    """ """
    elements = ElementPageGrandchild(html_grandchild)
    data_grandchild = elements.get_grandchild_element()
    print(data_grandchild)
    return data_grandchild

if __name__ == "__main__":
    
    base_url = 'https://pravoslavnoe-duhovenstvo.ru/'
    path = '../parser_code/parent.csv'
    
    delete_dir()
    data_parent = open_csv(path)
    create_parent_dir(data_parent)
    html_child = query(data_parent)
    data_child = element_child_page(html_child)
    html_grandchild = query_one(data_child)
    element_grandchild_page(html_grandchild)
    

    # del 
    #delete_dir()
    #for data_parent in open_csv(path):
    #    create_parent_dir(data_parent)

