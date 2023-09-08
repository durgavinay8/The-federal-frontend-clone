import requests
from bs4 import BeautifulSoup
import sys
from googletrans import Translator
import json

language = ""
translator = Translator()

def translate_text(text):
#   print("text : ",text)
  if language == "en":
      return text
  for i in range(3):
    try:
        return translator.translate(text, dest=language).text
    except  Exception as e:
        print("Translation request timed out. Retrying...",e)
        continue
  # a lot to-do
  raise Exception("Translation request failed after multiple retries")


def get_article(url, lang):
    global language
    language = lang
    data_to_be_sent={}
    data_to_be_sent["urls"]={}
    data_to_be_sent["texts"]={}
    data_to_be_sent["texts"]["para_text"]=[]
    data_to_be_sent["texts"]["sub_categories_text"]=[]
    data_to_be_sent["urls"]["sub_categories_href"]=[]
    data_to_be_sent["texts"]["breadcrumb_items"]=[]
    data_to_be_sent["urls"]["breadcrumb_items"]=[]
    try:
        # sys.stdout.reconfigure(encoding="utf-8")
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        req=requests.get(f"https://thefederal.com/category/{url}", headers=headers)
        soup=BeautifulSoup(req.content,"html.parser")
        article=soup.find("div",class_="all-details-content-wrap")
        
        breadcrumb_items = soup.select(".breadcrumb-item > a")
        breadcrumb_hrefs=[]
        breadcrumb_texts=[]
        for breadcrumb_item in breadcrumb_items:
            breadcrumb_hrefs.append(breadcrumb_item["href"])
            breadcrumb_texts.append(translate_text(breadcrumb_item.text))
        data_to_be_sent["texts"]["breadcrumb_items"] = breadcrumb_texts
        data_to_be_sent["urls"]["breadcrumb_items"] = breadcrumb_hrefs
        data_to_be_sent["urls"]["article_img_href"]=article.find("img",class_="img-fluid")["src"]
        data_to_be_sent["texts"]["image_context"]=translate_text(article.find("div",class_="image_caption").text)
        data_to_be_sent["texts"]["title"]=translate_text(article.find("h1",class_="article_two_cont_size").text)
        sub_title = article.find("h2")
        data_to_be_sent["texts"]["short_desc"] = translate_text(sub_title.text) if sub_title else ""
        data_to_be_sent["texts"]["author_name"]=translate_text(article.find("span",class_="internal-credit-name").text)
        data_to_be_sent["urls"]["author_href"]=article.find("span",class_="internal-credit-name").parent["href"]
        data_to_be_sent["texts"]["date_time"]=translate_text(article.find("span",class_="convert-to-localtime").text)
        article_text=soup.find("div",class_="entry-main-content")
        data_to_be_sent["texts"]["category"]=translate_text(article.find("a",class_="catTag_hover").text)
        data_to_be_sent["urls"]["category_href"]=article.find("a",class_="catTag_hover")["href"]

        category_list=article.find_all("a",class_="sub_category_button_three")
        for category in category_list:
            data_to_be_sent["urls"]["sub_categories_href"].append(category["href"])
            data_to_be_sent["texts"]["sub_categories_text"].append(translate_text(category.text))
        p_text=article_text.find_all("p")
        for para in p_text:
            data_to_be_sent["texts"]["para_text"].append(translate_text(para.decode_contents()))
        disclaimer = article_text.find("div",class_="feeds_message")
        data_to_be_sent["texts"]["disclaimer"] = translate_text(disclaimer.text) if disclaimer else ""

        # print(data_to_be_sent)
        return data_to_be_sent
    except Exception as e:
        print("error ==> ",e)
        return {"error":"error fetching files"}
