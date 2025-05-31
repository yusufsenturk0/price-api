from flask import Flask, request, jsonify
from scraper import trendyol, hepsiburada, n11

app = Flask(__name__)

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.json
    site = data.get("site")
    product = data.get("product")

    if not site or not product:
        return jsonify({"error": "site ve product zorunludur"}), 400

    if site == "trendyol":
        results = trendyol.trendyol_scrape(product)
    elif site == "hepsiburada":
        results = hepsiburada.hepsiburada_scrape(product)
    elif site == "n11":
        results = n11.n11_scrape(product)
    else:
        return jsonify({"error": "desteklenmeyen site"}), 400

    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(debug=True)