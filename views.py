from models.usuario import Usuario, usuarioDAO
from models.jogos import Jogo, JogoDAO
from models.palpites import PalpiteDAO, Palpite

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

    # --- REGRAS DE PONTUAÇÃO (A lógica que você pediu) ---
    @staticmethod
    def calcular_pontos(pa, pb, ra, rb):
        pa, pb, ra, rb = int(pa), int(pb), int(ra), int(rb)

        if pa == ra and pb == rb: return 12 # Placar cheio
        
        # Ganhador + Gols do ganhador
        if ((ra > rb and pa > pb and pa == ra) or (rb > ra and pb > pa and pb == rb)): return 5
        
        # Ganhador + Gols do perdedor
        if ((ra > rb and pa > pb and pb == rb) or (rb > ra and pb > pa and pa == ra)): return 4
        
        # Ganhador/Empate sem acertar gols exatos
        if ((ra > rb and pa > pb) or (rb > ra and pb > pa) or (ra == rb and pa == pb)): return 3
        
        # Somatória de gols
        if (pa + pb) == (ra + rb): return 2
        
        # Acertou gols de um dos times
        if pa == ra or pb == rb: return 1
        
        return 0

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
        palpites = PalpiteDAO.listar_por_usuario(usuario_id)
        jogos = JogoDAO.listar()
        dic_jogos = {j.get_id(): j for j in jogos}

        atualizou_algo = False # Flag para saber se precisamos salvar no usuário
        total_pontos_usuario = 0 # Vamos somar os pontos aqui

        for p in palpites:
            jogo = dic_jogos.get(p.get_jogo_id())
            pontos_deste_palpite = int(p.get_pontos_ganhos())

            # Se o jogo estiver FINALIZADO na planilha, calculamos os pontos
            if jogo and jogo.get_finalizado():
                pontos_calculados = cls.calcular_pontos(
                    p.get_gols_time_a(), p.get_gols_time_b(),
                    jogo.get_gols_time_a(), jogo.get_gols_time_b()
                )
                
                # Se o ponto salvo na planilha for diferente do cálculo, atualizamos a planilha
                if pontos_deste_palpite != pontos_calculados:
                    PalpiteDAO.atualizar_pontos(p.get_id(), pontos_calculados)
                    pontos_deste_palpite = pontos_calculados # Atualiza para a soma final
                    atualizou_algo = True
            
            # Vai somando os pontos válidos de todos os palpites
            total_pontos_usuario += pontos_deste_palpite

        # --- A MÁGICA NOVA ENTRA AQUI ---
        # Se algum palpite mudou de pontuação, atualizamos a aba do usuário!
        if atualizou_algo:
            usuario = usuarioDAO.listar_id(usuario_id)
            if usuario:
                usuario.set_pontos(total_pontos_usuario)
                usuarioDAO.atualizar(usuario)
                
        return palpites
    
    @classmethod
    def ranking_geral(cls):
        usuarios = cls.usuario_listar()
        # Puxa os palpites direto da DAO para somar
        df_palpites = PalpiteDAO.listar_aba("palpites")
        
        if df_palpites.empty:
            # Se não há palpites, todos têm 0 pontos
            for u in usuarios: u.pontos_temp = 0
            return usuarios

        # Garante que os IDs e Pontos sejam números
        df_palpites['usuario_id'] = df_palpites['usuario_id'].astype(int)
        df_palpites['pontos_ganhos'] = df_palpites['pontos_ganhos'].astype(float)

        # Soma os pontos agrupando por usuário
        soma_pontos = df_palpites.groupby('usuario_id')['pontos_ganhos'].sum().to_dict()

        lista_ranking = []
        for u in usuarios:
            if u.get_nome() != "admin":
                # Atribui a soma ou 0 se não houver palpites para aquele ID
                u.pontos_temp = int(soma_pontos.get(int(u.get_id()), 0))
                lista_ranking.append(u)

        # Ordena do maior para o menor
        return sorted(lista_ranking, key=lambda x: x.pontos_temp, reverse=True)