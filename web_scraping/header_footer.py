from flask import  url_for
import json
from googletrans import Translator

language = ""

translator = Translator()
def translate_text(text):
  if language == "en":
    return text
  for i in range(3):
    try:
      return translator.translate(text, dest=language).text
    except Exception as error:
      print("Translation request timed out. Retrying...",error)
      continue
  # a lot to-do
  raise Exception("Translation request failed after multiple retries")

header_json = {
  "urls":{
    "company_logo" : "",
    "premium_icon_href": "https://thefederal.com/theme_flamingo/images/icon_header_premium.png",
    "premium_href": "/pricing",
    "register_href": "/login",
  },
  "texts":{
    "premium_normal" : "Premium Access",
    "premium_on_hover" : "Only ₹599/year",
    "register": "Register / Login",
    "search_placeholder": "Search Website",
  },
  "menu":{
     "urls":{
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
    },
     "texts":{
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
        "section_title" : "quick links",
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

def update_texts(data):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if key == "texts" and isinstance(value, dict):
                new_data[key] = {k: translate_text(v) for k, v in value.items()}
            else:
                new_data[key] = update_texts(value)
        return new_data
    elif isinstance(data, list):
        return [update_texts(item) for item in data]
    else:
        return data

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
