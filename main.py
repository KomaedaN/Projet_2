import requests
from bs4 import BeautifulSoup


def extract_product_information(elements,i):
    result = []
    for element in elements:
        result.append(element.string)
    print(result[i])
    return result[i]


def book_page_focus():
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    response = requests.get(url)
    page = response.content

    soup = BeautifulSoup(page, "html.parser")

    book_title = soup.find_all("h1")
    book_product = soup.find_all("td")
    book_description = soup.find_all("p")
    book_category = soup.find_all("a")
    #book_rating = soup.find_all("p", "star-rating")

    universal_product_code = extract_product_information(book_product, 0)
    title = extract_product_information(book_title, 0)
    price_including_tax = extract_product_information(book_product, 3)
    price_excluding_tax = extract_product_information(book_product, 2)
    number_available = extract_product_information(book_product, 5)
    product_description = extract_product_information(book_description, 3)
    category = extract_product_information(book_category, 3)
    #review_rating = extract_product_information(book_rating, 0)


book_page_focus()


