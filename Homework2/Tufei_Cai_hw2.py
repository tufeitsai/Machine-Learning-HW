# IMPORT LIBRARIES
import sys
import json
from lxml import etree


# Define any helper functions here
def hash_fun(author_name):
    # Hashing function from Hw1
    # hashing by the length of author's name
    author_name_num = 0
    for i in author_name:
        author_name_num += 1
    return author_name_num % 2


def add_book(book_id, book_json):
    # INPUT : book json from command line
    # RETURN : 1 if successful, else 0 
    # Assume JSON is well formed with no missing attributes

    # Test if the data is following desire format
    try:
        book_data = json.loads(book_json)
        xml_num = hash_fun(book_data['author'])
        xml_name = XML_FILES[xml_num]

        # Create a root if the root is not exist, otherwise use the root
        try:
            tree = etree.parse(xml_name)
            root = tree.getroot()
        except:
            root = etree.Element('books')
            tree = etree.ElementTree(root)

        # Test if the id is unique, otherwise return 0
        unique_id = root.find(f".//book[@id='{book_id}']")
        if unique_id is not None:
            return 0

        book_element = etree.SubElement(root, 'book', id=str(book_id))

        for key, value in book_data.items():
            child = etree.SubElement(book_element, key)
            child.text = str(value)

        tree.write(xml_name, pretty_print=True, xml_declaration=True, encoding='UTF-8')

        return 1

    except:
        return 0


def search_by_author(author_name):
    # INPUT: name of author
    # RETURN: list of strings containing only book titles
    # EXPECTED RETURN TYPE: ['book title 1', 'book title 2', ...]

    xml_num = hash_fun(author_name)
    xml_path = XML_FILES[xml_num]

    tree = etree.parse(xml_path)
    xpath_query = f"//book[author='{author_name}']/title/text()"

    return tree.xpath(xpath_query)


def search_by_year(year):
    # INPUT: year of publication
    # RETURN: list of strings containing only book titles
    # EXPECTED RETURN TYPE: ['book name 1', 'book name 2', ...]

    result = []

    for xml_path in XML_FILES.values():
        tree = etree.parse(xml_path)
        xpath_query = f"//book[year/text()='{year}']/title/text()"
        result += tree.xpath(xpath_query)

    return result


# Use the below main method to test your code
if __name__ == "__main__":
    if len(sys.argv) < 5:
        sys.exit("\nUsage: python3 script.py [path/to/file0.xml] [path/to/file1.xml] [operation] [arguments]\n")

    xml0, xml1 = sys.argv[1], sys.argv[2]

    # Assume XML files exist at mentioned path and are initialized with empty <bib> </bib> tags
    global XML_FILES
    XML_FILES = {
        0: xml0,
        1: xml1
    }

    operation = sys.argv[3].lower()

    if operation == "add_book":
        result = add_book(sys.argv[4], sys.argv[5])
        print(result)
    elif operation == "search_by_author":
        books = search_by_author(sys.argv[4])
        print(books)
    elif operation == "search_by_year":
        year = int(sys.argv[4])
        books = search_by_year(year)
        print(books)
    else:
        sys.exit("\nInvalid operation.\n")
