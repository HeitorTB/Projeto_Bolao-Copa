from dao_sql.DAO import DAO
import pandas as pd
class Palpite:
    # Adicionamos o pontos_ganhos, que começa valendo 0
    def __init__(self, id, usuario_id, jogo_id, gols_time_a, gols_time_b, pontos_ganhos=0):
        self.__id = id
        self.__usuario_id = usuario_id
        self.__jogo_id = jogo_id
        self.__gols_time_a = gols_time_a
        self.__gols_time_b = gols_time_b
        self.__pontos_ganhos = pontos_ganhos

    def get_id(self): return self.__id
    def get_usuario_id(self): return self.__usuario_id
    def get_jogo_id(self): return self.__jogo_id
    def get_gols_time_a(self): return self.__gols_time_a
    def get_gols_time_b(self): return self.__gols_time_b
    def get_pontos_ganhos(self): return self.__pontos_ganhos

class PalpiteDAO(DAO):
    @classmethod
    def inserir(cls, obj):
        df = cls.listar_aba("palpites")
        novo_id = int(df["id"].max() + 1) if not df.empty else 1
        
        nova_linha = {
            "id": novo_id,
            "usuario_id": obj.get_usuario_id(),
            "jogo_id": obj.get_jogo_id(),
            "gols_time_a": obj.get_gols_time_a(),
            "gols_time_b": obj.get_gols_time_b(),
            "pontos_ganhos": obj.get_pontos_ganhos()
        }
        
        df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
        cls.salvar_aba("palpites", df)

    @classmethod
    def listar_por_usuario(cls, id_usuario):
        df = cls.listar_aba("palpites")
        # Filtra as linhas onde usuario_id é igual ao id_usuario
        filtro = df[df['usuario_id'] == id_usuario]
        return [Palpite(r['id'], r['usuario_id'], r['jogo_id'], 
                        r['gols_time_a'], r['gols_time_b'], r['pontos_ganhos']) 
                for _, r in filtro.iterrows()]

    @classmethod
    def listar_por_jogo(cls, id_jogo):
        df = cls.listar_aba("palpites")
        filtro = df[df['jogo_id'] == id_jogo]
        return [Palpite(r['id'], r['usuario_id'], r['jogo_id'], 
                        r['gols_time_a'], r['gols_time_b'], r['pontos_ganhos']) 
                for _, r in filtro.iterrows()]