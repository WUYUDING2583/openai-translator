from book.page import Page


class Book:
    def __init__(self, filename: str):
        self.filename = filename
        self.pages = []

    def add_page(self, page: Page):
        self.pages.append(page)
