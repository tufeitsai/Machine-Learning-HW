import sys
import json
from lxml import etree
import os

# Define any helper functions here
def hash_fun(author_name):
    # hashing by the length of author's name
    author_name_num = 0
    for i in author_name:
        author_name_num += 1
    return author_name_num % 2

'''
def add_book(book_id, book_json):
    # INPUT : book json from command line
    # RETURN : 1 if successful, else 0
    # Assume JSON is well formed with no missing attributes

    book_data = json.loads(book_json)
    xml_num = hash_fun(book_data['author'])
    xml_name = f'file{xml_num}.xml'

    if os.path.exists(xml_name):
        tree = etree.parse(xml_name)
        root = tree.getroot()
    else:
        root = etree.Element('books')
        tree = etree.ElementTree(root)

        # Create a new book element and populate it
    book_element = etree.SubElement(root, 'book', id=str(book_id))
    for key, value in book_data.items():
        child = etree.SubElement(book_element, key)
        child.text = str(value)

    # Write back to the XML file
    tree.write(xml_name, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    return 1
'''

def add_book(book_id, book_json):
    # INPUT : book json from command line
    # RETURN : 1 if successful, else 0
    # Assume JSON is well formed with no missing attributes
    try:
        book_data = json.loads(book_json)
        xml_num = hash_fun(book_data['author'])
        xml_name = XML_FILES[xml_num]  # Using the global XML_FILES dictionary

        # Load the XML file
        tree = etree.parse(xml_name)
        root = tree.getroot()

        # Create a new book element and populate it
        book_element = etree.SubElement(root, 'book', id=str(book_id))
        for key, value in book_data.items():
            child = etree.SubElement(book_element, key)
            child.text = str(value)

        # Write back to the XML file
        tree.write(xml_name, pretty_print=True, xml_declaration=True, encoding='UTF-8')

        return "Successfully added"

    except:
        return "Not Successful"

def search_by_author(author_name):
    # INPUT: name of author
    # RETURN: list of strings containing only book titles
    # EXPECTED RETURN TYPE: ['book title 1', 'book title 2', ...]

    xml_num = hash_fun(author_name)
    xml_path = XML_FILES[xml_num]

    tree = etree.parse(xml_path)

    xpath_query = f".//book[author='{author_name}']/title"

    book_titles = tree.xpath(xpath_query + "/text()")

    results = [title for title in book_titles]

    return results

'''
book_id = 100
book_json = '{"author": "john smith", "title": "The Great Adventure", "year": "2021", "price": "29.99"}'
result = add_book(book_id, book_json)
print(f"Book added successfully: {result}")

book_id_2 = 200
book_json_2 = '{"author": "Smith", "title": "The Book", "year": "2021", "price": "30.99"}'
result_2 = add_book(book_id_2, book_json_2)
print(f"Book added successfully: {result_2}")
'''

# search_by_author('john smith')

tree = etree.parse('file1.xml')
print(tree.xpath("/books/book[author = 'Michael Jackson']/title/text()"))


# tree = etree.parse(xml_path)
name = 'Michael Jackson'
xpath_query = f"/books/book[author='{name}']/title/text()"

print(tree.xpath(xpath_query))


# Use the df_split1 p=5 model


X = df_split1.drop(columns=['instance','label'])
y = df_split1['label']


logit = LogisticRegression(max_iter=1000)
rfecv = RFECV(estimator=logit, cv=5, scoring='accuracy')
rfecv.fit(X, y)

selected_features = X.columns[rfecv.support_]

logit.fit(X[selected_features], y)

y_pred = logit.predict(X[selected_features])


accuracy = accuracy_score(y, y_pred)
print("Accuracy:", accuracy)


conf_matrix = confusion_matrix(y, y_pred)
print("Confusion Matrix:")
print(conf_matrix)

y_score = logit.decision_function(X[selected_features])
fpr, tpr, _ = roc_curve(y, y_score)
roc_auc = auc(fpr, tpr)
print("AUC:", roc_auc)

plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.title('ROC')
plt.show()

values = best_p_values_all_splits['df_split1']
print(f"Dataset: {split}, Best p: {values['best_p']}, Best Accuracy: {values['best_accuracy']:.4f}")
print("Selected Features:")
print(values['selected_features'])
print("Logistic Regression Coefficients:")
print(logit.coef_)

# P-value
logit.fit(X[selected_features], y)
std_errors = np.sqrt(np.diag(np.linalg.inv(np.dot(X[selected_features].T, X[selected_features]))))

z_values = logit.coef_[0] / std_errors
p_values = norm.sf(np.abs(z_values)) * 2
for coef, p_val, feature in zip(logit.coef_[0], p_values, selected_features):
    print(f"{feature}: Coefficient = {coef:.4f}, p-value = {p_val:.4f}")