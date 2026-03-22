import streamlit as st
from templates.loginUI import LoginUI
from templates.abrirContaUI import AbrirContaUI
from templates.CadastrarJogosUI import cadastrarJogoUI
from templates.atualizarPlacarUI import AtualizarPlacarUI
from templates.apostasUI import MeusPalpitesUI
from templates.FazerApostasUI import fazerApostasUI
from templates.visualizarPlacarUI import VisualizarPlacarUI
from streamlit_option_menu import option_menu
from templates.RegrasUI import regrasUI
from views import View

class IndexUI: 
    
    @staticmethod
    def menu_visitante():
        # Menu superior horizontal
        op = option_menu(
            menu_title=None,
            options=["Entrar", "Abrir Conta"],
            icons=["box-arrow-in-right", "person-plus"], # Ícones do Bootstrap
            orientation="horizontal"
        )
        if op == "Entrar": LoginUI.main()
        if op == "Abrir Conta": AbrirContaUI.main()
    
    @staticmethod
    def menu_usuario():
        op = option_menu(
            menu_title=None,
            options=["Apostar", "Apostas", "Placar","Regras"],
            icons=["trophy", "card-checklist", "list-ol", "info-circle"],
            orientation="horizontal",
            styles={
                # Força o menu a não jogar itens para baixo
                "nav": {"flex-wrap": "nowrap"}, 
                # Ajusta o tamanho da fonte e o espaçamento para caber certinho
                "nav-link": {
                    "font-size": "15px", 
                    "text-align": "center", 
                    "margin": "0px", 
                    "padding": "10px 5px" 
                }
            }
        )
        if op == "Apostar": fazerApostasUI.main()
        if op == "Apostas": MeusPalpitesUI.main()
        if op == "Placar": VisualizarPlacarUI.main()
        if op == "Regras": regrasUI.main()

    @staticmethod
    def menu_admin():
        op = option_menu(
            menu_title=None,
            options=["Cadastrar", "Atualizar"],
            icons=["plus-circle", "arrow-clockwise"],
            orientation="horizontal"
        )
        if op == "Cadastrar": cadastrarJogoUI.main() # Certifique-se do nome exato do seu método
        if op == "Atualizar": AtualizarPlacarUI.main() # Certifique-se do nome exato do seu método
    
    @staticmethod
    def sidebar():
        # Como tiramos o 'st.sidebar', isso agora renderiza no corpo principal da página!
        if "usuario_id" not in st.session_state:
            IndexUI.menu_visitante()
        else:
            st.write(f"Bem-vindo(a), **{st.session_state['usuario_nome']}** ⚽")
            if st.session_state["usuario_nome"] == "admin":
                IndexUI.menu_admin()
            else:
                IndexUI.menu_usuario()

if __name__ == "__main__":
    IndexUI.sidebar()