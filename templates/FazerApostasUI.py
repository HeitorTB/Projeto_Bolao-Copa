import streamlit as st
import pandas as pd
from views import View

class fazerApostasUI:
    @classmethod
    def main(cls):
        st.header("Faça seus Palpites 🎯")
        st.info("Preencha os placares diretamente na tabela abaixo. Clique na célula para digitar!")

        if "usuario_id" not in st.session_state:
            st.error("Você precisa estar logado!")
            return

        usuario_id = st.session_state["usuario_id"]

        # 1. Puxar todos os jogos e os palpites que o usuário já fez (se houver)
        todos_jogos = View.jogo_listar()
        meus_palpites = View.palpite_listar_por_usuario(usuario_id)
        
        # Criar um dicionário rápido para saber se já tem palpite para o jogo
        dic_palpites = {p.get_jogo_id(): p for p in meus_palpites}

        # 2. Montar os dados para a Tabela
        dados = []
        for jogo in todos_jogos:
            # Vamos mostrar apenas os jogos que ainda não estão finalizados
            if not jogo.get_finalizado():
                palpite = dic_palpites.get(jogo.get_id())
                
                # Se já tiver palpite, puxa os gols. Se não, deixa vazio (None)
                gols_a = int(palpite.get_gols_time_a()) if palpite else None
                gols_b = int(palpite.get_gols_time_b()) if palpite else None

                dados.append({
                    "ID": jogo.get_id(), # Vamos esconder essa coluna depois
                    "Data/Hora": jogo.get_data_hora(),
                    "Casa": jogo.get_time_a(),
                    "Gols Casa": gols_a,
                    "X": "X",
                    "Gols Visit": gols_b,
                    "Visitante": jogo.get_time_b()
                })

        if not dados:
            st.success("Não há jogos abertos para palpitar no momento!")
            return

        df = pd.DataFrame(dados)

        # 3. A MÁGICA: st.data_editor cria a tabela editável
        df_editado = st.data_editor(
            df,
            hide_index=True,
            use_container_width=True,
            height=600, # Altura boa para ver vários jogos de uma vez
            column_config={
                "ID": None, # Isso esconde o ID do jogo do usuário
                "Data/Hora": st.column_config.TextColumn("Data", disabled=True),
                "Casa": st.column_config.TextColumn("Mandante", disabled=True),
                "X": st.column_config.TextColumn("", disabled=True), # Apenas decorativo
                "Visitante": st.column_config.TextColumn("Visitante", disabled=True),
                
                # AS ÚNICAS COLUNAS EDITÁVEIS:
                "Gols Casa": st.column_config.NumberColumn(
                    "Gols", min_value=0, max_value=20, step=1, format="%d"
                ),
                "Gols Visit": st.column_config.NumberColumn(
                    "Gols", min_value=0, max_value=20, step=1, format="%d"
                )
            }
        )

        # 4. Botão para Salvar as edições da tabela de uma vez só
        if st.button("Salvar Todos os Palpites", type="primary", use_container_width=True):
            # Percorre a tabela que o usuário acabou de preencher/editar na tela
            for index, row in df_editado.iterrows():
                
                # Só salva se ele preencheu OS DOIS placares (não estão vazios)
                if pd.notna(row["Gols Casa"]) and pd.notna(row["Gols Visit"]):
                    jogo_id = int(row["ID"])
                    gols_a = int(row["Gols Casa"])
                    gols_b = int(row["Gols Visit"])
                    
                    # Aqui você chama a sua função de inserir/atualizar o palpite
                    View.palpite_inserir(usuario_id, jogo_id, gols_a, gols_b)
            
            st.success("Palpites salvos com sucesso!")
            st.rerun() # Dá um refresh na tela para garantir