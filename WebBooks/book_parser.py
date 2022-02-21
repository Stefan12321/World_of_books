import json
import time

import requests
from bs4 import BeautifulSoup
from catalog.models import Book, Language, Genre, Author


class GetGenreBooksList:
    def __init__(self, genre: str):
        self.api = 'https://www-api.strandbooks.com/api'
        self.book_id_list = []
        self.book_list = self.__get_books_list(genre)
        for book in self.book_list:
            self.book_id_list.append(book['id'])

        for i in range(35,len(self.book_id_list)):
            time.sleep(1)
            try:
                self.__get_one_book(self.book_id_list[i])
                print("Books stolen", i+1)
            except Exception as e:
                print("Failed to stole", i+1, e)


    @staticmethod
    def __get_one_book(book_id):
        GetBook(book_id)

    def __get_books_list(self, genre: str) -> list:
        response = requests.post(self.api, json={
                                                "operationName": "getProdSection",
                                                "variables": {
                                                    "param": {},
                                                    "section": genre,
                                                    "order": {
                                                        "dir": "ASC",
                                                        "orderBy": "TITLE"
                                                    },
                                                    "filter": {
                                                        "onHand": 1,
                                                        "signed": False,
                                                        "condition": "ANY",
                                                        "binding": "ANY",
                                                        "salePriceStv": {
                                                            "maxStv": 1000000,
                                                            "minStv": 100
                                                        },
                                                        "stockFilter": "ANY",
                                                        "copyrightYear": {
                                                            "minYear": 0,
                                                            "maxYear": 0
                                                        }
                                                    }
                                                },
                                                "query": "query getProdSection($order: OrderCommonIn, $param: ProductParamTypeIn!, $section: String!, $filter: FilterCommonIn) {\n  productBySection(order: $order, param: $param, section: $section, filter: $filter, limit: 400) {\n    product {\n      gtin13\n      id\n      imageUrl\n      bookBinding\n      inventory {\n        onHand\n        salePrice\n        salePriceStv\n        section\n        signed\n        sku\n        store\n        __typename\n      }\n      apparel {\n        apparelId\n        size\n        sizeDesc\n        inventory {\n          catalogId\n          condition\n          sku\n          onHand\n          salePriceStv\n          __typename\n        }\n        __typename\n      }\n      inventoryOverview {\n        conditionList\n        locationList\n        onHand\n        sectionList\n        signedList\n        __typename\n      }\n      isbn10\n      keywords\n      originator\n      outOfPrint\n      publisher\n      retailStv\n      retailPrice\n      title\n      webDescription\n      __typename\n    }\n    __typename\n  }\n}\n"
                                            }).json()
        # print(type(response))
        return response['data']['productBySection'][0]['product']

    def __repr__(self):
        return f"Book list: {self.book_id_list}"


class GetBook:
    def __init__(self, ean: str):
        self.api = 'https://www-api.strandbooks.com/api'
        self.ean = ean
        self.path_to_images = "./media/images"
        book = self.__parce_response(self.__get_one_book(self.ean))
        self.isbn = book['isbn']
        self.title = book['title']
        self.summary = book['summary']
        self.genre = book['genre']
        self.langauge = book['langauge']
        self.price = book['price']
        self.image = book['image']
        self.author = book['author']
        self.__save_image(url=self.image)
        if not self.__is_author_in_database(self.author):
            self.__save_author_to_database()
        self.__save_book_to_database()

    def __get_one_book(self, ean: str) -> dict:
        response = requests.post(self.api, json={
                "operationName": "getSingleProduct",
                "variables": {
                    "ean": ean
                },
                "query": "query getSingleProduct($ean: String!) {\n  productDetail(ean: $ean) {\n    bookBinding\n    bookFormat\n    copyright\n    description\n    gtin13\n    id\n    apparel {\n      apparelId\n      size\n      sizeDesc\n      inventory {\n        catalogId\n        condition\n        sku\n        onHand\n        salePriceStv\n        __typename\n      }\n      __typename\n    }\n    imageUrl\n    webDescription\n    inventoryOverview {\n      conditionList\n      discountMaxPct\n      discountMinPct\n      locationList\n      onHand\n      salePriceMaxStv\n      salePriceMinStv\n      sectionList\n      signedList\n      __typename\n    }\n    inventory {\n      condition\n      discountPct\n      edition\n      isTaxable\n      jacketCondition\n      location\n      onHand\n      salePrice\n      salePriceStv\n      section\n      signed\n      sku\n      store\n      catalogId\n      __typename\n    }\n    isbn10\n    originDate\n    originator\n    outOfPrint\n    prop {\n      edition\n      heightIn00\n      noShipExpedited\n      noShipInternational\n      pagecount\n      publishPlace\n      thicknessIn00\n      universityPress\n      weightOz00\n      weightLb00\n      widthIn00\n      __typename\n    }\n    publisher\n    retailPrice\n    retailStv\n    salePriceMax\n    salePriceMin\n    title\n    __typename\n  }\n  productDetailAux(ean: $ean) {\n    annotation\n    contributors\n    description\n    dimensions\n    ean\n    jacket\n    publisherImprint\n    __typename\n  }\n}\n"
            }).json()
        return response

    @staticmethod
    def __parce_response(response: dict) -> dict:
        product_detail = response['data']['productDetail']
        return {'isbn': product_detail['gtin13'],
                'title': product_detail['title'],
                'summary': product_detail['webDescription'],
                'genre': product_detail['inventoryOverview']['sectionList'],
                'langauge': "english",
                'price': product_detail['inventory'][0]['salePrice'],
                'image': product_detail['imageUrl'],
                'author': product_detail['originator']}

    def __save_image(self, url):
        response = requests.get(url)
        file = open(f"{self.path_to_images}/{self.ean}.png", "wb")
        file.write(response.content)
        file.close()

    def __save_author_to_database(self):
        author = Author()
        author.first_name = self.author.split()[0]
        author.last_name = self.author.split()[1]
        author.save()

    @staticmethod
    def __is_author_in_database(author):
        authors_list = Author.objects.all()
        for db_author in authors_list:
            if author == f"{db_author.first_name} {db_author.last_name}":
                return True
        return False

    def __save_book_to_database(self):
        book = Book()
        book.isbn = self.isbn
        book.image = f"images/{self.ean}.png"
        book.title = self.title
        book.summary = self.summary
        book.language = Language.objects.get(id=1)
        book.genre = Genre.objects.get(id=11)
        book.price = self.price
        book.save()
        book.author.add(
            list(Author.objects.filter(first_name="Michelle").filter(last_name="Zauner").values_list('id', flat=True))[0])

    def __repr__(self):
        return f"isbn: {self.isbn}"\
               f"title: {self.title}"\
               f"summary: {self.summary}"\
               f"genre: {self.genre}"\
               f"langauge: {self.langauge}"\
               f"price: {self.price}"\



if __name__ == '__main__':
    pass
    # GetBook("9781586422387")
    # print(GetGenreBooksList("CRIME"))
