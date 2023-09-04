let dataToBeRendered;

//Fetching the data to be rendered when the html is loaded
document.addEventListener("DOMContentLoaded", ()=>{
  console.log("DOMContentLoaded");
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
    console.log("inside")
    langToBeSet = "en";
  }
  if(langToBeSet === "null"){
    console.log("inside")
    langToBeSet = language;
  }
  console.log("prevlanguage : ",typeof language,language,"& langToBeSet : ",typeof langToBeSet, langToBeSet);
  document.cookie = `language=${langToBeSet}`;
  renderPage(langToBeSet)
};

const fetchHomepageData = async(language)=>{
  try{
    const response = await fetch(`api/homepage/${language}`)
    if(!response.ok){
      throw new Error('Network response was not ok');
    }
    return await response.json();
  }catch(err){
    alert("Error Fetching Data")
    console.error("error fetching data\n",err);
  }
};

const renderPage = async(language)=>{
  try{
    console.log("renderPage");
    const dataToBeRendered = await fetchHomepageData(language);
    renderHeaderSection(dataToBeRendered['header']);
    renderMainSection(dataToBeRendered['main']);
    renderFooterSection(dataToBeRendered['footer']);
  }catch(err){
    console.error('Error: ', err);
  }
}

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
  mega_menu_ul.innerHTML = '';
  for(each_menu in header_Data.urls.menu){
    let li_tag = document.createElement('li');
    li_tag.innerHTML = `<a href="${header_Data.urls.menu[each_menu]}">${header_Data.texts.menu[each_menu]}</a>`;
    mega_menu_ul.appendChild(li_tag);
  }
}

const renderMainSection = async(main_section)=>{
  renderLevel1(main_section["level_1"]);
  renderLevel2(main_section["level_2"]);
  renderLevel3(main_section["level_3"]);
  renderLevel5(main_section["level_5"]);
  renderLevel6(main_section["level_6"]);
  renderLevel7(main_section["level_7"]);
  renderLevel8(main_section["level_8"]);
  renderLevel9(main_section["level_9"]);

  $(".level-2 .owl-carousel").owlCarousel({
      margin:16,
      nav : true,
      loop : true,
      navText: ['<span class="next">&lt;</span>','<span class="prev">&gt;</span>'],
      navContainer: '.level-2 .custom-nav',
      responsive:{
          0:{
              items:1
          },
          600:{
              items:3
          },
          1000:{
              items:4.5
          }
      }
  })
  $(".level-8 .owl-carousel").owlCarousel({
      nav : true,
      navText: ['<i class="fa-solid fa-caret-left"></i>','<i class="fa-solid fa-caret-right"></i>'],
      responsive:{
          1000:{
              items:1
          }
      }
  })
  $(".level-9 .owl-carousel").owlCarousel({
      margin:16,
      nav : true,
      navText: ['<span class="next">&lt;</span>','<span class="prev">&gt;</span>'],
      navContainer: '.level-9 .custom-nav',
      responsive:{
          0:{
              items:1
          },
          600:{
              items:3
          },
          1000:{
              items:4
          }
      }
  })
}

const renderFooterSection = async(footer_data)=>{
  let footer_tag = document.querySelector('footer');
  footer_tag.querySelector('.logo-img').src = footer_data.company_img_reverse;
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
  category_links_ul.innerHTML = `<p>${footer_data.quick_links.section_title}</p>`;
  for(x in footer_data.quick_links.urls){
    let li_tag = document.createElement('li');
    li_tag.innerHTML = `<a href="${footer_data.quick_links.urls[x]}">${footer_data.quick_links.texts[x]}</a>`;
    category_links_ul.appendChild(li_tag);
  }
  footer_tag.querySelector('.premium-access-img').src = footer_data.urls.premium_access_img_href;
  footer_tag.querySelector('.footer-bottom').innerText = footer_data.texts.copyright;
}

const renderLevel1= async(level1_Data)=>{    
  let main_story_a_tags =  document.getElementById('main-story').getElementsByTagName('a');
  //section title
  main_story_a_tags[0].innerText = level1_Data.top_story.section_title;
  main_story_a_tags[0].href = level1_Data.top_story.section_href;
  // main-story-card
  main_story_a_tags[1].href = main_story_a_tags[2].href = main_story_a_tags[3].href = level1_Data.top_story.main_story.urls.article_href;
  main_story_a_tags[1].innerText = level1_Data.top_story.main_story.texts.title;
  main_story_a_tags[2].innerText = level1_Data.top_story.main_story.texts.para_text;
  main_story_a_tags[3].querySelector('img').src = level1_Data.top_story.main_story.urls.article_img_href;
  //main-story-category
  main_story_a_tags[4].innerText = level1_Data.top_story.main_story.texts.category;
  main_story_a_tags[4].href = level1_Data.top_story.main_story.urls.category_href;

  //sub-top-stories
  const sub_top_stories_container = document.getElementById('sub-top-stories-row');
  const substory_card_template = document.getElementById("sub-story-card-template");
  print(substory_card_template)

  sub_top_stories_container.innerHTML = '';
  for(sub_story of level1_Data.top_story.sub_stories){
    let substory_card_clone = substory_card_template.content.cloneNode(true);
    let substory_card_a_tags = substory_card_clone.querySelectorAll('a'); 
    substory_card_a_tags[0].href = substory_card_a_tags[2].href = sub_story.urls.article_href;
    substory_card_a_tags[0].querySelector('img').src = sub_story.urls.article_img_href;
    substory_card_a_tags[1].href = sub_story.urls.category_href;
    substory_card_a_tags[1].innerText = sub_story.texts.category;
    substory_card_a_tags[2].innerText = sub_story.texts.para_text;

    sub_top_stories_container.appendChild(substory_card_clone);
    
  }
  sub_top_stories_container.getElementsByClassName('img-over_tag_btn')[2].insertAdjacentHTML("afterbegin", `<img src='https://thefederal.com/theme_flamingo/images/icon_header_premium.png' class="premium_icon>`);

  //what's brewing
  const whats_brewing_title = document.querySelector('#whats-brewing .main-heading');
  whats_brewing_title.href = level1_Data.whats_brewing.section_href;
  whats_brewing_title.innerHTML = level1_Data.whats_brewing.section_title;
  const brewing_card_cont = document.getElementById('brewing-cards-cont');
  const brewing_card_template = document.getElementById('brewing-card-template');
  brewing_card_cont.innerHTML = '';
  for(brewing_article of level1_Data.whats_brewing.brewing_articles){
    let brewing_card_clone = brewing_card_template.content.cloneNode(true);
    let brewing_card_a_tag = brewing_card_clone.querySelector('a'); 
    brewing_card_a_tag.href = brewing_article.urls.article_href;
    let brewing_card_img_p = brewing_card_a_tag.children; 
    brewing_card_img_p[0].src = brewing_article.urls.article_img_href;
    brewing_card_img_p[1].innerHTML = brewing_article.texts.para_text;

    brewing_card_cont.appendChild(brewing_card_clone);
  }
}

const renderLevel2 = async(level2_Data)=>{
  const carousel_cont = document.getElementById('level2-carousel-cont');
  const card_template = document.getElementById('level2-card-template');
  carousel_cont.innerHTML = '';
  for(story of level2_Data){
    let card_clone = card_template.content.cloneNode(true);
    let card_a_tags = card_clone.querySelectorAll('a'); 
    
    card_a_tags[0].href = story.urls.article_href;
    card_a_tags[0].querySelector('img').src = story.urls.article_img_href;
    card_a_tags[1].href = story.urls.category_href;
    card_a_tags[1].innerText = story.texts.category;
    card_a_tags[2].href = story.urls.article_href;
    card_a_tags[2].innerText = story.texts.title;
    
    carousel_cont.appendChild(card_clone);
  }
}

const renderLevel3 = async(level3_Data)=>{
    //multiVideo_sec
    const container = document.getElementById('multiVideo_sec');
    const template = document.getElementById('multiVideo_box_template');
    container.innerHTML = '';
    for(video of level3_Data){
        let video_card_clone = template.content.cloneNode(true);
        let card_a_tag = video_card_clone.querySelector('a'); 
        
        card_a_tag.href = video.urls.article_href;
        let img_p_tags = card_a_tag.children;
        img_p_tags[0].src = video.urls.article_img_href;
        img_p_tags[1].innerText = video.texts.para_text;
        container.appendChild(video_card_clone);
    }
}

const renderLevel5 = async(level5_Data)=>{
    //main-heading
    const main_heading = document.querySelector('.level-5 .main-heading')
    main_heading.innerText = level5_Data.section_title;
    main_heading.href = level5_Data.section_href;
    //categories
    const places_ul = document.querySelector('.level-5 ul');
    for(category in level5_Data.categories){
        let li_tag = document.createElement('li');
        li_tag.innerText = category;
        li_tag.className = 'category-based-on-place';
        places_ul.appendChild(li_tag);
    }
    //article-cards
    let son_articles_cont = document.getElementById('state_of_nation_listBox_sec');
    const son_card_template = document.getElementById('son_card_template');
    son_articles_cont.innerHTML = '';
    for(article of level5_Data.categories.All){
        let card_clone = son_card_template.content.cloneNode(true);
        let a_tag = card_clone.getElementById('son_card');
        a_tag.href = article.urls.article_href;
        let child_tags = a_tag.children; 
        child_tags[0].src = article.urls.article_img_href;
        child_tags[1].innerText = article.texts.title;
        child_tags[2].innerText = article.texts.date_time;

        son_articles_cont.appendChild(card_clone);
    }
};

const renderLevel6 = async(level6_Data)=>{
    const opinion_container = document.getElementById('opinion-cards-cont');
    const card_template = document.getElementById('opinion-card-template');
    opinion_container.innerHTML = '';
    for(opinion of level6_Data){
        let card_clone = card_template.content.cloneNode(true);
        let all_a_tags = card_clone.querySelectorAll('a');

        all_a_tags[0].href = opinion.urls.author_profile_href;
        all_a_tags[0].querySelector('img').src = opinion.urls.author_img_href;
        all_a_tags[1].href = opinion.urls.article_href;
        all_a_tags[1].innerText = opinion.texts.opinion_text;
        all_a_tags[2].href = opinion.urls.author_profile_href;
        all_a_tags[2].innerText = opinion.texts.author_name;

        opinion_container.appendChild(card_clone);
    }
}

const renderLevel7 = async(level7_Data)=>{
  //faultlines
  const faultline_sec = document.getElementById('faultline-sec');
  Object.assign(faultline_sec.querySelector('a'),{
    href: level7_Data.fault_lines.section_href,
    innerText : level7_Data.fault_lines.section_title,
  });
  faultline_sec.querySelector('img').src = level7_Data.fault_lines.urls.img_href;
  //two-bit
  const twobit_sec = document.getElementById('two-bit-sec');
  Object.assign(twobit_sec.querySelector('a'),{
    href: level7_Data.two_bit.section_href,
    innerText : level7_Data.two_bit.section_title,
  });
  twobit_sec.querySelector('img').src = level7_Data.two_bit.urls.img_href;
  //eight-column
  const eight_column_sec = document.getElementById('eight-column-sec');
  let all_a_tags = eight_column_sec.querySelectorAll('a');
    //title
  all_a_tags[0].href = level7_Data.eight_column.section_href;
  const eight_column_title = level7_Data.eight_column.section_title.split(" ");
  all_a_tags[0].querySelector('span').innerHTML = `${eight_column_title[0]} <strong>${eight_column_title[1]}</strong> ${eight_column_title[2]}`;
  all_a_tags[1].href = all_a_tags[3].href = level7_Data.eight_column.urls.article_href;
  all_a_tags[1].querySelector('.title').innerText = level7_Data.eight_column.texts.title;
  all_a_tags[1].querySelector('.para-text').innerText = level7_Data.eight_column.texts.para_text;
  all_a_tags[2].href = level7_Data.eight_column.urls.author_profile_href;
  all_a_tags[2].querySelector('.author-name').innerText = level7_Data.eight_column.texts.author_name;
  all_a_tags[3].querySelector('img').src = level7_Data.eight_column.urls.article_img_href; 
};

const renderLevel8 = async(level8_Data)=>{
  let l8_container = document.querySelector('.level-8');
  const cat_box_template = document.getElementById('l8_category_box_template');
  const article_card_template = document.getElementById('l8_article_card_template');

  l8_container.innerHTML = '';
  for(category in level8_Data){
    let cat_box_clone = cat_box_template.content.cloneNode(true);
    //main-heading
    let heading_tag = cat_box_clone.querySelector('a');
    heading_tag.href = `/${category}`;
    heading_tag.innerText = category;

    //article-cards into carousel-card
    let carousel_card, index = 0;
    for(article of level8_Data[category]){
      if(index%5 == 0){
        carousel_card = document.createElement('div');
        carousel_card.className = 'carousel-card flex-column';

        cat_box_clone.querySelector('.owl-carousel').appendChild(carousel_card);
      }
      let article_card_clone = article_card_template.content.cloneNode(true);
      article_card_clone.href = article.urls.article_href;
      article_card_clone.querySelector('img').src = article.urls.article_img_href;
      article_card_clone.querySelector('p').innerText = article.texts.para_text;

      carousel_card.appendChild(article_card_clone);
      index++;
    }
    l8_container.appendChild(cat_box_clone);
  }
}

const renderLevel9 = async(level9_Data)=>{
  let heading_a_tag = document.getElementById('the-federal-playlist-heading');
  heading_a_tag.href = level9_Data.section_href;
  heading_a_tag.querySelector('span').innerText = level9_Data.section_title;

  let container = document.getElementById('federal-playlist-carousel-cont');
  const card_template = document.getElementById('federal-playlist-card-template');
  container.innerHTML = '';
  for(video of level9_Data.videos){
    let card_clone = card_template.content.cloneNode(true);
    card_clone.href = video.urls.article_href;
    let a_tag = card_clone.querySelector('a');
    a_tag.href = video.urls.article_href;
    let all_children = a_tag.children;
    all_children[0].src = video.urls.article_img_href;
    all_children[1].innerText = video.texts.para_text; 
    all_children[2].innerText = video.date_time; 

    container.appendChild(card_clone);
  }
  document.querySelector('.level-9 .main-heading span').innerText = level9_Data.section_para_text;
};
