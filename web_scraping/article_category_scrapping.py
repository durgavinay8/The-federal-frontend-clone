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


def get_body_json_data(url, langToBeTranslated):
    global language
    language = langToBeTranslated
    # True --> article
    # False --> category
    articleOrCategory = True 

    sys.stdout.reconfigure(encoding="utf-8")
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    req=requests.get(f"https://thefederal.com/category/{url}", headers=headers)
    soup=BeautifulSoup(req.content,"html.parser")
    
    data_to_be_sent={}
    data_to_be_sent["urls"]={}
    data_to_be_sent["texts"]={}
    data_to_be_sent["texts"]["breadcrumb_items"]=[]
    data_to_be_sent["urls"]["breadcrumb_items"]=[]

    breadcrumb_items = soup.find_all('li',class_="breadcrumb-item")
    breadcrumb_hrefs=[]
    breadcrumb_texts=[]
    for breadcrumb_item in breadcrumb_items:
        a_tag = breadcrumb_item.find('a')
        if not a_tag:
            articleOrCategory = False 
        breadcrumb_hrefs.append(a_tag["href"] if a_tag else "")
        breadcrumb_texts.append(translate_text(breadcrumb_item.text))
    data_to_be_sent["texts"]["breadcrumb_items"] = breadcrumb_texts
    data_to_be_sent["urls"]["breadcrumb_items"] = breadcrumb_hrefs

    if articleOrCategory:
        data_to_be_sent["texts"]["para_text"]=[]
        data_to_be_sent["texts"]["sub_categories_text"]=[]
        data_to_be_sent["urls"]["sub_categories_href"]=[]

        article=soup.find("div",class_="all-details-content-wrap")

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
    else:
        data_to_be_sent['level_2']={}
        data_to_be_sent['level_1']={}
        data_to_be_sent['level_1']['sub_stories']=[]
        data_to_be_sent['level_2']['sub_stories']=[]
        data_to_be_sent['level_1']['main_story']={}
        data_to_be_sent['level_2']['main_story']={}
        data_to_be_sent['level_1']['main_story']['urls']={}
        data_to_be_sent['level_2']['main_story']['urls']={}
        data_to_be_sent['level_1']['main_story']['texts']={}
        data_to_be_sent['level_2']['main_story']['texts']={}
        breadcrumb_items = soup.find_all('li',class_="breadcrumb-item")
        breadcrumb_hrefs=[]
        breadcrumb_texts=[]
        for breadcrumb_item in breadcrumb_items:
            a_tag = breadcrumb_item.find('a')
            breadcrumb_hrefs.append(a_tag["href"] if a_tag else "")
            breadcrumb_texts.append(translate_text(breadcrumb_item.text))
        data_to_be_sent["texts"]["breadcrumb_items"] = breadcrumb_texts
        data_to_be_sent["urls"]["breadcrumb_items"] = breadcrumb_hrefs
        data_to_be_sent['texts']['section_title']=translate_text(soup.find('h1',class_='category_size').text)

        main_stories=soup.find_all('div',class_='col-md-4')
        for story in main_stories:
            main_data={}
            main_data['urls']={}
            main_data['texts']={}
            main_data['urls']['article_href']=story.find('a',class_='img_only_hover')['href']
            main_data['urls']['article_img_href']=story.find('img',class_='img-fluid')['data-src']
            main_data['texts']['title']=translate_text(story.find('h3',class_='line_restrict_img_box').text)
            main_data['texts']['date_time']=translate_text(story.find('span',class_='date_time').text)
            main_data['urls']['category_href']=story.find('a',class_='category_tag')['href']
            main_data['texts']['category']=translate_text(story.find('a',class_='category_tag').text)
            data_to_be_sent['level_1']['sub_stories'].append(main_data)

        stories=soup.find('div',class_='body_data_wrapper')
        stories=stories.find_all('div',class_='col-lg-6')

        for story in stories:
            data={}
            data['urls']={}
            data['texts']={}
            if(story.find('a',class_='img_para_text_hover') is None):
                pass
            else:
                data['urls']['article_href']=story.find('a',class_='img_para_text_hover')['href']
                # print(data['urls']['article_href'])
                data['urls']['article_img_href']=story.find('img',class_='img-fluid')['data-src']
                data['texts']['title']=translate_text(story.find('a',class_='img_para_text_hover').text)
                data['texts']['date_time']=translate_text(story.find('span',class_='date_time').text)
                data_to_be_sent['level_2']['sub_stories'].append(data)

        l1_main_story_text=soup.find('div',class_='col-xl-5')

        data_to_be_sent['level_1']['main_story']['urls']['article_href']=l1_main_story_text.find('a',class_='sub_title_hover_1')['href']
        data_to_be_sent['level_1']['main_story']['texts']['article_title']=translate_text(l1_main_story_text.find('a',class_='sub_title_hover_1').get_text())
        data_to_be_sent['level_1']['main_story']['texts']['date_time']=translate_text(l1_main_story_text.find('span',class_='date_three_card').get_text())
        data_to_be_sent['level_1']['main_story']['texts']['author']=translate_text(l1_main_story_text.find('a',class_='author_name_hover').text)
        short_desc = l1_main_story_text.find('h2',class_='category_third_content')
        data_to_be_sent['level_1']['main_story']['texts']['short_desc']=translate_text(short_desc.text) if short_desc else ""
        data_to_be_sent['level_1']['main_story']['urls']['author_href']=l1_main_story_text.find('a',class_='author_name_hover')['href']

        l1_main_story_img=soup.find('div',class_='col-xl-7')

        data_to_be_sent['level_1']['main_story']['urls']['article_img_href']=l1_main_story_img.find('img',class_='img-fluid')['data-src']
        data_to_be_sent['level_1']['main_story']['urls']['category_href']=l1_main_story_img.find('a',class_='catTag_hover')['href']
        data_to_be_sent['level_1']['main_story']['texts']['category']=translate_text(l1_main_story_img.find('a',class_='catTag_hover').text)

        l2_main_story=soup.find('div',class_='ad_imgbox_sec')

        data_to_be_sent['level_2']['main_story']['urls']['article_href']=l2_main_story.find('a',class_='img_only_hover')['href']
        data_to_be_sent['level_2']['main_story']['urls']['article_img_href']=l2_main_story.find('img',class_='img-fluid')['data-src']
        data_to_be_sent['level_2']['main_story']['texts']['title']=translate_text(l2_main_story.find('h2',class_='party_text_1').text)
        data_to_be_sent['level_2']['main_story']['texts']['author']=translate_text(l2_main_story.find('a',class_='author_name_hover').text)
        data_to_be_sent['level_2']['main_story']['urls']['author_href']=l2_main_story.find('a',class_='author_name_hover')['href']
        data_to_be_sent['level_2']['main_story']['texts']['date_time']=translate_text(l2_main_story.find('span',class_='date_three_card').text)
        data_to_be_sent['level_2']['main_story']['texts']['para_text']=translate_text(l2_main_story.find('h2',class_="content_demo").text)
        
        sub_categories_list = soup.find('ul', class_ = 'custom_navMenu_2')
        data_to_be_sent['urls']['sub_categories'] = []
        data_to_be_sent['texts']['sub_categories'] = []
        if sub_categories_list:
            sub_categories_list = sub_categories_list.find_all('a')
            sub_categories_urls = []
            sub_categories_texts = []
            for sub_category in sub_categories_list:
                sub_categories_urls.append(sub_category['href'])
                sub_categories_texts.append(translate_text(sub_category.text))
            data_to_be_sent['urls']['sub_categories'] = sub_categories_urls
            data_to_be_sent['texts']['sub_categories'] = sub_categories_texts

        prev_next_pages = soup.select('.pagination > a')
        if len(prev_next_pages)==1:
            data_to_be_sent["urls"]["next_page"] = prev_next_pages[0]['href']
            data_to_be_sent["texts"]["next_page"] = translate_text(prev_next_pages[0].text)
        else:
            data_to_be_sent["urls"]["prev_page"] = prev_next_pages[0]['href']
            data_to_be_sent["texts"]["prev_page"] = translate_text(prev_next_pages[0].text)
            data_to_be_sent["urls"]["next_page"] = prev_next_pages[1]['href']
            data_to_be_sent["texts"]["next_page"] = translate_text(prev_next_pages[1].text)

    # json_data = json.dumps(data_to_be_sent, indent=4)
    # with open('data.json', 'w') as json_file:
    #     json_file.write(json_data)
    return [articleOrCategory,data_to_be_sent]

# get_body_json_data('news','en')

