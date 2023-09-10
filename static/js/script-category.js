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

const renderMainSection = async(main_section)=>{
  //breadcrumbs
  let breadcrumb_cont = document.getElementById('breadcrumb-wrapper');
  const breadcrumb_template = document.getElementById('breadcrumb-item-template'),
    breadcrumb_urls = main_section['urls']['breadcrumb_items'],
    breadcrumb_texts = main_section['texts']['breadcrumb_items'];
  breadcrumb_urls.forEach((breadcrumb_url, index) => {
    let clone = breadcrumb_template.content.cloneNode(true);
    clone.querySelector('a').href = breadcrumb_url;
    clone.querySelector('a').innerText = breadcrumb_texts[index];
    breadcrumb_cont.appendChild(clone);
  });
  //category title
  document.getElementById('category-text').innerText = main_section.texts.section_title
  //level-1
  renderLevel1(main_section['level_1']);
  //divider
  let divider = document.getElementById('l1-l2-divider');
  divider.querySelector('hr').className = '';
  const subcategory_cont = divider.querySelector('#subcategory-list'),
    subcategory_urls = main_section['urls']['sub_categories'],
    subcategory_texts = main_section['texts']['sub_categories'];
  subcategory_urls.forEach((subcategory_url, index) => {
    let a_tag = document.createElement('a');
    a_tag.href = subcategory_url;
    a_tag.innerText = subcategory_texts[index];
    subcategory_cont.appendChild(a_tag);
  });
  //level-2
  renderLevel2(main_section['level_2']);
  prev_next_pages = document.getElementById('pagination').children;
  if(main_section['urls'].hasOwnProperty('prev_page')){
      prev_next_pages[0].href = main_section['urls']['prev_page'];
      prev_next_pages[0].innerText = main_section['texts']['prev_page'];
  }else{
      prev_next_pages[0].classList = 'hide';
  }
  prev_next_pages[1].href = main_section['urls']['next_page'];
  prev_next_pages[1].innerText = main_section['texts']['next_page'];
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
  

const renderLevel1= async(level1_Data)=>{    
  let top_story_a_tags =  document.getElementById('top-story').getElementsByTagName('a');

  top_story_a_tags[0].innerText = level1_Data.main_story.texts.article_title;
  top_story_a_tags[1].innerText = level1_Data.main_story.texts.author;
  top_story_a_tags[1].href = level1_Data.main_story.urls.author_href;
  top_story_a_tags[2].innerText = level1_Data.main_story.texts.date_time;
  top_story_a_tags[3].innerText = level1_Data.main_story.texts.short_desc;
  top_story_a_tags[4].querySelector('img').src = level1_Data.main_story.urls.article_img_href;
  //top-story-category
  top_story_a_tags[5].innerText = level1_Data.main_story.texts.category;
  top_story_a_tags[5].href = level1_Data.main_story.urls.category_href;
  top_story_a_tags[0].href = top_story_a_tags[3].href = top_story_a_tags[4].href = level1_Data.main_story.urls.article_href;
  //sub-top-stories
  const sub_top_stories_container = document.getElementById('sub-top-stories-row');
  const substory_card_template = document.getElementById("sub-story-card-template");

  sub_top_stories_container.innerHTML = '';
  for(sub_story of level1_Data.sub_stories){
    let substory_card_clone = substory_card_template.content.cloneNode(true);
    let substory_card_a_tags = substory_card_clone.querySelectorAll('a'); 
    substory_card_a_tags[0].href = substory_card_a_tags[2].href = sub_story.urls.article_href;
    substory_card_a_tags[0].querySelector('img').src = sub_story.urls.article_img_href;
    substory_card_a_tags[1].href = sub_story.urls.category_href;
    substory_card_a_tags[1].innerText = sub_story.texts.category;
    substory_card_a_tags[2].innerText = sub_story.texts.title;
    substory_card_a_tags[3].innerText = sub_story.texts.date_time;

    sub_top_stories_container.appendChild(substory_card_clone);
  }
}

const renderLevel2 = async(level2_Data)=>{
  const l2_cont = document.getElementById('level-2');
  l2_cont.innerHTML = '';
  let sub_cont, index = 0, main_story_bool = level2_Data.hasOwnProperty('main_story');
  const sub_card_template = document.getElementById('l2_subcard_template');
  for(article of level2_Data['sub_stories']){
    if(index%4 == 0){
      sub_cont = document.createElement('div');
      if(main_story_bool && index==8){
        let div_tag = document.createElement('div');
        div_tag.className = 'flex-row';
        div_tag.id = 'l2_main_story_row';

        const main_card_template = document.getElementById('l2_maincard_template');
        let card_clone = main_card_template.content.cloneNode(true);
        sub_cont.className = 'articles-row flex-row flex-wrap';
        let child_tags = card_clone.querySelector('#l2_maincard').children;
        child_tags[0].href = child_tags[3].href = level2_Data.main_story.urls.article_href;                
        child_tags[0].querySelector('img').src = level2_Data.main_story.urls.article_img_href;
        child_tags[0].querySelector('p').innerText = level2_Data.main_story.texts.title;
        child_tags[1].innerText = level2_Data.main_story.texts.author;
        child_tags[1].href = level2_Data.main_story.urls.author_href;
        child_tags[2].innerText = level2_Data.main_story.texts.date_time;
        child_tags[3].querySelector('p').innerText = level2_Data.main_story.texts.para_text;
        div_tag.appendChild(card_clone);
        div_tag.appendChild(sub_cont);
        l2_cont.appendChild(div_tag);
      }else{
        sub_cont.className = 'articles-row flex-row ';
        l2_cont.appendChild(sub_cont);
      }
    }
    let card_clone = sub_card_template.content.cloneNode(true);
    let a_tag = card_clone.getElementById('l2_subcard');
    a_tag.href = article.urls.article_href;
    a_tag.querySelector('img').src = article.urls.article_img_href;
    a_tag.querySelector('p').innerText = article.texts.title;
    a_tag.querySelector('span').innerText = article.texts.date_time;

    sub_cont.appendChild(card_clone);
    index++;
  }
}

