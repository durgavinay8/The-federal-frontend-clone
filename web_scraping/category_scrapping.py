import requests
from bs4 import  BeautifulSoup
import sys
import json
from googletrans import Translator

language = ""
translator = Translator()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def translate_text(text):
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

# sys.stdout.reconfigure(encoding='utf-8')

def get_article(url, langToBeTranslated):
    global language
    language = langToBeTranslated
    response=requests.get(f'https://thefederal.com/category/{url}', headers)
    soup=BeautifulSoup(response.content,'html.parser')

    data_to_be_sent = {}
    data_to_be_sent['urls']={}
    data_to_be_sent['texts']={}
    data_to_be_sent["texts"]["breadcrumb_items"]=[]
    data_to_be_sent["urls"]["breadcrumb_items"]=[]
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
    print(breadcrumb_items)
    breadcrumb_hrefs=[]
    breadcrumb_texts=[]
    for breadcrumb_item in breadcrumb_items:
        a_tag = breadcrumb_item.find('a')
        breadcrumb_hrefs.append(a_tag["href"] if a_tag else "")
        breadcrumb_texts.append(translate_text(breadcrumb_item.text))
    data_to_be_sent["texts"]["breadcrumb_items"] = breadcrumb_texts
    data_to_be_sent["urls"]["breadcrumb_items"] = breadcrumb_hrefs
    heading=(soup.find('h1',class_='category_size').text)
    data_to_be_sent['texts']['section_title']=heading

    main_stories=soup.find_all('div',class_='col-md-4')
    for story in main_stories:
        main_data={}
        main_data['urls']={}
        main_data['texts']={}
        main_data['urls']['main_href']=story.find('a',class_='img_only_hover')['href']
        main_data['urls']['article_image_href']=story.find('img',class_='img-fluid')['data-src']
        main_data['texts']['title']=story.find('h3',class_='line_restrict_img_box').text
        main_data['texts']['date_time']=story.find('span',class_='date_time').text
        
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
            data['texts']['title']=story.find('a',class_='img_para_text_hover').text
            data['texts']['date_time']=story.find('span',class_='date_time').text
            data_to_be_sent['level_2']['sub_stories'].append(data)

    l1_main_story_text=soup.find('div',class_='col-xl-5')

    data_to_be_sent['level_1']['main_story']['urls']['article_href']=l1_main_story_text.find('a',class_='sub_title_hover_1')['href']
    data_to_be_sent['level_1']['main_story']['texts']['title']=l1_main_story_text.find('a',class_='sub_title_hover_1').get_text()
    data_to_be_sent['level_1']['main_story']['texts']['date_time']=l1_main_story_text.find('span',class_='date_three_card').get_text()
    data_to_be_sent['level_1']['main_story']['texts']['author']=l1_main_story_text.find('a',class_='author_name_hover').text
    data_to_be_sent['level_1']['main_story']['urls']['author_href']=l1_main_story_text.find('a',class_='author_name_hover')['href']

    l1_main_story_img=soup.find('div',class_='col-xl-7')

    data_to_be_sent['level_1']['main_story']['urls']['article_img_href']=l1_main_story_img.find('img',class_='img-fluid')['data-src']
    data_to_be_sent['level_1']['main_story']['urls']['category_href']=l1_main_story_img.find('a',class_='catTag_hover')['href']
    data_to_be_sent['level_1']['main_story']['texts']['category']=l1_main_story_img.find('a',class_='catTag_hover').text

    l2_main_story=soup.find('div',class_='ad_imgbox_sec')

    data_to_be_sent['level_2']['main_story']['urls']['article_href']=l2_main_story.find('a',class_='img_only_hover')['href']
    data_to_be_sent['level_2']['main_story']['urls']['article_img_href']=l2_main_story.find('img',class_='img-fluid')['data-src']
    data_to_be_sent['level_2']['main_story']['texts']['title']=l2_main_story.find('h2',class_='party_text_1').text
    data_to_be_sent['level_2']['main_story']['texts']['author']=l2_main_story.find('a',class_='author_name_hover').text
    data_to_be_sent['level_2']['main_story']['urls']['author_href']=l2_main_story.find('a',class_='author_name_hover')['href']
    data_to_be_sent['level_2']['main_story']['texts']['date_time']=l2_main_story.find('span',class_='date_three_card').text
    data_to_be_sent['level_2']['main_story']['texts']['para_text']=l2_main_story.find('h2',class_="content_demo").text

    return json.dumps(data_to_be_sent)
