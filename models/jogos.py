import pandas as pd
class Jogo:
    # Quando cadastramos um jogo, ele começa com 0 gols e finalizado=False
    def __init__(self, id, time_a, time_b, data_hora, gols_time_a=0, gols_time_b=0, finalizado=False):
        self.__id = id
        self.__time_a = time_a
        self.__time_b = time_b
        self.__data_hora = data_hora
        self.__gols_time_a = gols_time_a
        self.__gols_time_b = gols_time_b
        self.__finalizado = finalizado

    def get_id(self): return self.__id
    def get_time_a(self): return self.__time_a
    def get_time_b(self): return self.__time_b
    def get_data_hora(self): return self.__data_hora
    def get_gols_time_a(self): return self.__gols_time_a
    def get_gols_time_b(self): return self.__gols_time_b
    def get_finalizado(self): return self.__finalizado

from dao_sql.DAO import DAO
class JogoDAO(DAO):
    @classmethod
    def inserir(cls, obj):
        df = cls.listar_aba("jogos")
        novo_id = int(df["id"].max() + 1) if not df.empty else 1
        
        nova_linha = {
            "id": novo_id,
            "time_a": obj.get_time_a(),
            "time_b": obj.get_time_b(),
            "data_hora": obj.get_data_hora(),
            "gols_time_a": obj.get_gols_time_a(),
            "gols_time_b": obj.get_gols_time_b(),
            "finalizado": obj.get_finalizado()
        }
        
        df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
        cls.salvar_aba("jogos", df)

    @classmethod
    def listar(cls):
        df = cls.listar_aba("jogos")
        return [Jogo(r['id'], r['time_a'], r['time_b'], r['data_hora'], 
                     r['gols_time_a'], r['gols_time_b'], bool(r['finalizado'])) 
                for _, r in df.iterrows()]

    @classmethod
    def atualizar(cls, obj):
        df = cls.listar_aba("jogos")
        df.loc[df['id'] == obj.get_id(), 
               ['time_a', 'time_b', 'data_hora', 'gols_time_a', 'gols_time_b', 'finalizado']] = \
            [obj.get_time_a(), obj.get_time_b(), obj.get_data_hora(), 
             obj.get_gols_time_a(), obj.get_gols_time_b(), obj.get_finalizado()]
        cls.salvar_aba("jogos", df)