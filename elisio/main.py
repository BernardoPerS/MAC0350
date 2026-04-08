from typing import Annotated
from fastapi import FastAPI, Request, Depends, Response, Cookie
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from fastapi import Form 
from sqlalchemy.exc import IntegrityError 
from sqlmodel import col

from database import create_db_and_tables, get_session
from models import Doador, Projeto, Doacao

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory=["Templates", "Templates/Partials"])



def obter_usuario_logado(
    session_user: Annotated[str | None, Cookie()] = None,
    session: Session = Depends(get_session)
):
    if not session_user:
        return None 
    usuario = session.exec(select(Doador).where(Doador.email == session_user)).first()
    return usuario



@app.get("/", response_class=HTMLResponse)
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request, usuario: Doador = Depends(obter_usuario_logado)):
    contexto = {"request": request, "pagina_atual": "home.html", "usuario": usuario}
    if "HX-Request" in request.headers:
        return templates.TemplateResponse(name="home.html", context=contexto)
    return templates.TemplateResponse(name="layout.html", context=contexto)


@app.get("/cadastrar", response_class=HTMLResponse)
async def pagina_cadastrar(request: Request, usuario: Doador = Depends(obter_usuario_logado)):
    contexto = {"request": request, "pagina_atual": "cadastro.html", "usuario": usuario}
    if "HX-Request" in request.headers:
        return templates.TemplateResponse(name="cadastro.html", context=contexto)
    return templates.TemplateResponse(name="layout.html", context=contexto)


@app.get("/login", response_class=HTMLResponse)
async def pagina_login(request: Request, usuario: Doador = Depends(obter_usuario_logado)):
    contexto = {"request": request, "pagina_atual": "login.html", "usuario": usuario}
    if "HX-Request" in request.headers:
        return templates.TemplateResponse(name="login.html", context=contexto)
    return templates.TemplateResponse(name="layout.html", context=contexto)


@app.get("/perfil", response_class=HTMLResponse)
async def pagina_perfil(
    request: Request, 
    page: int = 1,
    usuario: Doador = Depends(obter_usuario_logado),
    session: Session = Depends(get_session)
):
    if not usuario:
        return HTMLResponse("<h2>Acesso negado.</h2>")
    
    tamanho_pagina = 5
    offset = (page - 1) * tamanho_pagina
    
    statement = select(Doacao).where(Doacao.doador_id == usuario.id).offset(offset).limit(tamanho_pagina)
    doacoes = session.exec(statement).all()
    
    contexto = {
        "request": request, 
        "usuario": usuario, 
        "doacoes": doacoes, 
        "page": page,
        "tem_proximo": len(doacoes) == tamanho_pagina 
    }

    if "HX-Request" in request.headers and request.headers.get("HX-Target") == "lista-doacoes":
        return templates.TemplateResponse(name="doacao_lista.html", context=contexto)
    
    if "HX-Request" in request.headers:
        return templates.TemplateResponse(name="perfil.html", context=contexto)
        
    return templates.TemplateResponse(name="layout.html", context=contexto)       



@app.post("/cadastrar", response_class=HTMLResponse)
async def registrar_doador(
    request: Request, 
    session: Session = Depends(get_session)
):
    
    form_data = await request.form()
    
    
    nome = form_data.get("nome", "")
    telefone = form_data.get("telefone", "")
    email = form_data.get("email", "")
    senha = form_data.get("senha", "")
    
    
    if not email or not senha or not nome:
        return HTMLResponse("<div style='color: red;'>Erro: Preencha todos os campos obrigatórios.</div>")

    novo_doador = Doador(nome=nome, telefone=telefone, email=email, senha=senha)
    
    try:
        session.add(novo_doador)
        session.commit()
        return HTMLResponse(f"""
        <div style='color: green; padding: 20px; border: 1px solid green; border-radius: 8px;'>
            <h3>Cadastro realizado com sucesso!</h3>
            <button hx-get='/login' hx-target='#conteudo-principal' hx-push-url="true">Ir para o Login</button>
        </div>
        """)
    except IntegrityError:
        session.rollback()
        return HTMLResponse("<div style='color: red;'>Erro: Este e-mail já existe no banco de dados!</div>")


@app.post("/login", response_class=HTMLResponse)
async def fazer_login(
    request: Request,
    session: Session = Depends(get_session)
):

    form_data = await request.form()
    
    email_digitado = form_data.get("email", "")
    senha_digitada = form_data.get("senha", "")
    
    if not email_digitado or not senha_digitada:
        return HTMLResponse("<div style='color: red;'>Erro: Digite e-mail e senha.</div>")

    doador = session.exec(select(Doador).where(Doador.email == email_digitado)).first()
    
    if not doador or doador.senha != senha_digitada:
        return HTMLResponse("""
        <div style='color: red; margin-bottom: 10px;'>E-mail ou senha incorretos.</div>
        <form hx-post="/login" hx-target="#area-login" hx-swap="outerHTML">
            <div><label>E-mail:</label><input type="email" name="email" required></div><br>
            <div><label>Senha:</label><input type="password" name="senha" required></div><br>
            <button type="submit">Entrar</button>
        </form>
        """)
    
   
    
    resposta = HTMLResponse("Login aprovado! Redirecionando...")
    

    resposta.set_cookie(key="session_user", value=doador.email)
    resposta.headers["HX-Redirect"] = "/"
    
    return resposta

@app.get("/logout")
async def fazer_logout(request: Request):
    
    resposta = templates.TemplateResponse("layout.html", {
        "request": request, 
        "pagina_atual": "home.html", 
        "usuario": None
    })
    
    resposta.delete_cookie("session_user")
    
    return resposta


@app.get("/projetos", response_class=HTMLResponse)
async def listar_projetos(
    request: Request,
    q: str = "", 
    page: int = 1, 
    session: Session = Depends(get_session),
    usuario: Doador = Depends(obter_usuario_logado)
):
    tamanho_pagina = 3 
    offset = (page - 1) * tamanho_pagina
    
    statement = select(Projeto).where(
        col(Projeto.titulo).contains(q) | col(Projeto.proposta).contains(q)
    ).offset(offset).limit(tamanho_pagina)
    
    projetos = session.exec(statement).all()
    
    contexto = {
        "request": request,
        "projetos": projetos,
        "q": q,
        "page": page,
        "tem_proximo": len(projetos) == tamanho_pagina, 
        "usuario": usuario
    }
    
    if "HX-Request" in request.headers:
        return templates.TemplateResponse("projeto_lista.html", contexto)
    
    return templates.TemplateResponse("layout.html", {**contexto, "pagina_atual": "home.html"})



@app.put("/doar/{projeto_id}", response_class=HTMLResponse)
async def fazer_doacao(
    request: Request,
    projeto_id: int,
    session: Session = Depends(get_session),
    usuario: Doador = Depends(obter_usuario_logado)
):
    form_data = await request.form()
    valor_doado = float(form_data.get("valor", 0))

    if not usuario:
        return HTMLResponse("<div style='color: red;'>Você precisa estar logado para doar.</div>")

    projeto = session.get(Projeto, projeto_id)
    if not projeto:
        return HTMLResponse("Projeto não encontrado.")

    nova_doacao = Doacao(valor=valor_doado, doador_id=usuario.id, projeto_id=projeto.id)
    session.add(nova_doacao)

    projeto.valor_arrecadado += valor_doado
    session.add(projeto)

    session.commit()
    session.refresh(projeto)

    contexto = {"request": request, "p": projeto, "usuario": usuario}
    return templates.TemplateResponse(name="projeto_card.html", context=contexto)



@app.post("/perfil/atualizar")
async def atualizar_perfil(
    request: Request,
    nome: str = Form(...),
    telefone: str = Form(...),
    usuario: Doador = Depends(obter_usuario_logado),
    session: Session = Depends(get_session)
):
    if not usuario:
        return HTMLResponse("Sessão expirada.")
    
    usuario.nome = nome
    usuario.telefone = telefone
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    
    contexto = {"request": request, "usuario": usuario, "doacoes": usuario.doacoes[:5], "page": 1}
    return templates.TemplateResponse("perfil.html", contexto)

@app.delete("/perfil/deletar")
async def deletar_perfil(
    response: Response,
    usuario: Doador = Depends(obter_usuario_logado),
    session: Session = Depends(get_session)
):
    if usuario:
        session.delete(usuario)
        session.commit()
    
    response.delete_cookie("session_user")
    return HTMLResponse(headers={"HX-Redirect": "/"})