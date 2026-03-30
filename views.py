from models.usuario import Usuario, usuarioDAO
from models.jogos import Jogo, JogoDAO
from models.palpites import PalpiteDAO, Palpite
import pandas as pd

class View:
    
    # --- USUÁRIOS ---
    @classmethod
    def usuario_listar(cls):
        return usuarioDAO.listar()
    
    @classmethod
    def usuario_inserir(cls, nome, email, senha):
        for c in usuarioDAO.listar():
            if c.get_email() == email.lower():
                raise ValueError("Já existe um usuário com esse email")
        
        # A MUDANÇA AQUI: Adicionamos o "Pendente" como o 6º atributo do usuário
        usuario = Usuario(0, nome, email, senha, 0, "Pendente")
        usuarioDAO.inserir(usuario)

    @classmethod
    def usuario_autenticar(cls, email, senha):
        email_digitado = email.lower().strip()
        senha_digitada = str(senha).strip()
        for c in cls.usuario_listar():
            if c.get_email().strip() == email_digitado and c.get_senha().strip() == senha_digitada:
                
                # A MUDANÇA AQUI: Agora o login também devolve o status do usuário!
                return {
                    "id": c.get_id(), 
                    "nome": c.get_nome(),
                    "status": c.get_status() # Vamos criar isso no passo 2
                }
        return None

    # --- JOGOS ---
    @classmethod
    def jogo_listar(cls):
        return JogoDAO.listar()
    
    @classmethod
    def jogo_atualizar(cls, id, time_a, time_b, data_hora, gols_a, gols_b, finalizado):
        jogo_atualizado = Jogo(id, time_a, time_b, data_hora, gols_a, gols_b, finalizado)
        JogoDAO.atualizar(jogo_atualizado)

    # --- PALPITES (A mágica acontece aqui) ---
    @classmethod
    def palpite_inserir(cls, usuario_id, jogo_id, gols_a, gols_b):
        novo_palpite = Palpite(0, usuario_id, jogo_id, gols_a, gols_b, 0)
        PalpiteDAO.inserir(novo_palpite)

        import streamlit as st
        st.cache_data.clear()

    @classmethod
    def palpite_listar_por_usuario(cls, usuario_id):
        # O Python agora apenas lê os palpites do banco de dados. 
        # A planilha já fez o cálculo!
        return PalpiteDAO.listar_por_usuario(usuario_id)    
    
    @classmethod
    def ranking_geral(cls):
        usuarios = cls.usuario_listar()
        df_palpites = PalpiteDAO.listar_aba("palpites")
        
        if df_palpites.empty:
            for u in usuarios: u.pontos_temp = 0
            return usuarios

        # Garante que os IDs e Pontos sejam lidos corretamente
        df_palpites['usuario_id'] = df_palpites['usuario_id'].astype(int)
        df_palpites['pontos_ganhos'] = pd.to_numeric(df_palpites['pontos_ganhos'], errors='coerce').fillna(0)

        # Agrupa os palpites por usuário e soma os pontos (já calculados pela PLANILHA)
        soma_pontos = df_palpites.groupby('usuario_id')['pontos_ganhos'].sum().to_dict()

        lista_ranking = []
        for u in usuarios:
            if u.get_nome() != "admin":
                # Pega a soma feita, se não tiver, é 0
                u.pontos_temp = int(soma_pontos.get(int(u.get_id()), 0))
                lista_ranking.append(u)

        # Retorna ordenado do maior para o menor
        return sorted(lista_ranking, key=lambda x: x.pontos_temp, reverse=True)