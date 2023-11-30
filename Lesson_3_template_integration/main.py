from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse
from typing import Optional

app = FastAPI()

templates = Jinja2Templates('templates')


@app.get('index/', response_class=HTMLResponse)
def index(request: Request, hx_request: Optional[str] = Header(None)):
    films = [
        {'name': 'Blade Runner', 'director': 'Ridley Scott'},
        {'name': 'Pulp fiction', 'director': 'Quentin Tarantino'},
        {'name': 'Fast X', 'director': 'Justin Lin'},
        {'name': 'Warrior', 'director': 'Justin Lin'},
        {'name': 'Transformers', 'director': 'Steven Spielberg'},
    ]
    if hx_request:
        return templates.TemplateResponse('table.html', context)

    context = {'request': request, 'films': films}
    return templates.TemplateResponse('index.html', context)