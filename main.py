import requests
from bs4 import BeautifulSoup
import csv

#extract all book informations as list of string
def extract_product_information(elements, choice):
    result = []
    if choice == 1:
        for image in elements:
            result.append(image['src'])
    elif choice == 2:
        for element in elements:
            result.append(element.string)
    elif choice == 3:
        for url in elements:
            result.append(url['href'])
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

def book_page_focus(book_url):
    #link of the page

    url = book_url
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
    #print(number_available)

    load_data("data.csv", title, universal_product_code, price_including_tax, price_excluding_tax, number_available, product_description, category, image_url, review_rating)

def get_category_url(category):
    url = 'http://books.toscrape.com/catalogue/category/books/' + category +'/index.html'
    response = requests.get(url)
    page = response.content

    soup = BeautifulSoup(page, 'html.parser')
    next = soup.select('ul.pager')
    category_url = []

    if next == []:
        category_url[0] = 'http://books.toscrape.com/catalogue/category/books/' + category + '/index.html'
    else:
        number_of_page = soup.find('li', class_='current')
        number_of_page = number_of_page.text
        number_of_page = number_of_page.replace('Page 1 of', '')
        number_of_page = int(number_of_page)
        #category_url = 'http://books.toscrape.com/catalogue/category/books/' + category + '/page-1.html'
        for i in range(1, number_of_page+1):
            index_page = str(i)
            category_url.append('http://books.toscrape.com/catalogue/category/books/' + category + '/page-' + index_page + '.html')
    return category_url





def get_all_books_from_category(category):

    links = []
    for i in range(len(category)):
        url = category[i]

        response = requests.get(url)
        page = response.content

        soup = BeautifulSoup(page, 'html.parser')



        books_url = soup.select('article.product_pod')

        for book in books_url:
            link = book.find('a')["href"]
            link = link.replace('../../..', 'http://books.toscrape.com/catalogue')
            links.append(link)
    return links


def get_category_dict(name_category):
    url = "http://books.toscrape.com/catalogue/category/books_1/index.html"
    response = requests.get(url)
    page = response.content

    soup = BeautifulSoup(page, "html.parser")

    dict_category = {}
    category_path = soup.select('ul > li > ul > li')
    i = 2
    for category in category_path:
        link_category = category.find('a')['href']
        link_category = link_category.replace('../books/', '')
        link_category = link_category.replace('/index.html', '')
        # create the key as the name of category
        key_category = link_category.replace('_', '')
        i = str(i)
        key_category = key_category.replace(i, '')
        # assign the category to the good key
        dict_category[key_category] = link_category
        # add 1 to i for the next iteration of the loop
        i = int(i) + 1
    return dict_category[name_category]

def get_a_book_link(list_from_all_book):
    for i in range(len(list_from_all_book)):
        book_page_focus(list_from_all_book[i])



create_csv_column("data.csv")
choice = input("quelle catégorie voulez vous récupérer?:\n")
category_dict = get_category_dict(choice)
category_url = get_category_url(category_dict)
all_books_from_category = get_all_books_from_category(category_url)
get_a_book_link(all_books_from_category)


