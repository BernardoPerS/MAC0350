from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import Projeto

def popular_banco():
    # Garante que as tabelas existem
    create_db_and_tables()
    
    with Session(engine) as session:
        # Trava de segurança: Verifica se já existem projetos
        projetos_existentes = session.exec(select(Projeto)).all()
        if len(projetos_existentes) > 0:
            print("O banco já possui projetos. O seed foi cancelado para evitar duplicação.")
            return

        print("Limpando a pista... Populando o banco com dados reais!")

        projetos_iniciais = [
            Projeto(
                titulo="Reforma do Parquinho Esperança", 
                proposta="O parquinho da creche municipal está enferrujado. Queremos comprar novos escorregadores e balanços.", 
                meta_financeira=8500.0, 
                valor_arrecadado=6200.0, # Quase lá!
                localizacao="Zona Leste, São Paulo", 
                contato="parquinho@esperanca.org",
                imagem_url="https://images.unsplash.com/photo-1596464716127-f2a82984de30?auto=format&fit=crop&w=800&q=80"
            ),
            Projeto(
                titulo="Biblioteca Móvel", 
                proposta="Queremos montar uma kombi com mais de 500 livros infantis para visitar bairros periféricos.", 
                meta_financeira=15000.0, 
                valor_arrecadado=3500.0, # No começo
                localizacao="Campinas, SP", 
                contato="leitura@pequenosleitores.com.br",
                imagem_url="https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=800&q=80"
            ),
            Projeto(
                titulo="Escolinha de Futebol", 
                proposta="Precisamos de bolas novas, coletes e chuteiras para o nosso projeto social.", 
                meta_financeira=3200.0, 
                valor_arrecadado=3100.0, # Faltam só R$ 100!
                localizacao="Osasco, SP", 
                contato="craques@futebolsocial.net",
                imagem_url="https://images.unsplash.com/photo-1526232761682-d26e03ac148e?auto=format&fit=crop&w=800&q=80"
            ), Projeto(
                titulo="Oficina de Robótica: Criando o Futuro", 
                proposta="Queremos adquirir kits de robótica educacional para ensinar lógica de programação e eletrônica básica para 40 crianças da rede pública no contraturno.", 
                meta_financeira=12000.0, 
                valor_arrecadado=4500.0, 
                localizacao="São Bernardo do Campo, SP", 
                contato="robotica@futuro.org",
                imagem_url="https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&w=800&q=80"
            ),
            Projeto(
                titulo="Horta Comunitária 'Mão na Terra'", 
                proposta="Projeto para revitalizar um terreno baldio ao lado da escola, criando uma horta onde as crianças aprendem sobre biologia, sustentabilidade e alimentação saudável.", 
                meta_financeira=2500.0, 
                valor_arrecadado=2100.0, # Quase batendo a meta!
                localizacao="Ribeirão Preto, SP", 
                contato="contato@maonaterra.org",
                imagem_url="https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?auto=format&fit=crop&w=800&q=80"
            ),
            Projeto(
                titulo="Balé para Todos", 
                proposta="Compra de collants, sapatilhas e instalação de espelhos para nossa sala de dança social, que oferece aulas gratuitas de balé clássico para meninas e meninos da comunidade.", 
                meta_financeira=5000.0, 
                valor_arrecadado=1200.0, 
                localizacao="Santos, SP", 
                contato="danca@baleparatodos.br",
                imagem_url="https://images.unsplash.com/photo-1508700929628-666bc8bd84ea?auto=format&fit=crop&w=800&q=80"
            ),
            Projeto(
                titulo="Sorrisos em Cores: Oficina de Grafite", 
                proposta="Projeto para colorir os muros da escola local com a ajuda de artistas profissionais, ensinando técnicas de arte urbana e expressão cultural para os jovens.", 
                meta_financeira=3800.0, 
                valor_arrecadado=3650.0, # Falta muito pouco!
                localizacao="Santo André, SP", 
                contato="arte@sorrisos.org",
                imagem_url="https://images.unsplash.com/photo-1525909002-1b05e0c869d8?auto=format&fit=crop&w=800&q=80"
            ),
            Projeto(
                titulo="Inclusão no Tatame: Judô Infantil", 
                proposta="Aquisição de novos tatames e 30 quimonos para expandir nosso projeto de artes marciais, focado na disciplina e desenvolvimento motor de crianças com TDAH.", 
                meta_financeira=7500.0, 
                valor_arrecadado=2800.0, 
                localizacao="Jundiaí, SP", 
                contato="judo@inclusao.net",
                imagem_url="https://images.unsplash.com/photo-1555597673-b21d5c935865?auto=format&fit=crop&w=800&q=80"
            )
        ]

        # Adiciona todos os projetos de uma vez
        session.add_all(projetos_iniciais)
        session.commit()
        
        print(f"Sucesso! {len(projetos_iniciais)} projetos foram adicionados ao banco de dados.")

if __name__ == "__main__":
    popular_banco()