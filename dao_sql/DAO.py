import streamlit as st
from streamlit_gsheets import GSheetsConnection

class DAO:
    # Cria a conexão com o Google Sheets usando o cache do Streamlit
    conn = st.connection("gsheets", type=GSheetsConnection)

    @classmethod
    def abrir(cls):
        # Não precisamos mais do sqlite3.connect
        pass

    @classmethod
    def fechar(cls):
        pass

    @classmethod
    def listar_aba(cls, nome_aba):
        # Lê os dados de uma aba específica da planilha
        return cls.conn.read(worksheet=nome_aba, ttl=0) # ttl=0 evita cache antigo

    @classmethod
    def salvar_aba(cls, nome_aba, df):
        # Sobrescreve a aba com os novos dados (INSERT/UPDATE/DELETE)
        cls.conn.update(worksheet=nome_aba, data=df)