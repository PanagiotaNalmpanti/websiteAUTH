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
        products = mongo.db.products.find({"$text": {"$search": name}})  # search in mongoDB

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
            return jsonify([]) # Return empty list if products not found
    else:
        return jsonify({"error": "Please use parameter 'name'."}), 400 # In case 'name' parameter is missing


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
    return ""
    # END CODE HERE


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
