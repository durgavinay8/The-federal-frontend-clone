from flask import  url_for
import json
from googletrans import Translator

language = ""

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

header_json = {
  "urls":{
    "company_logo" : "",
    "premium_icon_href": "https://thefederal.com/theme_flamingo/images/icon_header_premium.png",
    "premium_href": "/pricing",
    "register_href": "/login",
    "menu":{
      "home": "/",
      "news": "/category/news/",
      "analysis": "/category/analysis",
      "state": "/category/states/",
      "perspective": "/category/opinion/",
      "videos": "/category/videos/",
      "entertainment": "/category/entertainment/",
      "sports": "/category/sports/",
      "features": "/category/features/",
      "business": "/category/business/",
      "premium": "/category/the-eighth-column/"
    }
  },
  "texts":{
    "premium_normal" : "Premium Access",
    "premium_on_hover" : "Only ₹599/year",
    "register": "Register / Login",
    "search_placeholder": "Search Website",
    "menu":{
      "home": "home",
      "news": "news",
      "analysis": "analysis",
      "state": "state",
      "perspective": "perspective",
      "videos": "videos",
      "entertainment": "entertainment",
      "sports": "sports",
      "features": "features",
      "business": "business",
      "premium": "premium"
    }
  }
}

footer_json = {
    "urls":{
      "company_img_reverse_href": "",
      "premium_access_img_href": ""
    },
    "texts":{
      "company_desc": "The Federal is a digital platform disseminating news, analysis and commentary. It seeks to look at India from the perspective of the states with special focus on the south.",
      "subscribe_desc":"Get news delivered to your in-box. Subscribe to our newsletter.",
      "subscribe_text":"Subscribe",
      "copyright": "© 2023 THE FEDERAL. ALL RIGHTS RESERVED. All Images, Videos and content are proprietary to Federal."
    },
    "social_media_links": [
      "https://www.instagram.com/thefederal_india/reels/",
      "https://www.facebook.com/TheFederal.India",
      "https://twitter.com/i/flow/login?redirect_after_login=/TheFederal_IN",
      "https://www.linkedin.com/company/thefederal?originalSubdomain=in",
      "https://www.youtube.com/channel/UCY0hLvZl90ALbeaUMjKlsyw"
    ],
    "company_links":{
      "urls": {
        "about_us": "/about-us",
        "contact_us": "/contact-us",
        "careers": "/careers",
        "premium_access": "/pricing",
        "terms_of_use": "/terms",
        "privacy_policy": "/privacy-policy"
      },
      "texts":{
        "about_us": "About us",
        "contact_us": "Contact us",
        "careers": "Careers",
        "premium_access": "Premium Access Subscription",
        "terms_of_use": "Terms of Use",
        "privacy_policy": "Privacy Policy"
      }
    },
    "quick_links":{
      "section_title" : "quick links",
      "urls":{
        "news": "/category/news/",
        "analysis": "/category/analysis",
        "states": "/category/states/",
        "perspective": "/category/opinion/",
        "videos": "/category/videos/",
        "entertainment": "/category/entertainment/",
        "sports": "/category/sports/",
        "features": "/category/features",
        "business": "/category/business",
        "premium": "/category/the-eighth-column/",
        "brand_studio": "/brand-studio"
      },
      "texts":{
        "news": "News",
        "analysis": "Analysis",
        "states": "States",
        "perspective": "Perspective",
        "videos": "Videos",
        "entertainment": "Entertainment",
        "sports": "Sports",
        "features": "Features",
        "business": "Business",
        "premium": "Premium",
        "brand_studio": "Brand Studio"
      }
    }
}

def update_texts(json_data):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == "texts" and isinstance(value, dict):
                for text_key, text_value in value.items():
                    # if isinstance(text_value, list): 
                    #   pass
                    if isinstance(text_value, dict):
                      for subkey, subvalue in text_value.items():
                          json_data["texts"][text_key][subkey] = tran(subvalue)
                    else:
                      json_data[key][text_key] = tran(text_value)
                break
            else:
                update_texts(value)
    elif isinstance(json_data, list):
        for i, item in enumerate(json_data):
            json_data[i] = update_texts(item)
    return json_data 


def get_header_footer_jsons(lang):
   global language
   language = lang
   
   if lang == "en":
    updated_header_json = header_json
    updated_footer_json = footer_json
   else:
    updated_header_json = update_texts(header_json)
    updated_footer_json = update_texts(footer_json)

   updated_header_json["urls"]["company_logo"] = url_for('static', filename=f'images/logo/{lang}.png')
   updated_footer_json["urls"]["company_img_reverse_href"] = url_for('static', filename=f'images/logo_reverse/{lang}.png')
   updated_footer_json["urls"]["premium_access_img_href"] = url_for('static', filename=f'images/premium_access_card/{lang}.png')

   return [updated_header_json, updated_footer_json]
