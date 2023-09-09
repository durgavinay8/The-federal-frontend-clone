from flask import Flask, render_template, jsonify, request, abort
from web_scraping.homepage_scrapping import *
from web_scraping.article_category_scrapping import *
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
    print('request taken')
    print("subpath===>",subpath)
    if subpath == "undefined": 
        abort(404)
    language = request.cookies.get('language')
    if language is None:
        language = "en"
    body_json_data = get_body_json_data(subpath, language)
    header_footer_jsons = get_header_footer_jsons(language)
    if body_json_data[0]:
        html_content = render_template('article.html',article = body_json_data[1], zip_lists = zip_lists)
        combined_response = f'{html_content}\n<script type="text/javascript">renderHeaderSection({header_footer_jsons[0]}); renderFooterSection({header_footer_jsons[1]});</script>'
    else:
        html_content = render_template('category.html')
        combined_response = f'{html_content}\n<script type="text/javascript">renderHeaderSection({header_footer_jsons[0]}); renderMainSection({body_json_data[1]});renderFooterSection({header_footer_jsons[1]});</script>'
        
    print('request served')
    return combined_response

@app.route("/api/homepage/<level>/<lang>")
def serve_homepage_data(level,lang):
    print('request taken')
    if lang == "undefined": 
        abort(404)
    response = jsonify(get_homepage_data(level[5],lang))
    response.status_code = 200
    print('request served')
    return response

@app.route("/api/header-footer/<lang>")
def serve_headerfooter_data(lang):
    print('request taken')
    if lang == "undefined": 
        abort(404)
    data_to_be_sent = {}
    header_footer_jsons = get_header_footer_jsons(lang)
    data_to_be_sent['header'] = header_footer_jsons[0]
    data_to_be_sent['footer'] = header_footer_jsons[1]
    data_to_be_sent = jsonify(data_to_be_sent)
    data_to_be_sent.status_code = 200
    print('request served')
    return data_to_be_sent

def zip_lists(list1, list2):
    print("list1==>",list1)
    return zip(list1, list2)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
