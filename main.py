import requests
from bs4 import BeautifulSoup


def extract_product_information(elements):
    result = []
    for element in elements:
        result.append(element.string)
    print(result)
    return result


def book_page_focus():
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    response = requests.get(url)
    page = response.content

    soup = BeautifulSoup(page, "html.parser")

    book_product = soup.select_one("tr:nth-child(1) > td")
    book_title = soup.find_all("h1")
    book_price_including_tax = soup.select_one("tr:nth-child(4) > td")
    book_price_excluding_tax = soup.select_one("tr:nth-child(3) > td")
    book_number_available = soup.select_one("tr:nth-child(6) > td")
    book_description = soup.select_one("article > p")
    book_category = soup.select_one("li:nth-child(3) > a")
    #book_rating = soup.select_one("tr:nth-child(1) > td")


    universal_product_code = extract_product_information(book_product)
    title = extract_product_information(book_title)
    price_including_tax = extract_product_information(book_price_including_tax)
    price_excluding_tax = extract_product_information(book_price_excluding_tax)
    number_available = extract_product_information(book_number_available)
    product_description = extract_product_information(book_description)
    category = extract_product_information(book_category)
    #review_rating = extract_product_information(book_rating)


book_page_focus()


