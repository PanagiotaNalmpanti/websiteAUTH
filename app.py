# BEGIN CODE HERE
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT

# END CODE HERE

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])


@app.route("/search", methods=["GET"])
def search():
    name = request.args.get("name")
    if name:
        # "$options": "i" makes the search case-insensitive
        products = mongo.db.products.find({"name": {"$regex": name, "$options": "i"}})  # search in mongoDB

        if products.count() > 0:
            products = list(products)

            # Sorting the products in descending price order
            n = len(products)
            for i in range(n):
                for j in range(0, n - i - 1):
                    if products[j]['price'] < products[j + 1]['price']:
                        products[j], products[j + 1] = products[j + 1], products[j]

            # JSON
            response = []
            for product in products:
                response.append({
                    "id": str(product["_id"]),
                    "name": product["name"],
                    "production_year": product["production_year"],
                    "price": product["price"],
                    "color": product["color"],
                    "size": product["size"]
                })
            return jsonify(response)

        else:
            return jsonify([])  # Return empty list if products not found
    else:
        return jsonify({"error": "Please use parameter 'name'."}), 400  # In case 'name' parameter is missing


@app.route("/add-product", methods=["POST"])
def add_product():
    product_data = request.json

    # Έλεγχος για έγκυρο χρώμα
    valid_colors = [1, 2, 3]
    if "color" in product_data and product_data["color"] not in valid_colors:
        return jsonify({"error": "Invalid color code"}), 400

    # Έλεγχος για έγκυρο μέγεθος
    valid_sizes = [1, 2, 3, 4]
    if "size" in product_data and product_data["size"] not in valid_sizes:
        return jsonify({"error": "Invalid size code"}), 400

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
        return "Product added successfully", 201


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # BEGIN CODE HERE
    return ""
    # END CODE HERE


@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE
    return ""
    # END CODE HERE
