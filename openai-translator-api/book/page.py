from .content import Content


class Page:
    def __init__(self) -> None:
        self.contents = []

    def add_content(self, content: Content):
        self.contents.append(content)
