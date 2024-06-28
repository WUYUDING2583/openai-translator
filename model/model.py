from book import ContentType


class Model:
    def make_text_prompt(self, text: str, target_language: str) -> str:
        return f"Translate to {target_language}: {text}"

    def make_table_prompt(self, table: str, target_language: str) -> str:
        return f"This is a string in an array, translate all texts to {target_language}, keep spacing (spaces, delimiters), return translated data in table form: \n{table}"

    def translate_prompt(self, content, target_language: str) -> str:
        if content.content_type == ContentType.TEXT:
            return self.make_text_prompt(content.original, target_language)
        elif content.content_type == ContentType.TABLE:
            return self.make_table_prompt(
                content.get_original_as_str(), target_language
            )

    def make_request(self, prompt):
        raise NotImplementedError("Child class must implement make_request method.")
