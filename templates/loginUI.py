import streamlit as st
from views import View

class LoginUI:
    def main():
        st.header("Entrar")
        st.text("(Entre se você já fez o cadastro)")
        
        # Cria o formulário de login
        with st.form("form_login"):
            email = st.text_input("Informe o e-mail")
            senha = st.text_input("Informe a senha", type="password")
            
            # O botão de envio DEVE ser o form_submit_button
            botao_entrar = st.form_submit_button("Entrar")

        # A lógica acontece FORA do 'with st.form'
        if botao_entrar:
            c = View.usuario_autenticar(email, senha)
            if c:
                st.session_state["usuario_tipo"] = "logado"
                st.session_state['usuario_id'] = c["id"]
                st.session_state["usuario_nome"] = c["nome"]
                st.session_state["status"] = c["status"]
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("E-mail ou senha incorretos.")