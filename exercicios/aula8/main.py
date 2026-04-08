from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
# Define a busca de templates nas pastas especificadas
templates = Jinja2Templates(directory=["Templates", "Templates/Partials", "."])
app.mount("/static", StaticFiles(directory="static"), name="static")

# Estado global para persistência das curtidas
curtidas = 0

@app.get("/", response_class=HTMLResponse)
@app.get("/home", response_class=HTMLResponse)
async def root(request: Request):

    return templates.TemplateResponse(request, "index.html", {"pagina": "/aba-curtidas"})

@app.get("/aba-curtidas", response_class=HTMLResponse)
async def aba_curtidas(request: Request):
    if "HX-Request" not in request.headers:
        return templates.TemplateResponse(request, "index.html", {"pagina": "/aba-curtidas"})
    global curtidas
    return templates.TemplateResponse(request, "curtida.html", {"numero_likes": curtidas})

@app.get("/aba-jupiter", response_class=HTMLResponse)
async def aba_jupiter(request: Request):
    if "HX-Request" not in request.headers:
        return templates.TemplateResponse(request, "index.html", {"pagina": "/aba-jupiter"})
    return templates.TemplateResponse(request, "jupiter.html")

@app.get("/home/kelly", response_class=HTMLResponse)
async def aba_kelly(request: Request):
    if "HX-Request" not in request.headers:
        return templates.TemplateResponse(request, "index.html", {"pagina": "/home/kelly"})
    return templates.TemplateResponse(request, "kelly.html")


@app.post("/curtir", response_class=HTMLResponse)
async def curtir(request: Request):
    global curtidas
    curtidas += 1
    return templates.TemplateResponse(request, "curtida.html", {"numero_likes": curtidas})

@app.put("/curtir", response_class=HTMLResponse)
async def zerar(request: Request):
    global curtidas
    curtidas = 0
    return templates.TemplateResponse(request, "curtida.html", {"numero_likes": curtidas})