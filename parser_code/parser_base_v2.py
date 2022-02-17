
from obj_parser.pages import HttpQuery, ElementPageParent, ElementPageChild, ElementPageGrandchild
from obj_parser.db import DbParser
import csv
import os
import re
import shutil # для удаления всех директиорий и файлов в каталоге
from itertools import chain

def query_parents_page(url):
    """ """

    params = {
        'search_type': 'fulltext',
        'query': 'епархиальные+ведомости',
        'page': 1,
        'area': 'name'
    }
    # страницы на которых есть искомые журналы: 1-4
    # начиная с 5 страницы выбираем в ручном режиме 
    n = 1
    parents_data = []
    while(n<=1):
        params['page'] = n
        query = HttpQuery(url, params)
        html = query.get_page_html()
        elements = ElementPageParent(html)
        data_parent = elements.get_parent_element()
        # соединяем списки/***переделать с intertools
        # parents_data = parents_data + data_parent   
        parents_data = list(chain(parents_data, data_parent))
        n += 1
    print(len(parents_data)) 
    return parents_data # [(title, url), (title_1, url_1),... ]  

def sort_parent_data(parents_data, BASE_URL):
    """ """
    #parents_data = [('rt', '/library/material/4966/')]
    parents_data_sort = [] 
    for data_parent in parents_data[0:1]:  # [0:4]:
        #ПЕРЕДЕЛАТЬ соединять с помощью join или f-строки
        url_child = BASE_URL  + data_parent[1]
        print(url_child)
        query = HttpQuery(url_child, params=None)
        html = query.get_page_html()
        elements = ElementPageChild(html)
        childs_url= elements.get_child_element_title()
        # print(childs_url) # [url, url_1, url_2, ...]
        sentence = " ".join(childs_url)
        # print(sentence)
        pattern = r"\.pdf|\.PDF"
        if re.search(pattern, sentence):
             path = 'title' + '/' + 'parent_yes_pdf.csv'
             with open(path, 'a', newline='') as file:
                writer = csv.writer(file, delimiter = ';')
                writer.writerow(data_parent)
        else:
            parents_data_sort.append(data_parent)
    print(len(parents_data_sort))
    return parents_data_sort

def delete_dir():
    """ """
    if os.path.exists('../library/'):
        shutil.rmtree('../library/')
        os.mkdir('../library/')

def create_parent_dir(PATH_LIB, parents_sort):
    """ """
    n = 1
    print(parents_sort)
    parent_for_db = []
    for data_parent in parents_sort:
        path_parent = PATH_LIB + '/' + str(n)
        title_parent = data_parent[0]
        url_parent = data_parent[1]
          # a = str(n)
        os.mkdir(path_parent)
        with open(path_parent+'.txt', 'w', newline='') as file:
            file.write(title_parent)
        db = (title_parent, url_parent, path_parent)
        parent_for_db.append(db) 
        n += 1
    print(parent_for_db)
    return parent_for_db

def save_db_parent(parent_for_db):
    """ """
    db = DbParser()
    db.insert_table_parent(parent_for_db)

# переделать
def get_data_child(BASE_URL, parent_for_sort):
    """ """
    n = 1
    for data_parent in parent_for_sort: # [(title, url, path), (), ()]
        title = data_parent[0]
        url = BASE_URL + data_parent[1]
        #
        db = DbParser()
        id_parent = db.select_table_parent(title)
        path_parent = data_parent[2] 
        #
        query = HttpQuery(url, params=None)
        html = query.get_page_html()
        #
        elements = ElementPageChild(html)
        data_childs = elements.get_child_element(id_parent, path_parent)
        n += 1
    return data_childs  # [(id_parent, title, url, path_child)]


def path_data_child(data_childs):
    """ """
    db = DbParser()
    db.insert_table_child(data_childs)
    for data_child in data_childs:
        path_child = data_child[3]
        os.mkdir(path_child)


def get_data_grandchild():
    """ """
    db = DbParser()
    data_childs = db.select_table_child()  # [(id, id_parent, title, path, url), (...)] 
    n = 1
    for data_child in data_childs:
       
        url = data_child[4]
        query = HttpQuery(url, params=None)
        html = query.get_grandchild_element()
        elements = ElementPageGrandchild()
        data_grandchild = elements.get_grandchild_element()         

        path_grandchild = data_child[3] + '/' + str(n)

        id_child = data_child[0]
        id_parent = data_child[1]

        data_drandchild = '' # [id_parent, id_child, title_grandchild, path_grandchild, url_grandchild]
        db = DbParser()
        db.insert_table_grandchild(data_grandchild)
        n += 1



if __name__ == "__main__":

    BASE_URL = 'https://pravoslavnoe-duhovenstvo.ru' 
    url = 'https://pravoslavnoe-duhovenstvo.ru/materials'
    PATH_LIB = '../library'

    parents_data = query_parents_page(url)
    parents_sort = sort_parent_data(parents_data, BASE_URL)
    delete_dir()
    parent_for_db = create_parent_dir(PATH_LIB, parents_sort)
    save_db_parent(parent_for_db)
    data_childs = get_data_child(BASE_URL, parent_for_db)
    path_data_child(data_childs)
