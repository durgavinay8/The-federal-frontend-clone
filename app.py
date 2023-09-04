from flask import Flask, render_template, jsonify
from web_scraping.homepage_scrapping import *
from web_scraping.header_footer import *

app = Flask(__name__)
# languages_supported = {"english", "telugu", "hindi"}

@app.route("/")
def serve_homepage_html():
    return render_template('index.html')

@app.route("/api/homepage/<lang>")
def serve_homepage_data(lang):
    print("language: ",lang)
    homepage_json = {}
    homepage_json["main"] = get_homepage_data(lang)
    header_footer_jsons = get_header_footer_jsons(lang)
    homepage_json["header"] = header_footer_jsons[0]
    homepage_json["footer"] = header_footer_jsons[1]

    response = jsonify(homepage_json)
    response.status_code = 200
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
