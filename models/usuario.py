import pandas as pd
from dao_sql.DAO import DAO

class Usuario:
    def __init__(self, id, nome, email, senha, pontos, status="Pendente"):
        self.set_id(id)
        self.set_nome(nome)
        self.set_email(email)
        self.set_senha(senha)
        self.set_pontos(pontos)
        self.set_status(status)

    def set_id(self, valor):
        self.__id = valor
    def set_nome(self, valor):
        if not valor.strip():
            raise ValueError("Nome não pode ser vazio")
        self.__nome = valor
    def set_email(self, valor):
        if not valor.strip():
            raise ValueError("Email não pode ser vazio")
        self.__email = valor
    def set_senha(self, valor):
        if not valor.strip():
            raise ValueError("Senha não pode ser vazia")
        self.__senha = valor
    def set_pontos(self, valor):
        self.__pontos = valor
    def set_status(self, valor):
        self.__status = valor
        
    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_senha(self): return self.__senha
    def get_email(self): return self.__email
    def get_pontos(self): return self.__pontos
    def get_status(self): return self.__status

class usuarioDAO(DAO):
    @classmethod
    def listar(cls):
        df = cls.listar_aba("usuario")
        
        # --- A MÁGICA DA BLINDAGEM CONTRA O NaN COMEÇA AQUI ---
        if 'id' in df.columns:
            df = df.dropna(subset=['id'])
            
        col_pontos = 'pontos' if 'pontos' in df.columns else 'Pontos'
        if col_pontos in df.columns:
            df[col_pontos] = pd.to_numeric(df[col_pontos], errors='coerce').fillna(0)
        else:
            df['pontos'] = 0 # Previne erro caso a coluna suma
        # -------------------------------------------------------

        if "status" not in df.columns:
            df["status"] = "Pendente"
        df["status"] = df["status"].fillna("Pendente")

        usuarios = []
        for _, row in df.iterrows():
            senha_limpa = str(row['senha']).removesuffix('.0')
            
            usuarios.append(Usuario(
                int(row['id']), 
                str(row['nome']), 
                str(row['email']), 
                senha_limpa, 
                int(row['pontos']), # <--- CORRIGIDO AQUI (Evita o erro do iloc[6])
                str(row['status'])
            ))
        return usuarios

    @classmethod
    def inserir(cls, obj):
        df = cls.listar_aba("usuario")
        
        # 1. Remove linhas vazias e calcula o novo ID
        if 'id' in df.columns:
            df = df.dropna(subset=['id'])
            
        novo_id = int(df["id"].max() + 1) if not df.empty else 1
        
        # 2. Criamos a nova linha SEM a coluna de pontos
        nova_linha = {
            "id": novo_id,
            "nome": obj.get_nome(),
            "email": obj.get_email().lower(),
            "senha": obj.get_senha(),
            "status": obj.get_status()
        }
        
        # --- O PULO DO GATO ---
        # Antes de concatenar, removemos as colunas de pontos do DataFrame lido.
        # Assim, o Pandas não terá nenhuma coluna de pontos para salvar na planilha.
        colunas_para_remover = ['pontos', 'Pontos', 'pontos_ganhos']
        for col in colunas_para_remover:
            if col in df.columns:
                df = df.drop(columns=[col])
        
        # 3. Concatena apenas com as colunas básicas
        df_nova = pd.DataFrame([nova_linha])
        df = pd.concat([df, df_nova], ignore_index=True)
             
        # 4. Salva. Como o DF não tem a coluna 'pontos', o Sheets preserva a fórmula que está lá.
        cls.salvar_aba("usuario", df)

    @classmethod
    def listar_id(cls, id):
        df = cls.listar_aba("usuario")
        
        # BLINDAGEM: Mesma coisa aqui, garante que a coluna existe
        if "status" not in df.columns:
            df["status"] = "Pendente"
        df["status"] = df["status"].fillna("Pendente")
        
        r = df[df['id'] == id]
        if not r.empty:
            row = r.iloc[0]
            senha_limpa = str(row['senha']).removesuffix('.0')
            
            return Usuario(
                int(row['id']), 
                str(row['nome']), 
                str(row['email']), 
                senha_limpa, 
                int(row['pontos']),
                str(row['status'])
            )
        return None

    @classmethod
    def atualizar(cls, obj):
        df = cls.listar_aba("usuario")
        
        if "status" not in df.columns:
            df["status"] = "Pendente"
            
        # 1. Atualiza apenas os campos que o usuário pode editar (sem os pontos)
        df.loc[df['id'] == obj.get_id(), ['nome', 'email', 'senha', 'status']] = \
            [obj.get_nome(), obj.get_email(), obj.get_senha(), obj.get_status()]
            
        # 2. O PULO DO GATO REPLICADO
        # Removemos a coluna pontos para o Sheets manter a ArrayFormula intacta
        colunas_para_remover = ['pontos', 'Pontos', 'pontos_ganhos']
        for col in colunas_para_remover:
            if col in df.columns:
                df = df.drop(columns=[col])
                
        cls.salvar_aba("usuario", df)