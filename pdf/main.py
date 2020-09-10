from PyPDF2 import PdfFileReader
from re import split, search
from os import path

print("Enter path for you pdf file. Sample D:/Users/Folder/file.pdf")
PDF_FILE = str(input())
while not path.exists(PDF_FILE):
    print("Error path")
    PDF_FILE = str(input())


def add_word(d: dict, text: str):
    words = split("  |\n| ", text)
    for word in words:
        word = search(r"\w+", word)
        if not word:
            continue
        word = word.group(0).lower()
        if word.isdigit():
            continue
        d.setdefault(word, 0)
        d[word] += 1


pdfReader = PdfFileReader(open(PDF_FILE, "rb"))
d = {}
print("Start parsing file - " + PDF_FILE)
for page_ind in range(pdfReader.numPages):
    print("Parse " + str((page_ind + 1)) + " page")
    page = pdfReader.getPage(page_ind)
    add_word(d, page.extractText())

d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}

print("Write words to file " + PDF_FILE.rstrip(".pdf") + ".txt")
with open(PDF_FILE.rstrip(".pdf") + ".txt", "w", encoding='utf-8') as file:
    words = [str(i) + " - " + str(j) for i, j in d.items()]
    file.write("\n".join(words))
str(input(""))
