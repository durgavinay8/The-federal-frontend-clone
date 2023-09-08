from flask import Flask, render_template, jsonify, request
from web_scraping.homepage_scrapping import *
from web_scraping.article_scrapping import *
from web_scraping.header_footer import *

app = Flask(__name__)
# languages_supported = {"english", "telugu", "hindi"}

@app.route("/")
def serve_homepage_html():
    return render_template('index.html')

@app.route("/category/videos")
def videos():
    pass

@app.route("/category/<path:subpath>")
def func(subpath):
    print("subpath===>",subpath)
    language = request.cookies.get('language')
    if language is None:
        language = "en"
    article = get_article(subpath, language)
    article_html = render_template('article.html',article = article, zip_lists = zip_lists)

    header_footer_jsons = get_header_footer_jsons(language)
    combined_response = f'{article_html}\n<script type="text/javascript">renderHeaderSection({header_footer_jsons[0]}); renderFooterSection({header_footer_jsons[1]});</script>'
    return combined_response #header_footer_jsons #200

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

def zip_lists(list1, list2):
    return zip(list1, list2)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
