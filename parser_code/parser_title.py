
from obj_parser.pages import HttpQuery, ElementPageChild, ElementPageGrandchild
import csv
import os
import re

def create_dir_title(path_title):
    """ """
    if os.path.exists(path_title):
        print('file exist')
    else:
        os.mkdir(path_title)

def open_csv(path):
    """ """
    with open(path, 'r', newline="") as file:
        reader = csv.reader(file, delimiter=';')
        data_parents = list(reader)
        for data_parent in data_parents[0:1]:
            print(data_parent)
            yield data_parent 

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
    print(data_child)
    #data_child = data_child[0]
    #print(data_child)
    return data_child

def save_title_child(path_title, data_child):
    """ """
    title = data_child[0]
    path = path_title + '/' + 'child_title.csv'
    with open(path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([title])

def query_one(data_child):
    """ """
    url = data_child[1]
    print(url)
    query = HttpQuery(url, params=None)
    html_grandchild = query.get_page_html()
    return html_grandchild

def element_grandchild_page(html_grandchild):
    """ """
    elements = ElementPageGrandchild(html_grandchild)
    data_grandchild = elements.get_grandchild_element()
    #print(data_grandchild)
    return data_grandchild

def save_data_grandchild(data_grandchild, path_child):
    """ """
    for row in data_grandchild:
        url = base_url+row[1]
        print(url)
        title = row[0]
        #query = HttpQuery(url, params=None)
        #path_grandchild = path_child + '/' + new_title
        #query.get_content_page(path_grandchild)
    
if __name__ == "__main__":
    
    base_url = 'https://pravoslavnoe-duhovenstvo.ru/'
    path = '../parser_code/parent.csv'
    path_lib = '../library/'
    path_title = 'title' 
    
    create_dir_title(path_title)
    data_parents = open_csv(path)
    for data_parent in data_parents:
        html_child = query(data_parent)
        data_childs = element_child_page(html_child)
        for data_child in data_childs:
            save_title_child(path_title, data_child)
    #html_grandchild = query_one(data_child)
    #data_grandchild = element_grandchild_page(html_grandchild)

