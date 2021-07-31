import re
import requests
from bs4 import BeautifulSoup
def extract_url(url):

    if url.find("www.amazon.in") != -1:
        index = url.find("/dp/")
        if index != -1:
            index2 = index + 14
            url = "https://www.amazon.in" + url[index:index2]
        else:
            index = url.find("/gp/")
            if index != -1:
                index2 = index + 22
                url = "https://www.amazon.in" + url[index:index2]
            else:
                url = None
    elif url.find("www.flipkart.com") != -1:
        index = url.find("/p/")
        if index != -1:
            index2 = index + 40
            url = "https://www.flipkart.com/product" + url[index:index2]
        else:
             url = None
    else:
        url = None
    return url
def get_converted_price(price):
    converted_price = float(re.sub(r"[^\d.]", "", price))
    return converted_price
    
def get_product_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }
    details = {"name": "", "price": 0, "deal": True, "url": ""}
    _url = extract_url(url)
    if _url == "":
        details = None
    else:
        if url.find("www.amazon.in") != -1:
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.content, "html5lib")
            title = soup.find(id="productTitle")
            price = soup.find(id="priceblock_dealprice")
            if price is None:
                price = soup.find(id="priceblock_ourprice")
                details["deal"] = False
            if title is not None and price is not None:
                details["name"] = title.get_text().strip()
                details["price"] = get_converted_price(price.get_text())
                details["url"] = _url
            else:
                return None
        elif url.find("www.flipkart.com") != -1:
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.content, "html5lib")
            title = soup.find(class_ = "B_NuCI")
            price = soup.find(class_ = "_30jeq3 _16Jk6d")
            if title is not None and price is not None:
                details["name"] = title.get_text().strip()
                details["price"] = get_converted_price(price.get_text())
                details["url"] = _url
                details["deal"] = "N/A"
            else:
                return None
    return details
print("Enter the URL of the product on Amazon India or Flipkart: ")
productURL = input()
print(get_product_details(productURL))