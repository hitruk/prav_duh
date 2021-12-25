

from obj_parser.pages import HttpQuery, ElementPageParent, ElementPageChild, ElementPageGrandchild

import csv
import os

def delete_csv():
    """ """
    filename = 'parent.csv'
    if os.path.exists(filename):
        print(filename, " - существует")
        os.remove(filename)
        print(filename, " - удален")
    else:
        print("Файл не существует")


def query(url, params):
    """ """
    query = HttpQuery(url, params)
    html = query.get_page_html()
    return html

def element_parent_page(html):
    """ """
    elements = ElementPageParent(html)
    # !!! возможно стоит написать сортировку !!!
    data_parent = elements.get_parent_element()
    print(data_parent)
    return data_parent

def save_data(data_parent):
    """ """
    with open('parent.csv', 'a', newline='') as file:
        writer= csv.writer(file, delimiter=';')
        for row in data_parent:
            writer.writerow(row)

if __name__ == '__main__':
    
    url = 'https://pravoslavnoe-duhovenstvo.ru/materials/'
    n = 1  # страницы на которых есть искомые журналы: 6
    params = {
        'search_type': 'fulltext',
        'query': 'епархиальные+ведомости',
        'page': 1,
        'area': 'name'
    }
    # delete parent.csv file
    delete_csv()
    # get parent page
    while(n<=6):
        print(n)
        params['page'] = n
        html = query(url, params)
        data_parent = element_parent_page(html)
        save_data(data_parent)
        n += 1
