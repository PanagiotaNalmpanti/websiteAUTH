# BEGIN CODE HERE
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT
from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# END CODE HERE

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])


@app.route("/search", methods=["GET"])
def search():
    name = request.args.get("name")
    # "$options": "i" makes the search case-insensitive
    products = mongo.db.products.find({"name": {"$regex": name, "$options": "i"}}).sort("price", -1)
    plist = list(products)
    # prevent an error caused by the id that MongoDB gives to the products
    for item in plist:
        item['_id'] = str(item['_id'])
    return jsonify(plist)


@app.route("/add-product", methods=["POST"])
def add_product():
    product_data = request.json

    # Έλεγχος για έγκυρο χρώμα
    valid_colors = [1, 2, 3]
    if "color" in product_data and product_data["color"] not in valid_colors:
        return jsonify("Invalid color code"), 400

    # Έλεγχος για έγκυρο μέγεθος
    valid_sizes = [1, 2, 3, 4]
    if "size" in product_data and product_data["size"] not in valid_sizes:
        return jsonify("Invalid size code"), 400

    existing_product = mongo.db.products.find_one({"name": product_data["name"]})
    if existing_product:
        # If product exists, update its details
        mongo.db.products.update_one(
            {"_id": existing_product["_id"]},
            {
                "$set": {
                    "production_year": product_data["production_year"],
                    "price": product_data["price"],
                    "color": product_data["color"],
                    "size": product_data["size"]
                }
            }
        )
        return "Product updated successfully", 200
    else:
        # If product doesn't exist, insert it
        mongo.db.products.insert_one(product_data)
        return "Product added successfully", 200


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # calculate cosine similarity
    def cosine_similarity(vec1, vec2):
        dot_product = np.dot(vec1, vec2)
        vec1 = np.linalg.norm(vec1)
        vec2 = np.linalg.norm(vec2)
        similarity = dot_product / (vec1 * vec2)
        return similarity

    product_data = request.json

    # convert to numpy array
    query_vec = np.array(
        [product_data['production_year'], product_data['price'], product_data['color'], product_data['size']])

    similar_products = []
    # JSON
    for product in mongo.db.products:
        product_vec = np.array([product['production_year'], product['price'], product['color'], product['size']])
        similar = cosine_similarity(query_vec, product_vec)
        if similar > 0.7:
            similar_products.append(product['name'])

    return jsonify(similar_products)


@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE
    def get_courses(sem):
        url = 'https://qa.auth.gr/el/x/studyguide/600000438/current'
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)

        try:
            driver.get(url)
            wait = WebDriverWait(driver, 10)
            # course_el consists of all the elements that exist in the table of the given exam
            table = wait.until(EC.presence_of_element_located((By.ID, f'exam{sem}')))
            # the courses are in table rows (tr) inside the table body (tbody) inside a table
            course_el = table.find_elements(By.TAG_NAME, 'tr')
            courses = []
            for c in course_el:
                courses.append(c.get_attribute('coursetitle'))  # coursetitle gives the name of the course in the given url (html)
        finally:
            driver.quit()
        return courses

    semester = request.args.get('semester', type=int)
    if semester is not None:
        course_list = get_courses(semester)
        if course_list:
            return jsonify(course_list), 200
        else:
            return jsonify({'error': f'Failed to get courses for semester {semester}'}), 404
    else:
        return jsonify({'error': 'Please use parameter "semester", or give a valid integer'}), 400
    # END CODE HERE
