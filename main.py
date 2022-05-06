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
    print(result)
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

#load all data inside "data.csv" file
def load_data(file_name, column, title, UPC, including, excluding, available, description, category, img, rating):
    with open(file_name, 'w') as file_csv:
        writer = csv.writer(file_csv, delimiter=',')
        writer.writerow(column)
        for titles, upc, priceI, priceE, stock, text, cate, url, note in zip(title, UPC, including, excluding, available, description, category, img, rating):
            writer.writerow([titles, upc, priceI, priceE, stock, text, cate, url, note])

def book_page_focus():
    #link of the page
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
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

    image_url = image_url[0]
    image_url = image_url.replace('../..', 'http://books.toscrape.com')
    image_url = [image_url]
    print(image_url)

    #remove text from "number_available" and keep number
    number_available = number_available[0].text
    number_available = number_available.replace('In stock (', '')
    number_available = number_available.replace('available)', '')
    number_available = int(number_available)
    number_available = [number_available]
    print(number_available)
    column = ["title", "universal_product_code", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "image_url", "review_rating"]
    load_data("data.csv", column, title, universal_product_code, price_including_tax, price_excluding_tax, number_available, product_description, category, image_url, review_rating)

book_page_focus()


