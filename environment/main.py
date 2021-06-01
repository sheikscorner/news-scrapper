from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from . models import User_Pydantic, UserIn_Pydantic, User
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError
from typing import List
from fastapi.encoders import jsonable_encoder
import requests
from bs4 import BeautifulSoup as BS


app = FastAPI()

register_tortoise(
    app,
    db_url="sqlite://store_db.db",
    modules={'models':['environment.models']},
    generate_schemas = True,
    add_exception_handlers = True,
    
https://avatars.githubusercontent.com/u/85100480?s=60&v=4
)


templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
async def login_page(request :Request):
    return templates.TemplateResponse("index.html", {"request":request})


@app.post("/loginsuccess/", response_class=HTMLResponse)
async def login_success(request: Request, username: str = Form(...), password: str = Form(...)):
    p = await User_Pydantic.from_tortoise_orm(await User.get(username=username, password=password))
    json_compatible_item_data = jsonable_encoder(p)
    print(json_compatible_item_data, "33333333333333333333333")
    if json_compatible_item_data is not None:
        
        print(json_compatible_item_data["username"], "22222222222222222")
        return templates.TemplateResponse("homepage.html", {"request": request, "username":username})
    else:
        print("NOOOOOOOOOOOOOOOOO")
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
    print(json_compatible_item_data, "1000000000000000000")
    return templates.TemplateResponse("index.html", {"request":request})


    
@app.get('/hacker_news', response_class=HTMLResponse)
async def hacker_news(request: Request):
    dict={}
    URL="https://thehackernews.com/"
    page=requests.get(URL)

    soup=BS(page.content, 'html.parser')
    results=soup.find_all('div', class_="blog-posts clear")
    for results_element in results:
        title_elem = results_element.find_all('h2', class_='home-title')
        link_element=results_element.find_all('a', class_="story-link", href=True)
        for index,(title,link) in enumerate(zip(title_elem, link_element)):
            dict[str(title.text)]=str(link['href'])
    json_compatible_item_data = jsonable_encoder(dict)
    return templates.TemplateResponse("display.html", {"request":request, "json_data":json_compatible_item_data})


@app.get('/indian_express', response_class=HTMLResponse)
async def dna_india(request: Request):
    dict={}
    URL="https://indianexpress.com/latest-news/"
    page=requests.get(URL)
    soup=BS(page.content, 'html.parser')
    main_div=soup.find("div",class_="nation")
    articles=main_div.find_all("div",class_="articles")
    for i in articles:
        link_data=i.find("div",class_="title").find("a", href=True)
        text_data=link_data.text
        dict[str(text_data)] = str(link_data.attrs['href'])
    json_compatible_item_data = jsonable_encoder(dict)
    return templates.TemplateResponse("display.html", {"request":request, "json_data":json_compatible_item_data})
