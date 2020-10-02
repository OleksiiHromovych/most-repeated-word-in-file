from os import path
from re import split, search

from PyPDF2 import PdfFileReader


def input_file_name():
    print("Enter path for you pdf file. Sample D:/Users/Folder/file.pdf")
    file = str(input())
    while not path.exists(file):
        print("Error path")
        file = str(input())
    return file


def update_dict(word_dict: dict, text: str):
    """
    Analyze text, extract words, count them and update already exist dict with new value.

    :param word_dict: dict that contain word as key and word count as value
    :param text: text for extract words
    :return: None
    """
    words = split("  |\n| ", text)
    for word in words:
        word = search(r"\w+", word)
        if not word:
            continue
        word = word.group(0).lower()
        if word.isdigit():
            continue
        word_dict.setdefault(word, 0)
        word_dict[word] += 1


def read_file(file_path: str):
    """
    Read file_path, extract text, and analyze it, count words.

    :param file_path: name of PDF file
    :return: dict with words and their count
    """
    pdfReader = PdfFileReader(open(file_path, "rb"))
    word_dict = {}
    print("Start parsing file - " + file_path)
    for page_ind in range(pdfReader.numPages):
        print("Parse " + str((page_ind + 1)) + " page")
        page = pdfReader.getPage(page_ind)
        update_dict(word_dict, page.extractText())
    return word_dict


def sort_dict(word_dict, key=lambda item: item[1], reverse=True):
    """
    Sort dict by specified parameters.

    :param word_dict: dict that contain word as key and word count as value
    :param key: function by which word_dict will be sorted
    :param reverse: True sort by decrease, False - increase.
    :return: New sorted dict
    """
    return {k: v for k, v in sorted(word_dict.items(), key=key, reverse=reverse)}


def write_file(word_dict, file_path):
    """
    Write word with their count to file_path.

    :param word_dict: dict that contain word as key and word count as value
    :param file_path: path to save file
    :return: boolean with status of writing to file. True - ok, False - some problems.
    """
    print("Write words to file " + file_path)
    try:
        with open(file_path, "w", encoding='utf-8') as file:
            words = [str(i) + " - " + str(j) for i, j in word_dict.items()]
            file.write("\n".join(words))
            print("File success created!")
            print(f"File contain {len(words)}")
            return True
    except IOError as e:
        print(e)
        return False


if __name__ == '__main__':
    file = input_file_name()
    word_dict = read_file(file)
    word_dict = sort_dict(word_dict)
    write_file(word_dict, file.rstrip(".pdf") + ".txt")
    str(input(""))
