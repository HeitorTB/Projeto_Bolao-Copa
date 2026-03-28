import streamlit as st
from views import View

class MeusPalpitesUI:
    @classmethod
    def main(cls):
        st.header("Meus Palpites 📝")

        # ==========================================
        # 1. VERIFICAÇÃO DE LOGIN
        # ==========================================
        if "usuario_id" not in st.session_state:
            st.error("Você precisa estar logado!")
            return

        # ==========================================
        # 2. BUSCA E PREPARAÇÃO DOS DADOS
        # ==========================================
        usuario_id = st.session_state["usuario_id"]
        palpites = View.palpite_listar_por_usuario(usuario_id)
        
        if not palpites:
            st.info("Você ainda não fez nenhum palpite. Vá na aba de apostas!")
            return

        todos_jogos = View.jogo_listar()
        dic_jogos = {j.get_id(): j for j in todos_jogos}

        # ==========================================
        # 3. EXIBIÇÃO VISUAL (CARDS)
        # ==========================================
        for palpite in palpites:
            jogo = dic_jogos.get(palpite.get_jogo_id())
            
            # Se por algum motivo o jogo foi apagado, pula para o próximo
            if not jogo:
                continue 

            # --- Extraindo variáveis para limpar o código visual ---
            time_a = jogo.get_time_a()
            time_b = jogo.get_time_b()
            meu_gols_a = int(palpite.get_gols_time_a())
            meu_gols_b = int(palpite.get_gols_time_b())
            finalizado = jogo.get_finalizado()

            # --- Desenhando o Card ---
            with st.container(border=True):
                
                # Cabeçalho: Status
                if finalizado:
                    st.caption("🔴 Finalizado")
                else:
                    st.caption("🟢 Em Aberto")
                
                # Meio: Times e O Seu Palpite
                col1, col2, col3 = st.columns([3, 2, 3])
                
                with col1:
                    st.markdown(f"<div style='text-align: right;'><b>{time_a}</b></div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<div style='text-align: center; background-color: #f0f2f6; border-radius: 5px; color: black;'><b>{meu_gols_a} x {meu_gols_b}</b></div>", unsafe_allow_html=True)
                with col3:
                    st.markdown(f"<div style='text-align: left;'><b>{time_b}</b></div>", unsafe_allow_html=True)
                
                # Divisória nativa do Streamlit
                st.divider() 
                
                # Rodapé: Placar Oficial e Pontuação
                if finalizado:
                    oficial_gols_a = int(jogo.get_gols_time_a())
                    oficial_gols_b = int(jogo.get_gols_time_b())
                    pontos = palpite.get_pontos_ganhos()
                    
                    st.markdown(f"<div style='text-align: center; font-size: 14px;'>Placar Oficial: <b>{oficial_gols_a} x {oficial_gols_b}</b></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: center; color: #28a745; font-size: 14px;'><b>Pontos: {pontos}</b></div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='text-align: center; font-size: 13px; color: gray;'>⏳ Aguardando resultado...</div>", unsafe_allow_html=True)

