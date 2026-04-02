import streamlit as st
from views import View
import time

class AbrirContaUI:
    def main():
        st.header("Criar uma conta")
        
        # Cria o formulário de cadastro
        with st.form("form_cadastro"):
            nome = st.text_input("Informe o nome")
            email = st.text_input("Informe o e-mail")
            senha = st.text_input("Informe a senha", type="password")
            
            # O botão de envio DEVE ser o form_submit_button
            botao_inserir = st.form_submit_button("Inserir")

        # A lógica acontece FORA do 'with st.form'
        if botao_inserir:
            try:
                View.usuario_inserir(nome, email, senha)
                st.success("Conta criada com sucesso!")
                time.sleep(2)
                st.rerun()
            except Exception as erro:
                st.error(erro)
                # Dica: Tirei o rerun() automático do erro para dar tempo de ler a mensagem!