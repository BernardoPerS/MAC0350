# models.py
from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel


# Tabela Doações
class Doacao(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    valor: float
    data_doacao: datetime = Field(default_factory=datetime.utcnow)
    
    doador_id: Optional[int] = Field(default=None, foreign_key="doador.id")
    projeto_id: Optional[int] = Field(default=None, foreign_key="projeto.id")
    
    doador: Optional["Doador"] = Relationship(back_populates="doacoes")
    projeto: Optional["Projeto"] = Relationship(back_populates="doacoes")



# Tabela de Doadores
class Doador(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    nome: str
    telefone: str
    email: str = Field(index=True, unique=True)
    senha: str 
    
    # Um doador pode ter várias doações
    doacoes: List[Doacao] = Relationship(back_populates="doador")


# Tabela de Projetos
class Projeto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    titulo: str 
    proposta: str
    imagem_url: Optional[str] = None 
    localizacao: str
    contato: str
    meta_financeira: float
    
    valor_arrecadado: float = Field(default=0.0) 
    
    proponente_id: Optional[int] = None 
    
    # Um projeto pode receber várias doações
    doacoes: List[Doacao] = Relationship(back_populates="projeto")