
from obj_parser.pages import HttpQuery, ElementPageChild, ElementPageGrandchild
import csv
import os
import re
import shutil # для удаления всех директиорий и файлов в каталоге


def delete_dir():
    """ """
    if os.path.exists('../library/'):
        shutil.rmtree('../library/')
        os.mkdir('../library/')

def open_csv(path):
    """ """
    with open(path, 'r', newline="") as file:
        reader = csv.reader(file, delimiter=';')
        data_parents = list(reader)
        for data_parent in data_parents: # [0:1]:  # можно задать родительскую страницу
            print(data_parent)
            yield data_parent

def create_parent_dir(path_lib, data_parent):
    """ """
    n = 1
    a = str(n)
    while True:
        path_parent = path_lib+'/'+a
        if os.path.exists(path_parent):
            n += 1
            a = str(n)
        else:
            os.mkdir(path_parent)
            with open(path_parent+'.txt', 'w', newline='') as file:
                file.write(data_parent[0])
            print(path_parent)
            break
    return path_parent

def query(data_parent):
    """ """
    short_url = data_parent[-1]
    url = base_url + short_url 
    print(url)
    query = HttpQuery(url, params=None)
    html_child = query.get_page_html()
    return html_child

def element_child_page(html_child):
    """ """
    elements = ElementPageChild(html_child)
    data_childs= elements.get_child_element() # если на дочерней странице url оканчивается на pdf, то игнорируем данную строку
    for data_child in data_childs:
        print(data_child)
        yield data_child

def create_child_dir(path_parent, data_child):
    """ """
    # title сделать обработку, Всевозможные варианты, можно получить с помощью parser_title.py 
    title = data_child[0][0:4]
    path_child = path_parent+'/'+title
    if os.path.exists(path_child):
        dir_child = os.mkdir(path_child+'_dop')
        with open(path_child+'_dop.txt', 'w') as file:
            file.write(data_child[0])
        return dir_child
    else:
        dir_child = os.mkdir(path_child)
        with open(path_child+'.txt', 'w') as file:
            file.write(data_child[0])
        return dir_child

# перенеси функцию в файл: parser_title.py 
def save_title_child(data_child, data_parent):
    """ """
    title_child = data_child[0]
    title_parent = data_parent[0]
    with open('title_child.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([title_child])

def query_one(data_child):
    """ """
    url = data_child[1]
    query = HttpQuery(url, params=None)
    html_grandchild = query.get_page_html()
    return html_grandchild

def element_grandchild_page(html_grandchild):
    """ """
    elements = ElementPageGrandchild(html_grandchild)
    data_grandchild = elements.get_grandchild_element()
    #print(data_grandchild)
    return data_grandchild

def create_grandchild_dir(dir_child, data_grandchild):
    """ """
    for row in data_grandchild:
        title =row[0]
        print(title)
        title_new = title.split(" ", 2)
        print("N"+title_new[1])
        # обработка_названий файлов

def save_data_grandchild(dir_child, data_grandchild, list_title_grandchild):
    """ """
    for row in data_grandchild:
        url = base_url+row[1]
        #print(url)
        title = row[0]
        print(title)
        title_new = title.split(" ", 2)
        print(title_new[1])
        # обработка_названий файлов
        pattern = r"№"
        if re.matсh(pattern, new_title):
            gold_title = new_title.replace(" ", )

        if title not in list_title_grandchild:
            list_title_grandchild.append(title)
            with open('title_grandchild.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([title])
        #query = HttpQuery(url, params=None)
        #query.get_content_page(dir_child)

if __name__ == "__main__":
    
    base_url = 'https://pravoslavnoe-duhovenstvo.ru/'
    path = '../parser_code/parent.csv'
    path_lib = '../library'
    list_title_grandchild = []
    
    delete_dir()
    data_parents = open_csv(path)
    for data_parent in data_parents:
        path_parent = create_parent_dir(path_lib, data_parent)
        html_child = query(data_parent)
        data_childs = element_child_page(html_child)
        
        for data_child in data_childs:
            # csv
            save_title_child(data_child, data_parent)
            path_child = create_child_dir(path_parent, data_child)

            html_grandchild = query_one(data_child)
            data_grandchild = element_grandchild_page(html_grandchild)
            path_grandchild = create_grandchild_dir(path_child, data_grandchild)
            
            # создание директорий
            ###path_parent = create_parent_dir(path_lib, data_parent)
            ###path_child = create_child_dir(path_parent, data_child)
            ###path_parent = create_parent_dir(path_lib, data_parent)

            #save_data_grandchild(data_child, data_grandchild, list_title_grandchild)
 
