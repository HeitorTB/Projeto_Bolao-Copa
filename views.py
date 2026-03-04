from models.usuario import Usuario,usuarioDAO
from models.jogos import Jogo, JogoDAO
from models.palpites import PalpiteDAO, Palpite

class View:
    
    def usuario_listar():
        return usuarioDAO.listar()
    
    def usuario_inserir(nome, email, senha):
        for c in usuarioDAO.listar():
            if c.get_email() == email.lower():
                raise ValueError("Já existe um usuário com esse email")
        usuario = Usuario(0, nome, email, senha, 0)
        usuarioDAO.inserir(usuario)

    def usuario_listar_id(id):
        return usuarioDAO.listar_id(id)
    
    def usuario_atualizar(id, nome, email, senha, pontos):
        for c in usuarioDAO.listar():
            if c.get_id() != id and c.get_email() == email.lower():
                raise ValueError("Já existe outro usuario com este e-mail.")
        usuario = Usuario(id, nome, email, senha, pontos)
        usuarioDAO.atualizar(usuario)
    
    def usuario_excluir(id):
        usuario = usuarioDAO.listar_id(id)
        if usuario is None:
            raise ValueError("usuario não encontrado")
        usuarioDAO.excluir(usuario)

    @classmethod
    def usuario_autenticar(cls, email, senha):
        # Garante que o email digitado no login fique igual ao do banco (minúsculo)
        email_digitado = email.lower().strip()
        senha_digitada = str(senha).strip()
        
        for c in View.usuario_listar():
            # Tira possíveis espaços perdidos e compara
            if c.get_email().strip() == email_digitado and c.get_senha().strip() == senha_digitada:
                return {"id": c.get_id(), "nome": c.get_nome()}
        return None
    
    def criar_admin():
        for c in View.usuario_listar():
            if c.get_email() == "admin":
                return
        View.usuario_inserir("admin", "admin", "1234",) 
    
    @classmethod
    def jogo_inserir(cls, time_a, time_b, data_hora):
        jogo = Jogo(0, time_a, time_b, data_hora, 0, 0, False)
        JogoDAO.inserir(jogo)

    @classmethod
    def jogo_listar(cls):
        return JogoDAO.listar()
    
    @classmethod
    def jogo_atualizar(cls, id, time_a, time_b, data_hora, gols_a, gols_b, finalizado):
        # Remonta o objeto Jogo, mas agora com os gols e status atualizados
        jogo_atualizado = Jogo(id, time_a, time_b, data_hora, gols_a, gols_b, finalizado)
        JogoDAO.atualizar(jogo_atualizado)
    
    @classmethod
    def palpite_inserir(cls, usuario_id, jogo_id, gols_a, gols_b):
        # O último '0' é para a coluna pontos_ganhos (ninguém ganha ponto antes do jogo acabar!)
        novo_palpite = Palpite(0, usuario_id, jogo_id, gols_a, gols_b, 0)
        PalpiteDAO.inserir(novo_palpite)
    
    @classmethod
    def palpite_listar_por_usuario(cls, usuario_id):
        return PalpiteDAO.listar_por_usuario(usuario_id)
    
    @classmethod
    def processar_pontuacao_jogo(cls, jogo_id, gols_oficial_a, gols_oficial_b):
        from models.palpites import PalpiteDAO
        from models.usuario import usuarioDAO

        # Garante que o ID do jogo é um número inteiro (evita que o banco não ache as apostas)
        id_jogo_int = int(jogo_id)
        
        # 1. Puxa todas as apostas que a galera fez para esse jogo
        palpites = PalpiteDAO.listar_por_jogo(id_jogo_int)
        
        for p in palpites:
            pontos = 0
            
            # Força os gols a serem números inteiros (evita que '2' texto seja diferente de 2 número)
            gols_p_a = int(p.get_gols_time_a())
            gols_p_b = int(p.get_gols_time_b())
            gols_of_a = int(gols_oficial_a)
            gols_of_b = int(gols_oficial_b)

            # REGRAS DO JOGO:
            if gols_p_a == gols_of_a and gols_p_b == gols_of_b:
                pontos = 5 # Na mosca
            
            elif (gols_p_a > gols_p_b and gols_of_a > gols_of_b) or \
                 (gols_p_a < gols_p_b and gols_of_a < gols_of_b) or \
                 (gols_p_a == gols_p_b and gols_of_a == gols_of_b):
                pontos = 3 # Acertou o vencedor/empate
            
            # 2. Salva os pontos daquela aposta
            PalpiteDAO.atualizar_pontos(p.get_id(), pontos)

        # 3. Pede pro DAO do Usuário recalcular a pontuação total
        usuarioDAO.atualizar_todos_pontos()