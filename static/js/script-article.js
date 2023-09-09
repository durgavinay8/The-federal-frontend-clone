let dataToBeRendered;

//Fetching the data to be rendered when the html is loaded
document.addEventListener("DOMContentLoaded", ()=>{
  changeLanguage("null");
});

const getLanguageFromCookie = async()=>{
  return document.cookie
  .split("; ")
  .find((row) => row.startsWith("language="))
  ?.split("=")[1];
};
const changeLanguage = async(langToBeSet)=>{
  console.log("inside")
  const language = await getLanguageFromCookie();
  if(langToBeSet!="null" && langToBeSet === language ){
    return
  }
  if(language === "null"){
    langToBeSet = "en";
  }
  else if(langToBeSet != "null"){
    document.cookie = `language=${langToBeSet}`;
    window.location.reload();
  }
};

const renderHeaderSection = async(header_Data)=>{
  const header = document.getElementById('header-tag');
  //update logo
  header.querySelector('.the-federal-logo').src = header_Data.urls.company_logo;
  let premium_access_btn = header.querySelector('.premium_access_btn');
  premium_access_btn.href = header_Data.urls.premium_href;
  premium_access_btn.querySelector('img').src = header_Data.urls.premium_icon_href;
  premium_access_btn.querySelector('span').innerText = header_Data.texts.premium_normal;
  let reg_login_btn = header.querySelector('.reg_login_btn');
  reg_login_btn.href = header_Data.urls.login_href;
  reg_login_btn.querySelector('span').innerText = header_Data.texts.register;
  header.querySelector('input').placeholder = header_Data.texts.search_placeholder;
  //mega-menu
  let mega_menu_ul = header.querySelector('#mega-menu');
  mega_menu_ul.innerHTML = '<li class="hamburger"><i class="fa-solid fa-bars"></i></li>';
  for(each_menu in header_Data.menu.urls){
    let li_tag = document.createElement('li');
    li_tag.innerHTML = `<a href="${header_Data.menu.urls[each_menu]}">${header_Data.menu.texts[each_menu]}</a>`;
    mega_menu_ul.appendChild(li_tag);
  }
}

const renderFooterSection = async(footer_data)=>{
    let footer_tag = document.querySelector('footer');
    footer_tag.querySelector('.logo-img').src = footer_data.urls.company_img_reverse_href;
    footer_tag.querySelector('.company-description').innerText = footer_data.texts.company_desc;
    let social_media_tags = footer_tag.querySelectorAll('.social-media-links a');
    let index=0;
    for(social_media  of footer_data.social_media_links){
      social_media_tags[index++].href = social_media;
    }
    let company_links_ul = footer_tag.querySelector('.company-links-list');
    for(x in footer_data.company_links.urls){
      let li_tag = document.createElement('li');
      li_tag.innerHTML = `<a href="${footer_data.company_links.urls[x]}">${footer_data.company_links.texts[x]}</a>`;
      company_links_ul.appendChild(li_tag);
    }
    footer_tag.querySelector('.subscribe-container p').innerText = footer_data.texts.subscribe_desc;
    footer_tag.querySelector('.subscribe-container span').innerText = footer_data.texts.subscribe_text;
    let category_links_ul = footer_tag.querySelector('.category-links-list');
    category_links_ul.innerHTML = `<p>${footer_data.quick_links.texts.section_title}</p>`;
    for(x in footer_data.quick_links.urls){
      let li_tag = document.createElement('li');
      li_tag.innerHTML = `<a href="${footer_data.quick_links.urls[x]}">${footer_data.quick_links.texts[x]}</a>`;
      category_links_ul.appendChild(li_tag);
    }
    footer_tag.querySelector('.premium-access-img').src = footer_data.urls.premium_access_img_href;
    footer_tag.querySelector('.footer-bottom').innerText = footer_data.texts.copyright;
}