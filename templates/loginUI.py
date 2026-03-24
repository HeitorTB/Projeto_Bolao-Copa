import streamlit as st
from views import View

class LoginUI:
    def main():
        st.header("Entrar")
        st.text("(Entre se você já fez o cadastro)")
        email = st.text_input("Informe o e-mail")
        senha = st.text_input("Informe a senha", type="password")

        if st.button("Entrar"):
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

            