import requests
import json
from googletrans import Translator
from bs4 import BeautifulSoup
from flask import  url_for

url=f'https://thefederal.com/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.content,"html.parser")
######
language = ""
data_to_be_fed={}
level1={}
level7={}
translator = Translator()
headings = {
  "en":{
    "the_eighth_column":"the eighth column",
    "premium_access_subscription":"premium access subscription",
    "home":"home",
    "top_stories":"top stories",
    "whats_brewing":"whats brewing",
    "state_of_the_nation":"state of the nation",
    "fault_lines":"fault lines",
    "two_bit":"two-bit",
    "the_federal_playlist":"the federal playlist",
    "brand_studio":"brand studio",
    "subscribe":"subscribe"
  },
  "te":{
    "the_eighth_column":"ది ఎయిట్ కాలమ్",
    "premium_access_subscription":"ప్రీమియం యాక్సెస్ సబ్‌స్క్రిప్షన్",
    "home":"హోమ్",
    "top_stories":"ప్రధాన కథలు",
    "whats_brewing":"వాట్స్ బ్రూయింగ్",
    "state_of_the_nation":"దేశం యొక్క పరిస్థితి",
    "fault_lines":"ఫాల్ట్ లైన్స్",
    "two_bit":"టూ-బిట్",
    "the_federal_playlist":"ది ఫెడరల్ ప్లేజాబితా",
    "brand_studio":"బ్రాండ్ స్టూడియో",
    "subscribe":"సభ్యత్వం పొందండి"
  },
  "hi":{
    "the_eighth_column":"द एइथ कॉलम",
    "premium_access_subscription":"प्रीमियम एक्सेस सब्सक्रिप्शन",
    "home":"होम",
    "top_stories":"मुख्य कहानियाँ",
    "whats_brewing":"व्हाट्स ब्रुइंग",
    "state_of_the_nation":"राष्ट्र की स्थिति",
    "fault_lines":"फॉल्ट लाइंस",
    "two_bit":"टू-बिट",
    "the_federal_playlist":"द फेडरल प्लेलिस्ट ",
    "brand_studio":"ब्रांड स्टूडियो",
    "subscribe":"सदस्यता लें"
  },
  "ta":{
    "the_eighth_column":"தி எய்ட் காலம்",
    "premium_access_subscription":"பிரீமியம் அணுகல் சந்தா",
    "home":"ஹோம்",
    "top_stories":"முக்கிய கதைகள்",
    "whats_brewing":"என்ன வருகின்றது",
    "state_of_the_nation":"நாட்டின் நிலை",
    "fault_lines":"பிழை ரேகைகள்",
    "two_bit":"இரு-பிட் ",
    "the_federal_playlist":"தி ஃபெடரல் ப்ளேய்லிஸ்ட்",
    "brand_studio":"பிராண்ட் ஸ்டூடியோ",
    "subscribe":"பதிவு"
  }
}
def translate_text(text):
  if language == "en":
      return text
  for i in range(3):
    try:
        return translator.translate(text, dest=language).text
    except:
        print("translate_textslation request timed out. Retrying...")
        continue
  
  raise Exception("translate_textslation request failed after multiple retries")

def level1_topstories():
  topStory_soup=soup.find('div','topStory_dataBox')
  topStory_title=topStory_soup.find('a','main_title_hover_1')
  topStory={}
  topStory['section_title']=headings[language]['top_stories']
  topStory['section_href']=topStory_title['href']
  main_story={}
  url={}
  texts={}
  topStory_subtitle=topStory_soup.find('a','sub_title_hover_1')
  texts['title']=translate_text(topStory_subtitle.text)
  url['article_href']=topStory_subtitle['href']
  topStory_para=topStory_soup.find('a','para_text_hover_1')
  texts['para_text']=translate_text(topStory_para.text)

  topStory_img_soup= soup.find('div','topStory_imgBox')
  topStory_img=topStory_img_soup.find('a','img_only_hover')
  url['article_img_href']=topStory_img.img['data-src']
  topStory_category= topStory_img_soup.find('a','catTag_hover')

  texts['category']=translate_text(topStory_category.span.text)
  url['category_href']=topStory_category['href']
  main_story['texts']=texts
  main_story['urls']=url
  topStory['main_story']=main_story
  ####
  ####
  sub_stories_list=[]

  for i in soup.find_all('div','topStory_multyImgBox'):
    sub_story={}
    url={}
    text={}

    subStory_img=i.find('a','img_only_hover')
    url['article_img_href']= subStory_img.img['data-src']
    url['article_href']=subStory_img['href']
    substoryCategory= i.find('a','catTag_hover')
    if(substoryCategory is None):
      url['category_href']=""
      text['category']=""
    else:
      url['category_href']=substoryCategory['href']
      text['category']=translate_text(substoryCategory.span.text)
    substoryPara= i.find('a','para_text_hover_1')
    text['para_text']=translate_text(substoryPara.text)
    sub_story['urls']=url
    sub_story['texts']=text
    sub_stories_list.append(sub_story)

  topStory['sub_stories']=sub_stories_list
  level1['top_story']=topStory
  

def level1_brewing():
  Brewing_data={}
  BrewingTitleSoup= soup.find('div','brewing_right_sec')
  BrewingTitle=BrewingTitleSoup.find('a','main_title_hover_1')
  Brewing_data['section_title']=headings[language]['whats_brewing']
  Brewing_data['section_href']=BrewingTitle['href']

  brewing_articles_list=[]

  for i in soup.find_all('div','brewing_dataBox'):
    brew_box={}
    url={}
    text={}
    brewing_img=i.find('a','img_only_hover')
    url['article_img_href']=brewing_img.img['data-src']
    url['article_href']=brewing_img['href']
    brewing_detail=i.find('div','brewing_detail')
    text['para_text']=translate_text(brewing_detail.h3.text)
    brew_box['urls']=url
    brew_box['texts']=text
    brewing_articles_list.append(brew_box)
  Brewing_data['brewing_articles']=brewing_articles_list
  level1["whats_brewing"]=Brewing_data

def level_1():
  level1_topstories()
  level1_brewing()
  return level1

def level_2():
    l2=[]
    l2_dict={}
    l2_div_tag=soup.find('div',id="level_2")
    list_group=l2_div_tag.find_all('li',class_='list-group-item')
    for list in list_group:
        data={}
        data['urls']={}
        data['texts']={}

        data['urls']['article_href']=(list.find('a',class_='img_only_hover'))['href']
        data['urls']['article_img_href']= (list.find('img'))['data-src']
        data['urls']['category_href']=((list.find('a',class_='catTag_hover category_tag dflex-inline without_icon'))['href'])
        data['texts']['title']=translate_text(list.find('a',class_='img_with_text_hover').text)
        data['texts']['category']=translate_text(list.find('a',class_='catTag_hover category_tag dflex-inline without_icon').text)

        l2.append(data)
    l2_dict["level2"]=l2
    return l2_dict

def level_3():
    l3_dict={}
    l3_div_tag=soup.find('div',id='level_3')
    # l3['section_title']=(l3_div_tag.find('h1')).text
    l3=[]
    div_group=l3_div_tag.find_all('div',class_='col-xl-4 col-lg-4 col-md-12 col-sm-12 col-12 px-2')
    for div in div_group:
        data={}
        data['urls']={}
        data['texts']={}
        data['urls']['article_href']=((div.find('a',class_='img_only_hover'))['href'])
        data['urls']['article_img_href']=((div.find('img'))['data-src'])
        data['texts']['para_text']=translate_text(div.find('a',class_='para_text_hover_1').text)
        l3.append(data)
    l3_dict["level3"]=l3
    return l3_dict

def level_5():
  l5={}
  l5_div_tag=soup.find('div',id='level_5')
  l5['section_title']=headings[language]['state_of_the_nation']
  l5['section_href']=((l5_div_tag.find('a',class_='main_title_hover_1'))['href'])
  l5['categories']={}
  cate={}
  nav_list_group=l5_div_tag.find_all('li',class_='nav-item')
  son_articles=l5_div_tag.find_all('div',class_='col-xl-3 col-lg-6 col-md-6 col-sm-12 col-12 mb-3')
  for nav_list in nav_list_group:
    cate[translate_text(nav_list.text)]=[]
  cate['All']=[]
  for article in son_articles:
    data={}
    data['urls']={}
    data['texts']={}
    data['urls']['article_img_href']=((article.find('img',class_='img-fluid'))['data-src'])
    data['urls']['article_href']=((article.find('a',class_='img_only_hover'))['href'])
    data['texts']['title']=translate_text(article.find('a',class_='img_para_text_hover').text)
    data['texts']['date_time']=translate_text(article.find('a',class_='img_dateTime_hover').text)
    cate['All'].append(data)
  l5['categories']=cate
  return l5
def level_6():
  Opinion_data={}
  Opinion_data['urls'] = {}
  Op_Cards=[]
  for opBox in soup.find_all('div','opinionPlay_multyImgBox'):
    op_card={}
    url={}
    text={}

    url['author_img_href']=(opBox.find('img')['src'])
    text['author_name']=translate_text(opBox.find('a','full_divBox_hover_1')['aria-label'])
    url['author_profile_href']=(opBox.find('a','full_divBox_hover_1')['href'])
    optext_sec=opBox.find('div','op_text_detail')
    url['article_href']=(optext_sec.find('a')['href'])
    text['opinion_text']=translate_text(optext_sec.find('a')['aria-label'])
    op_card['urls']=url
    op_card['texts']=text
    Op_Cards.append(op_card)
  # Opinion_data['Opinions']=Op_Cards
  Opinion_data['urls']['opinions_img_href'] = url_for('static', filename=f'images/opinion/{language}.png')
  Opinion_data['urls']['opinions_page_href'] = '/category/opinion'
  Opinion_data['opinions'] = Op_Cards
  return Opinion_data

def faultlines():
  fault_lines={}
  fault_lines['section_title']=headings[language]['fault_lines']
  fault_lines['section_href']='/faultlines'
  
  url={}
  fault_article=soup.find('div',id='fault_line_home')
  img_link=(fault_article.find('a','img_only_hover'))
  url['img_href']=img_link
  fault_lines['urls']=url
  fault_lines['urls']['img_href']=""
  level7['fault_lines']=fault_lines

def two_bit():
  twoBit={}
  twoBit['section_title']=headings[language]['two_bit']
  twoBit['section_href']='/twobit'
  
  url={}
  twoBit_article=soup.find('div',id='two_bit_home')
  img_link=(twoBit_article.find('a','img_only_hover'))
  url['img_href']=img_link
  twoBit['urls']=url
  twoBit['urls']['img_href']=""
  
  level7['two_bit']=twoBit

def eight_column():
    eight_col={}
    eight_column=soup.find('div',class_='eightColum_sec')
    eight_col['section_title']=headings[language]['the_eighth_column']
    eight_col['section_href']=eight_column.find('a',class_='eight_column_tittle_hover')['href']
    eight_col['urls']={}
    eight_col['texts']={}
    symbol_eight_link=(eight_column.find('a',class_='eight_column_tittle_hover'))['href']
    symbol_eight_source=(eight_column.find('img',class_='img-fluid pre_reverce_icon_size'))['src']

    eight_col['urls']['article_href']=(eight_column.find('a',class_='sub_title_hover_2')['href'])
    eight_col['texts']['title']=translate_text(eight_column.find('a',class_='sub_title_hover_2').text)
    eight_col['texts']['para_text']=translate_text(eight_column.find('a',class_='para_text_hover_2').text)
    eight_author_span=eight_column.find('span',class_='para_text_5 font22 font_normal mb_30 d-xl-block d-lg-block d-md-block d-none')
    eight_col['urls']['author_profile_href']=(eight_author_span.find('a',class_='para_text_hover_2')['href'])
    eight_col['texts']['author_name']=translate_text(eight_author_span.find('a',class_='para_text_hover_2').text)
    eight_image=eight_column.find('div',class_='eightColum_imgBox')
    eight_col['urls']['article_img_href']=eight_image.find('img',class_='img-fluid')['data-src']
    
    level7['eight_column']=eight_col
    
def level_7():
  faultlines()
  two_bit()
  eight_column()
  return level7

def level_8():
  Carousel_cards_data={}
  a=1
  for i in soup.find_all('div','event_card_carousel_divBox'):
    carousel_cards_list=[]
    if(a%2==1):
      for j in i.find_all('a','main_title_hover_1'):
        carousel_title=j['aria-label']
        Carousel_cards_data[carousel_title] = {}
        Carousel_cards_data[carousel_title]['section_href']=j['href']
        Carousel_cards_data[carousel_title]['section_title']=translate_text(carousel_title)

      cc=1
      for j in i.find_all('div','card_dataBox'):
        carousel_card={}
        url={}
        text={}
        for k in j.find_all('a','img_only_hover'):
          url['article_href']=(k['href'])
          url['article_img_href']=(k.img['data-src'])

        for k in j.find_all('a','para_text_hover_1'):
          text['para_text']=translate_text(k['aria-label'])
        carousel_card={}
        carousel_card['urls']=url
        carousel_card['texts']=text
        carousel_cards_list.append(carousel_card)
      Carousel_cards_data[carousel_title]['articles']=carousel_cards_list
    a+=1
  return Carousel_cards_data

def level_9():
  videoPlaylist_data={}
  section_title="THE FEDERAL PLAYLIST"

  videos_list=[]
  for dataBox in soup.find_all('div','federal_playlist_dataBox'):
    video={}
    url={}
    text={}
    date_time={}
    image_sec=dataBox.find('a','img_only_hover')
    url['article_href']=(image_sec['href'])
    url['article_img_href']=(image_sec.img['data-src'])
    text_sec=dataBox.find('a','para_text_2')
    text['para_text']=translate_text(text_sec['aria-label'])
    time_sec=dataBox.find('p','video-playlist-date-time')
    video['urls']=url
    video['texts']=text
    video['date_time']=translate_text(time_sec.text)
    videos_list.append(video)
    videoPlaylist_data["section_title"]=translate_text(section_title)
    videoPlaylist_data["section_href"]="/category/videos"
    videoPlaylist_data["section_para_text"]=translate_text("more videos")
    videoPlaylist_data["videos"]=videos_list

  return videoPlaylist_data

def nav_hover():
  menuSoup=soup.find('div','mega_menu_navbar_sec')
  hoverData={}
  for i in menuSoup.find_all('li','hover_mengamenu'):
    hoverTag={}
    nav_item_name=translate_text(i.find('a','dropdown-toggle nav-link').text)
    nav_item_href=i.find('a','dropdown-toggle nav-link')['href']
    hoverTag["nav_title"]=nav_item_name
    hoverTag["nav_href"]=nav_item_href
    hoverTag["rows"]=[]
    subMenuSoup=i.find('div','mega_subMenu_wrapper')
    for j in subMenuSoup.find_all('li','col-md-2 dropdown-item'):
      row={}
      row['urls']=[]
      row['texts']=[]
      for k in j.find_all('a'):
        row['urls'].append(k['href'])
        row['texts'].append(translate_text(k.text))
      hoverTag["rows"].append(row)
    hoverData[nav_item_name]=hoverTag
  return hoverData

def get_homepage_data(level,lang):
    global language 
    language = lang

    if level == '1':
      return level_1()
    elif level == '2':
      return level_2()
    elif level == '3':
      return level_3()
    elif level == '5':
      return level_5()
    elif level == '6':
      return level_6()
    elif level == '7':
      return level_7()
    elif level == '8':
      return level_8()
    elif level == '9':
      return level_9()
    
    # json_data = json.dumps(data_to_be_fed)
    # with open('data.json', 'w') as json_file:
    #     json_file.write(json_data)
# print(get_homepage_data('2','en'))