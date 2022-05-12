import requests
from bs4 import BeautifulSoup
import csv
import urllib.request

#extract all book informations as list of string
def extract_product_information(elements, choice):
    result = []
    if choice == 1:
        for image in elements:
            result.append(image['src'])
    elif choice == 2:
        for element in elements:
            result.append(element.string)
    return result

#convert "review_rating" from string to number
def convert_rating(elements):
    if elements == "One":
        elements = [1]
    elif elements == "Two":
        elements = [2]
    elif elements == "Three":
        elements = [3]
    elif elements == "Four":
        elements = [4]
    elif elements == "Five":
        elements = [5]
    else:
        elements = [0]
    return elements

def create_csv_column(file_name):
    column = ["title", "universal_product_code", "price_including_tax", "price_excluding_tax", "number_available",
                "product_description", "category", "image_url", "review_rating"]
    with open(file_name, 'w', encoding="utf-8") as file_csv:
        writer = csv.writer(file_csv, delimiter=',')
        writer.writerow(column)

def download_img(image_link, title_image):
    for i in range(len(image_link)):
        image_url = image_link[i]
        file_path = 'images/'
        char_to_replace = {':': '',
                           '\x5C': '',
                           '/': '',
                           '*': '',
                           '?': '',
                           '"': '',
                           '<': '',
                           '>': '',
                           '|': ''}
        image_name = title_image[0].translate(str.maketrans(char_to_replace))
        file_name = 'image-{}.jpg'.format(image_name)
        full_path = '{}{}'.format(file_path, file_name)
        urllib.request.urlretrieve(image_url, full_path)





#load all data inside "data.csv" file
def load_data(file_name,
              title,
              UPC,
              including,
              excluding,
              available,
              description,
              category,
              img,
              rating):
    #print(file_name)
    with open(file_name, 'a', encoding="utf-8") as file_csv:
        writer = csv.writer(file_csv, delimiter=',')
        for titles, upc, priceI, priceE, stock, text, cate, url, note in zip(title,
                                                                                UPC,
                                                                                including,
                                                                                excluding,
                                                                                available,
                                                                                description,
                                                                                category,
                                                                                img,
                                                                                rating):
            writer.writerow([titles, upc, priceI, priceE, stock, text, cate, url, note])

def book_page_focus(book_url, category_from_list):
    #link of the page
    for i in range(len(book_url)):
        url = book_url[i]
        #print(url)
        response = requests.get(url)
        page = response.content

        soup = BeautifulSoup(page, "html.parser")
        #get all informations from book
        book_product = soup.select_one("tr:nth-child(1) > td")
        book_title = soup.find_all("h1")
        book_price_including_tax = soup.select_one("tr:nth-child(4) > td")
        book_price_excluding_tax = soup.select_one("tr:nth-child(3) > td")
        book_number_available = soup.select_one("tr:nth-child(6) > td")
        book_description = soup.select_one("article > p")
        book_category = soup.select_one("li:nth-child(3) > a")
        book_img = soup.find_all('img')
        book_rating = soup.select_one('article > div.row > div.col-sm-6.product_main > p.star-rating')
        review_rating = book_rating["class"][1]



        universal_product_code = extract_product_information(book_product, 2)
        title = extract_product_information(book_title, 2)
        price_including_tax = extract_product_information(book_price_including_tax, 2)
        price_excluding_tax = extract_product_information(book_price_excluding_tax, 2)
        number_available = extract_product_information(book_number_available, 2)
        product_description = extract_product_information(book_description, 2)
        category = extract_product_information(book_category, 2)
        image_url = extract_product_information(book_img, 1)
        review_rating = convert_rating(review_rating)

        #add domain link to "image_url"
        image_url = image_url[0]
        image_url = image_url.replace('../..', 'http://books.toscrape.com')
        image_url = [image_url]

        #remove text from "number_available" and keep number
        number_available = number_available[0].text
        number_available = number_available.replace('In stock (', '')
        number_available = number_available.replace('available)', '')
        number_available = int(number_available)
        number_available = [number_available]

        download_img(image_url, title)
        load_data(category_from_list, title, universal_product_code, price_including_tax, price_excluding_tax, number_available, product_description, category, image_url, review_rating)

def get_category_url(category):

    category_url = []
    for i in range(len(category)):
        current_category = category[i]
        category_url_page = []
        url = 'http://books.toscrape.com/catalogue/category/books/' + current_category +'/index.html'

        response = requests.get(url)
        page = response.content

        soup = BeautifulSoup(page, 'html.parser')
        next = soup.select('ul.pager')


        if next == []:
            category_url.append(['http://books.toscrape.com/catalogue/category/books/' + current_category + '/index.html'])
        else:
            number_of_page = soup.find('li', class_='current')
            number_of_page = number_of_page.text
            number_of_page = number_of_page.replace('Page 1 of', '')
            number_of_page = int(number_of_page)
            for i in range(1, number_of_page+1):
                index_page = str(i)
                category_url_page.append('http://books.toscrape.com/catalogue/category/books/' + current_category + '/page-' + index_page + '.html')
            category_url.append(category_url_page)
    return category_url


def get_all_books_from_category(category, list_category):
    for i in range(len(category)):
        url = category[i]
        #print(i)
        create_csv_column(list_category[i])
        category_from_list = list_category[i]

        links = []
        for o in range(len(url)):
            page_url = url[o]
            #print(page_url)
            response = requests.get(page_url)
            page = response.content

            soup = BeautifulSoup(page, 'html.parser')

            books_url = soup.select('article.product_pod')

            for book in books_url:
                link = book.find('a')["href"]
                link = link.replace('../../..', 'http://books.toscrape.com/catalogue')
                links.append(link)
            #print(links)
            book_page_focus(links, category_from_list)



def get_category_list():
    url = "http://books.toscrape.com/catalogue/category/books_1/index.html"
    response = requests.get(url)
    page = response.content

    soup = BeautifulSoup(page, "html.parser")

    list_category = []
    category_path = soup.select('ul > li > ul > li')

    for category in category_path:
        link_category = category.find('a')['href']
        link_category = link_category.replace('../books/', '')
        link_category = link_category.replace('/index.html', '')
        list_category.append(link_category)
    return list_category
'''
def get_a_book_link(list_from_all_book):
    #print(list_from_all_book)
    for i in range(len(list_from_all_book)):
        books_from_category = list_from_all_book
        #print(books_from_category)
        book_page_focus(books_from_category)
'''



#choice = input("quelle catégorie voulez vous récupérer?:\n")

category_list = get_category_list()
category_url = get_category_url(category_list)
get_all_books_from_category(category_url, category_list)



