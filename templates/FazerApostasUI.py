import streamlit as st
from views import View

class fazerApostasUI:
    @classmethod
    def main(cls):
        st.header("Faça seus Palpites 🎯")
        st.warning("⚠️ **Atenção:** Se você sair ou atualizar a página sem clicar em salvar, seu progresso será perdido!")

        # 1. Verifica quem é o usuário logado
        if "usuario_id" not in st.session_state:
            st.error("Você precisa estar logado para fazer apostas!")
            return

        usuario_id = st.session_state["usuario_id"]

        # 2. Busca todos os jogos e os palpites que o usuário JÁ FEZ
        todos_jogos = View.jogo_listar()
        meus_palpites = View.palpite_listar_por_usuario(usuario_id)
        
        # Cria uma lista apenas com os IDs dos jogos que ele já apostou
        jogos_apostados_ids = [p.get_jogo_id() for p in meus_palpites]

        # Só pega os jogos abertos e que NÃO estão na lista de apostados
        jogos_abertos = [j for j in todos_jogos if not j.get_finalizado() and j.get_id() not in jogos_apostados_ids]

        if not jogos_abertos:
            st.success("Você já palpitou em todos os jogos disponíveis! Acompanhe na aba 'Minhas Apostas'.")
            return

        # 3. Cria o formulário apenas para os jogos que sobraram
        with st.form("form_apostas"):           
            palpites_digitados = {}
            
            for jogo in jogos_abertos:
                # O container com borda deixa cada jogo parecendo um "Card" de aplicativo
                with st.container(border=True):
                    st.caption(f"📅 **{jogo.get_data_hora()}**")
                    
                    # LINHA 1: Time A e Caixa de Gol A
                    colA1, colA2 = st.columns([3, 1], vertical_alignment="center")
                    with colA1:
                        st.markdown(f"<h5 style='margin: 0;'>{jogo.get_time_a()}</h5>", unsafe_allow_html=True)
                    with colA2:
                        gols_a = st.number_input("A", min_value=0, step=1, key=f"gols_a_{jogo.get_id()}", label_visibility="collapsed")
                    
                    # LINHA 2: Time B e Caixa de Gol B
                    colB1, colB2 = st.columns([3, 1], vertical_alignment="center")
                    with colB1:
                        st.markdown(f"<h5 style='margin: 0;'>{jogo.get_time_b()}</h5>", unsafe_allow_html=True)
                    with colB2:
                        gols_b = st.number_input("B", min_value=0, step=1, key=f"gols_b_{jogo.get_id()}", label_visibility="collapsed")
                    
                # Salva no dicionário
                palpites_digitados[jogo.get_id()] = {"gols_a": gols_a, "gols_b": gols_b}

            # Botão de salvar
            submit = st.form_submit_button("Salvar Meus Palpites", use_container_width=True)

            if submit:
                for jogo_id, placar in palpites_digitados.items():
                    View.palpite_inserir(usuario_id, jogo_id, placar["gols_a"], placar["gols_b"])
                
                st.success("Palpite salvo com sucesso!")
                st.rerun()