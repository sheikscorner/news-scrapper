from os import altsep
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from . models import User_Pydantic, UserIn_Pydantic, User
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError
from typing import List
from fastapi.encoders import jsonable_encoder
import requests
from bs4 import BeautifulSoup as BS
from collections import defaultdict
import numpy as np
import nltk 
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import re
from newspaper import Article
app = FastAPI()

register_tortoise(
    app,
    db_url="sqlite://store_db.db",
    modules={'models':['environment.models']},
    generate_schemas = True,
    add_exception_handlers = True,
    

)


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
async def login_page(request :Request):
    return templates.TemplateResponse("index.html", {"request":request})


@app.post("/loginsuccess/", response_class=HTMLResponse)
async def login_success(request: Request, username: str = Form(...), password: str = Form(...)):
    p = await User_Pydantic.from_tortoise_orm(await User.get(username=username, password=password))
    json_compatible_item_data = jsonable_encoder(p)
    if json_compatible_item_data is not None:
        
        
        return templates.TemplateResponse("homepage.html", {"request": request, "username":username})
    else:
        
        status_code:int
        status_code = 500
        return templates.TemplateResponse("index.html", {"request":request, "status_code":status_code})
    
 
@app.get("/register", response_class=HTMLResponse)
async def register(request :Request):
    return templates.TemplateResponse("register.html", {"request":request})

@app.post("/create_user", response_class=HTMLResponse)
async def create_user(request: Request, username: str = Form(...), password: str = Form(...)):
    p = await User.create(username=username, password=password)
    json_compatible_item_data = jsonable_encoder(p)
    return templates.TemplateResponse("index.html", {"request":request})


    
@app.get('/hacker_news', response_class=HTMLResponse)
async def hacker_news(request: Request):
    dict1=defaultdict(list)
    URL="https://thehackernews.com/"
    page=requests.get(URL)
    soup=BS(page.content, 'html.parser')
    results=soup.find_all('div', class_="blog-posts clear")
    for results_element in results:
        title_elem = results_element.find_all('h2', class_='home-title')
        link_element=results_element.find_all('a', class_="story-link", href=True)
        description= results_element.find_all('div', class_="home-desc")
        
        for index,(title,link, desc) in enumerate(zip(title_elem, link_element, description)):
            
            dict1[str(title.text)].append(str(link['href']))
            article = Article(str(link['href']))
            try:
                article.download()
                article.parse()
                article.nlp()
                dict1[str(title.text)].append(article.summary)
            except Exception:
                 del dict1[str(title.text)]   
    
    json_compatible_item_data = jsonable_encoder(dict1)
    return templates.TemplateResponse("display.html", {"request":request, "json_data":json_compatible_item_data})



@app.get('/indian_express', response_class=HTMLResponse)
async def dna_india(request: Request):
    dict1=defaultdict(list)
    URL="https://indianexpress.com/latest-news/"
    page=requests.get(URL)
    soup=BS(page.content, 'html.parser')
    main_div=soup.find("div",class_="nation")
    articles=main_div.find_all("div",class_="articles")
    for i in articles:
        link_data=i.find("div",class_="title").find("a", href=True)
        desc_data = i.find("p").get_text()
        text_data=link_data.text
        dict1[str(text_data)].append(str(link_data.attrs['href']))
        article = Article(str(link_data.attrs['href']))
        try:
            article.download()
            article.parse()
            article.nlp()
            dict1[str(text_data)].append(article.summary)
        except Exception:
            del dict1[str(text_data)]
    
    json_compatible_item_data = jsonable_encoder(dict1)
    return templates.TemplateResponse("display.html", {"request":request, "json_data":json_compatible_item_data})


@app.get('/news_18', response_class=HTMLResponse)
async def deccan_chronicle(request: Request):
    dict1=defaultdict(list)
    URL="https://www.news18.com/india/"
    page=requests.get(URL)
    soup=BS(page.content, 'html.parser')
    main_div = soup.find("div", class_="blog-list") 
    data=main_div.find_all("h4")
    for i in data:
        dict1[str(i.find("a").text)].append(str(i.find("a")['href']))
        article = Article(str(i.find("a")['href']))
        try:
            article.download()
            article.parse()
            article.nlp()
            dict1[str(i.find("a").text)].append(article.summary)
        except Exception:
            del dict1[str(i.find("a").text)]
        
    json_compatible_item_data = jsonable_encoder(dict1)
    return templates.TemplateResponse("display.html", {"request":request, "json_data":json_compatible_item_data})

        
