from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi import Depends, HTTPException, status, Cookie, Response
from typing import Annotated
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Sintaxe recomendada: diretório como primeiro argumento posicional
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

class Usuario(BaseModel):
    nome: str
    senha: str
    bio: str

usuarios_db = []

@app.get("/")
def pagina_cadastro(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})

@app.get("/login")
def pagina_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/usuarios")
def criar_usuario(user: Usuario):
    usuarios_db.append(user.model_dump())
    return {"usuario": user.nome}


class DadosLogin(BaseModel):
    nome: str
    senha: str

# 1. Rota para "Logar" (Define o Cookie)
@app.post("/login")
def login(dados: DadosLogin, response: Response):
    # Buscamos o usuário usando um laço simples
    usuario_encontrado = None
    for u in usuarios_db:
        if u["nome"] == dados.nome and u["senha"] == dados.senha:
            usuario_encontrado = u
            break
    
    if not usuario_encontrado:
        raise HTTPException(status_code=404, detail="Usuário ou senha incorretos")
    
    # O servidor diz ao navegador: "Guarde esse nome no cookie 'session_user'"
    response.set_cookie(key="session_user", value=dados.nome)
    return {"message": "Logado com sucesso"}

# 2. A Dependência: Lendo o Cookie
def get_active_user(session_user: Annotated[str | None, Cookie()] = None):
    # O FastAPI busca automaticamente um cookie chamado 'session_user'
    if not session_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acesso negado: você não está logado."
        )
    
    user = next((u for u in usuarios_db if u["nome"] == session_user), None)
    if not user:
        raise HTTPException(status_code=401, detail="Sessão inválida")
    
    return user

# 3. Rota Protegida
@app.get("/profile")
def show_profile(request: Request, user: dict = Depends(get_active_user)):
    return templates.TemplateResponse(
        request=request, 
        name="profile.html", 
        context={"nome": user["nome"], "bio": user["bio"]}
    )




