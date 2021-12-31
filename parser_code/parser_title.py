
from obj_parser.pages import HttpQuery, ElementPageChild, ElementPageGrandchild
import csv
import os
import re

# данные находящиеся на странице родителя, а так же адреса на этой страницы, будут называться родительскими!!!
import shutil
def delete_dir():
    """ """
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
    #print(data_child)
    data_child = data_child[0]
    print(data_child)
    return data_child

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

def create_path_parent(path_lib, data_parent):
    """ """
    n = 1
    a = str(n)
    while True:
        path_parent = path_lib+a
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

def create_child_dir(path_parent, data_child):
    """ """
    #n = 1
    #for row in data_child:
    #    title = row[0][0:4]
    #    print(title)
    #    os.mkdir(new_path+'/'+title)
    #    with open(new_path+'/'+title+'.txt', 'w') as file:
    #        file.write(row[0])
    #result = os.listdir(new_path)
    #print(result)
    title = data_child[0][0:4]
    path_child = path_parent+'/'+title
    os.mkdir(path_child)
    with open(path_parent+'/'+title+'.txt', 'w') as file:
            file.write(data_child[0])   
    print(path_child)
    return path_child


def save_data_grandchild(data_grandchild, path_child):
    """ """
    for row in data_grandchild:
        url = base_url+row[1]
        print(url)
        title = row[0]
        pattern = r"№"
        if re.match(pattern, title):
            pattern = r"№ "
            new_title = re.sub(pattern, 'N', title)
            print(new_title
        else:

        #query = HttpQuery(url, params=None)
        #path_grandchild = path_child + '/' + new_title
        #query.get_content_page(path_grandchild)
    
    
if __name__ == "__main__":
    
    base_url = 'https://pravoslavnoe-duhovenstvo.ru/'
    path = '../parser_code/parent.csv'
    path_lib = '../library/'   
    
    delete_dir()
    data_parent = open_csv(path)
    html_child = query(data_parent)
    data_child = element_child_page(html_child)
    html_grandchild = query_one(data_child)
    data_grandchild = element_grandchild_page(html_grandchild)
    path_parent = create_path_parent(path_lib, data_parent)
    path_child = create_child_dir(path_parent, data_child)
    save_data_grandchild(data_grandchild, path_child)


