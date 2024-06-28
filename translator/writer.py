from book import Book, ContentType
from utils import LOG
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)
from reportlab.lib import colors, pagesizes, units


class Writer:
    def __init__(self):
        pass

    def save_translated_book(
        self, book: Book, output_file_path: str = None, file_format: str = "PDF"
    ):
        if file_format.lower() == "pdf":
            self._save_translated_book_pdf(book, output_file_path)
        elif file_format.lower() == "markdown":
            self._save_translated_book_markdown(book, output_file_path)

    def _save_translated_book_pdf(self, book: Book, output_file_path: str = None):
        if output_file_path is None:
            output_file_path = book.pdf_file_path.replace(".pdf", "_translated.pdf")

        LOG.info(f"pdf_file_path: {book.pdf_file_path}")
        LOG.info(f"Start translation: {output_file_path}")

        # register Chinese font
        font_path = "../fonts/simsun.ttc"
        pdfmetrics.registerFont(TTFont("SimSun", font_path))

        # create a new ParagraphStyle with the SimSun font
        simsun_style = ParagraphStyle(
            "SimSun", fontName="SimSun", fontSize=12, leading=14
        )

        # create a PDF document
        doc = SimpleDocTemplate(output_file_path, pagesize=pagesizes.letter)
        story = []

        # iterate over the pages and contents
        for page in book.pages:
            for content in page.contents:
                if content.status:
                    if content.content_type == ContentType.TEXT:
                        # add translated text to PDF
                        text = content.translation
                        para = Paragraph(text, simsun_style)
                        story.append(para)

                    elif content.content_type == ContentType.TABLE:
                        # add table to PDF
                        table = content.translation
                        table_style = TableStyle(
                            [
                                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                ("FONTNAME", (0, 0), (-1, 0), "SimSun"),
                                ("FONTSIZE", (0, 0), (-1, 0), 14),
                                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                                ("FONTNAME", (0, 1), (-1, -1), "SimSun"),
                                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                            ]
                        )
                        pdf_table = Table(table.values.tolist())
                        pdf_table.setStyle(table_style)
                        story.append(pdf_table)

            # add a page break after each page except the last one
            if page != book.pages[-1]:
                story.append(PageBreak())

        # save translated book as a new PDF file
        doc.build(story)
        LOG.info(f"Translation complete: {output_file_path}")

    def _save_translated_book_markdown(self, book: Book, output_file_path: str = None):
        if output_file_path is None:
            output_file_path = book.pdf_file_path.replace(".pdf", "_transalted.md")

        LOG.info(f"pdf_file_path: {book.pdf_file_path}")
        LOG.info(f"Translation start: {output_file_path}")

        with open(output_file_path, "w", encoding="utf-8") as output_file:
            # iterate over pages and contents:
            for page in book.pages:
                for content in page.contents:
                    if content.status:
                        if content.content_type == ContentType.TEXT:
                            # add translated text to markdown file
                            text = content.translation
                            output_file.write(text + "\n\n")

                        elif content.content_type == ContentType.TABLE:
                            # add table to markdown file
                            table = content.translation
                            header = (
                                "| "
                                + " | ".join(str(column) for column in table.columns)
                                + " |"
                                + "\n"
                            )
                            separator = (
                                "| "
                                + " | ".join(["---" * len(table.columns)])
                                + " |"
                                + "\n"
                            )
                            body = (
                                "\n".join(
                                    [
                                        "| "
                                        + " | ".join(str(cell) for cell in row)
                                        + " |"
                                        for row in table.values.tolist()
                                    ]
                                )
                                + "\n\n"
                            )
                            output_file.write(header + separator + body)

                # add page break (horizontal rule) after each page except the last one
                if page != book.pages[-1]:
                    output_file.write("---\n\n")

        LOG.info(f"Translation complete: {output_file_path}")
