
import requests
from bs4 import BeautifulSoup
import re 
import csv

class HttpQuery:

    def __init__(self, url, params):
        self.url = url
        self.params = params
        self.req = requests.get(url=self.url, params=self.params)

    def get_page_html(self):
        """ """

        if self.req.status_code == 200:
            return self.req.text
        else:
            print('Server status code: ', self.req.status_code)
            return

    def get_content_page(self, dir_child):
        """ """
        with open(dir_child+'.pdf', "wb") as code:
            code.write(self.req.content)

class ElementPage:

    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(self.html, 'lxml')

class ElementPageParent(ElementPage):
    
    def get_parent_element(self):
        """ """
        abc = self.soup.find('div', class_='materials').find_all('li', class_='materials__item')
        data_parent = []
        for row in abc:
            try:
                title = row.find('h2').text.strip()
                # обработка POY, Переделать на более адекватный!!
                # если хватит времени
                pattern = r"//"
                if re.search(pattern, title):
                    title = ''
            except:
                title = ''
            try:
                url = row.find('a').get('href')
            except:
                url = ''
            if title != '' and url != '':
                data_parent.append((title, url))
        return data_parent


class ElementPageChild(ElementPage):
 
    def get_child_element(self):
        """ """
        abc = self.soup.find('div', class_='material__attachments').find_all('li')
        data = []
        for row in abc:
            try:
                title = row.find('span').text
            except:
                title = ''
            try:
                url = row.find('a').get('href')
            except:
                url = ''
            if title != '' and url != '':
                # если на дочерней странице вместо ссылок стоит PDF файл
                # в список data не добавляем
                pattern = r"\.pdf|\.PDF"
                if re.search(pattern, url):
                    pass       
                else:
                    data.append((title, url))
        return data

class ElementPageGrandchild(ElementPage):

    def get_grandchild_element(self):

        try:
            abc = self.soup.find('div', class_='material__wrapper_short_list').find_all('li')
        except:
            try:
                abc = self.soup.find('div', class_='material__wrapper').find_all('li')
            except AttributeError:
                with open("error.txt", "a") as file:
                    file.write("url address AttributeError: "+url_child)
                abc = []

        data_grandchild = []
        for row in abc:
            # переделать в одно r - строку
            try:
                title = row.find('span').text
            except:
                title = ''
            try:
                url = row.find('a').get('href')
            except:
                url = ''

            if title != '' and url != '':
                data_grandchild.append((title, url))

        return data_grandchild
