import logging
import os

logger = logging.getLogger(__name__)


def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    punctuation_marks = '.,!:;?'
    text_book = text[start:(start + size)]
    if ((start+size) >= len(text)) and text_book[-1] in punctuation_marks:
        return (text_book, len(text) - start)
    elif text[(start+size)] == ' ' and text_book[-1] in punctuation_marks:
        return (text_book, size)
    else:
        text_book = text_book.split(' ')[:-1]
        temp = text_book[-1][-1]
        while temp not in (punctuation_marks + '\n'):
            text_book.pop(-1)
            if len(text_book[-1])>0:
                temp = text_book[-1][-1]
            else:
                temp = '@'

        text_book = ' '.join(text_book)
        if text_book[-1][-1] == '\n':
            text_book = text_book[:-1]
        dif = size - len(text_book)
        return (text_book, size-dif)



def prepare_book(path: str, page_size: int = 1050) -> dict[int, str]:
    try:
        with open(file=os.path.normpath(path), mode="r", encoding="utf-8") as file:
            text = file.read()
    except Exception as e:
        logger.error("Error reading a book: %s", e)
        raise e

    book = {}
    start, page_number = 0, 1

    while start < len(text):
        page_text, actual_page_size = _get_part_text(text, start, page_size)
        start += actual_page_size
        book[page_number] = page_text.strip()
        page_number += 1

    return book