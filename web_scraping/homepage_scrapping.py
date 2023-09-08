import requests
import json
from googletrans import Translator
from bs4 import BeautifulSoup

url=f'https://thefederal.com/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.content,"html.parser")
######
language = ""
data_to_be_fed={}
level1={}
translator = Translator()
def tran(text):
  if language == "en":
      return text
  for i in range(3):
    try:
        return translator.translate(text, dest=language).text
    except:
        print("Translation request timed out. Retrying...")
        continue
  # a lot to-do
  raise Exception("Translation request failed after multiple retries")

def level1_topstories():

  topStory_soup=soup.find('div','topStory_dataBox')
  topStory_title=topStory_soup.find('a','main_title_hover_1')
  topStory={}
  topStory['section_title']=tran(topStory_title.text)
  topStory['section_href']=topStory_title['href']
  main_story={}
  url={}
  texts={}
  topStory_subtitle=topStory_soup.find('a','sub_title_hover_1')
  texts['title']=tran(topStory_subtitle.text)
  url['article_href']=topStory_subtitle['href']
  topStory_para=topStory_soup.find('a','para_text_hover_1')
  texts['para_text']=tran(topStory_para.text)

  topStory_img_soup= soup.find('div','topStory_imgBox')
  topStory_img=topStory_img_soup.find('a','img_only_hover')
  url['article_img_href']=topStory_img.img['data-src']
  topStory_category= topStory_img_soup.find('a','catTag_hover')

  texts['category']=tran(topStory_category.span.text)
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
      text['category']=tran(substoryCategory.span.text)
    substoryPara= i.find('a','para_text_hover_1')
    text['para_text']=tran(substoryPara.text)
    sub_story['urls']=url
    sub_story['texts']=text
    sub_stories_list.append(sub_story)

  topStory['sub_stories']=sub_stories_list
  level1['top_story']=topStory

def level1_brewing():
  Brewing_data={}
  BrewingTitleSoup= soup.find('div','brewing_right_sec')
  BrewingTitle=BrewingTitleSoup.find('a','main_title_hover_1')
  Brewing_data['section_title']=tran(BrewingTitle.text)
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
    text['para_text']=tran(brewing_detail.h3.text)
    brew_box['urls']=url
    brew_box['texts']=text
    brewing_articles_list.append(brew_box)
  Brewing_data['brewing_articles']=brewing_articles_list
  level1["whats_brewing"]=Brewing_data

def level_1():
  level1_topstories()
  level1_brewing()
  data_to_be_fed['level_1']=level1

def level_2():
    l2=[]

    l2_div_tag=soup.find('div',id="level_2")
    list_group=l2_div_tag.find_all('li',class_='list-group-item')
    for list in list_group:
        data={}
        data['urls']={}
        data['texts']={}

        data['urls']['article_href']=(list.find('a',class_='img_only_hover'))['href']
        data['urls']['article_img_href']= (list.find('img'))['data-src']
        data['urls']['category_href']=((list.find('a',class_='catTag_hover category_tag dflex-inline without_icon'))['href'])
        data['texts']['title']=tran(list.find('a',class_='img_with_text_hover').text)
        data['texts']['category']=tran(list.find('a',class_='catTag_hover category_tag dflex-inline without_icon').text)

        l2.append(data)
    data_to_be_fed['level_2']=l2

def level_3():
    l3={}
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
        data['texts']['para_text']=tran(div.find('a',class_='para_text_hover_1').text)
        l3.append(data)
    data_to_be_fed['level_3']=l3

def level_5():
    l5={}

    l5_div_tag=soup.find('div',id='level_5')
    l5['section_title']=tran((l5_div_tag.find('a',class_='main_title_hover_1')).text)
    l5['section_href']=((l5_div_tag.find('a',class_='main_title_hover_1'))['href'])
    l5['categories']={}
    cate={}
    nav_list_group=l5_div_tag.find_all('li',class_='nav-item')
    son_articles=l5_div_tag.find_all('div',class_='col-xl-3 col-lg-6 col-md-6 col-sm-12 col-12 mb-3')
    for nav_list in nav_list_group:
        cate[(nav_list.text)]=[]
    
    for article in son_articles:
        data={}
        data['urls']={}
        data['texts']={}
        data['urls']['article_img_href']=((article.find('img',class_='img-fluid'))['data-src'])
        data['urls']['article_href']=((article.find('a',class_='img_only_hover'))['href'])
        data['texts']['title']=tran(article.find('a',class_='img_para_text_hover').text)
        data['texts']['date_time']=((article.find('a',class_='img_dateTime_hover')).text)
        cate['All'].append(data)
    l5['categories']=cate
    data_to_be_fed['level_5']=l5
def level_6():
  Opinion_data={}
 
  Op_Cards=[]
  for opBox in soup.find_all('div','opinionPlay_multyImgBox'):
    op_card={}
    url={}
    text={}

    url['author_img_href']=(opBox.find('img')['src'])
    text['author_name']=tran(opBox.find('a','full_divBox_hover_1')['aria-label'])
    url['author_profile_href']=(opBox.find('a','full_divBox_hover_1')['href'])
    optext_sec=opBox.find('div','op_text_detail')
    url['article_href']=(optext_sec.find('a')['href'])
    text['opinion_text']=tran(optext_sec.find('a')['aria-label'])
    op_card['urls']=url
    op_card['texts']=text
    Op_Cards.append(op_card)
  # Opinion_data['Opinions']=Op_Cards

  data_to_be_fed['level_6']=Op_Cards

def faultlines():
  fault_lines={}
  fault_lines['section_title']='faultlines'
  fault_lines['section_href']='/faultlines'
  
  url={}
  fault_article=soup.find('div',id='fault_line_home')
  img_link=(fault_article.find('a','img_only_hover'))
  url['img_href']=img_link
  fault_lines['urls']=url
  fault_lines['urls']['img_href']=""
  data_to_be_fed['level_7']['fault_lines']=fault_lines

def two_bit():
  twoBit={}
  twoBit['section_title']='two-bit'
  twoBit['section_href']='/twobit'
  
  url={}
  twoBit_article=soup.find('div',id='two_bit_home')
  img_link=(twoBit_article.find('a','img_only_hover'))
  url['img_href']=img_link
  twoBit['urls']=url
  twoBit['urls']['img_href']=""
  
  data_to_be_fed['level_7']['two_bit']=twoBit

def eight_column():
    eight_col={}
    eight_column=soup.find('div',class_='eightColum_sec')
    eight_col['section_title']=eight_column.find('h2',class_='title_2').get_text(' ')
    eight_col['section_href']=eight_column.find('a',class_='eight_column_tittle_hover')['href']
    eight_col['urls']={}
    eight_col['texts']={}
    symbol_eight_link=(eight_column.find('a',class_='eight_column_tittle_hover'))['href']
    symbol_eight_source=(eight_column.find('img',class_='img-fluid pre_reverce_icon_size'))['src']

    eight_col['urls']['article_href']=(eight_column.find('a',class_='sub_title_hover_2')['href'])
    eight_col['texts']['title']=tran(eight_column.find('a',class_='sub_title_hover_2').text)
    eight_col['texts']['para_text']=tran(eight_column.find('a',class_='para_text_hover_2').text)
    eight_author_span=eight_column.find('span',class_='para_text_5 font22 font_normal mb_30 d-xl-block d-lg-block d-md-block d-none')
    eight_col['urls']['author_profile_href']=(eight_author_span.find('a',class_='para_text_hover_2')['href'])
    eight_col['texts']['author_name']=tran(eight_author_span.find('a',class_='para_text_hover_2').text)
    eight_image=eight_column.find('div',class_='eightColum_imgBox')
    eight_col['urls']['article_img_href']=eight_image.find('img',class_='img-fluid')['data-src']
    
    data_to_be_fed['level_7']['eight_column']=eight_col
    
def level_7():
  data_to_be_fed["level_7"]={}
  faultlines()
  two_bit()
  eight_column()

def level_8():
  Carousel_cards_data={}

  a=1
  for i in soup.find_all('div','event_card_carousel_divBox'):
    carousel_cards_list=[]
    if(a%2==1):
      for j in i.find_all('a','main_title_hover_1'):
          carousel_title=j['aria-label']
      cc=1
      for j in i.find_all('div','card_dataBox'):
        carousel_card={}
        url={}
        text={}
        for k in j.find_all('a','img_only_hover'):
          url['article_href']=(k['href'])
          url['article_img_href']=(k.img['data-src'])

        for k in j.find_all('a','para_text_hover_1'):
          text['para_text']=tran(k['aria-label'])
        carousel_card={}
        carousel_card['urls']=url
        carousel_card['texts']=text
        carousel_cards_list.append(carousel_card)
      Carousel_cards_data[carousel_title]=carousel_cards_list
    a+=1
  data_to_be_fed['level_8']=(Carousel_cards_data)

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
    text['para_text']=tran(text_sec['aria-label'])
    time_sec=dataBox.find('p','video-playlist-date-time')
    video['urls']=url
    video['texts']=text
    video['date_time']=tran(time_sec.text)
    videos_list.append(video)
    videoPlaylist_data["section_title"]=tran(section_title)
    videoPlaylist_data["section_href"]="/category/videos"
    videoPlaylist_data["section_para_text"]=tran("more videos")
    videoPlaylist_data["videos"]=videos_list

  data_to_be_fed["level_9"]=videoPlaylist_data

def nav_hover():
  menuSoup=soup.find('div','mega_menu_navbar_sec')
  hoverData={}
  for i in menuSoup.find_all('li','hover_mengamenu'):
    hoverTag={}
    nav_item_name=i.find('a','dropdown-toggle nav-link').text
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
        row['texts'].append(tran(k.text))
      hoverTag["rows"].append(row)
    hoverData[nav_item_name]=hoverTag
  data_to_be_fed["cateogory_hover"]=hoverData

def get_homepage_data(lang):
    global language 
    language = lang

    level_1()
    level_2()
    level_3()
    level_5()
    level_6()
    level_7()
    level_8()
    level_9()

    # json_data = json.dumps(data_to_be_fed)
    # with open('data.json', 'w') as json_file:
    #     json_file.write(json_data)
    return data_to_be_fed
