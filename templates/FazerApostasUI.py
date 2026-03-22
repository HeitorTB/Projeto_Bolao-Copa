import streamlit as st
from views import View

class fazerApostasUI:
    @classmethod
    def main(cls):
        st.header("Faça seus Palpites 🎯")

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

        # O FILTRO MÁGICO: Só pega os jogos abertos e que NÃO estão na lista de apostados
        jogos_abertos = [j for j in todos_jogos if not j.get_finalizado() and j.get_id() not in jogos_apostados_ids]

        # Se a lista ficar vazia, ele esconde o formulário e mostra o aviso:
        if not jogos_abertos:
            st.success("Você já palpitou em todos os jogos disponíveis! Acompanhe na aba 'Minhas Apostas'.")
            return

        # 3. Cria o formulário apenas para os jogos que sobraram
        with st.form("form_apostas"):           
            palpites_digitados = {}
            for jogo in jogos_abertos:
                st.write(f"{jogo.get_data_hora()}")
                
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2], vertical_alignment="center")
                
                with col1:
                    st.subheader(jogo.get_time_a())
                with col2:
                    gols_a = st.number_input("", min_value=0, step=1, key=f"gols_a_{jogo.get_id()}")
                with col3:
                    st.subheader("X")
                with col4:
                    gols_b = st.number_input("", min_value=0, step=1, key=f"gols_b_{jogo.get_id()}")
                with col5:
                    st.subheader(jogo.get_time_b())
                # Guarda os gols digitados
                palpites_digitados[jogo.get_id()] = {"gols_a": gols_a, "gols_b": gols_b}

            # O botão de salvar
            submit = st.form_submit_button("Salvar Meus Palpites")

            if submit:
                for jogo_id, placar in palpites_digitados.items():
                    View.palpite_inserir(usuario_id, jogo_id, placar["gols_a"], placar["gols_b"])
                
                st.success("Palpite salvo com sucesso!")
                
                # 4. A MÁGICA ACONTECE AQUI: Atualiza a tela para o jogo sumir na hora!
                st.rerun()