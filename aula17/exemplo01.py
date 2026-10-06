import subprocess
from sqlalchemy import create_engine 
import pandas as pd
import os
# pip install python-dotenv
from dotenv import load_dotenv


def conecta_banco():
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    database = os.getenv('DB_DATABASE')
    # URL de conexão com o banco
    engine = create_engine(
    f'mysql+pymysql://{user}:{password}@{host}/{database}'
    )
    return engine


subprocess.run('cls', shell=True)
# ***** Inicio do codigo *****
# Carrega variáveis de ambiente
load_dotenv()
# Chama a função q conecta ao banco
engine = conecta_banco()

try:
    df_usuarios = pd.read_sql('tb_usuarios', engine)
    df_livros = pd.read_sql('tb_livros', engine)
    df_alugados = pd.read_sql('tb_alugados', engine)
    df_itens = pd.read_sql('tb_itens_alugados', engine)
    
    print(df_usuarios)
    print(df_livros)
    print(df_alugados)
    print(df_itens)


except Exception as e:
    print(f'Erro ao conectar aos dados{e}')


# Relacionando os Dataframes com merge
# Pesquisar outras formas de "JOIM" 
try:
    df_merge1 = pd.merge(
        df_livros, df_itens, on= 'id_livro'
    )
    df_merge2 = pd.merge(
        df_merge1, df_alugados, on= 'id_aluguel'
    )
    df_dados = pd.merge(
        # quando os campos forem diferentes, usara a sintaxe
        df_merge2, df_usuarios, left_on= 'id_usuario', right_on= 'id_usuario' 
    )
    print(df_dados)

except Exception as e:
    print(f'Erro ao relacionar os dataframes {e}')

# Filtro para Novembro
try:
    df_novembro = df_dados[(
        (df_dados['data_devolucao'] >= '2024-11-01') & 
        (df_dados['data_devolucao'] <= '2024-11-30')
    )]

    print(df_novembro[
        [
            'id_usuario', 'nome',
            'id_aluguel', 'data_aluguel', 'data_devolucao',
            'id_livro', 'titulo'
        ]
    ])

except Exception as e:
    print(f'Erro ao relacionar os dataframe {e}')








'''
query = """
            SELECT 
                tb_usuarios.id_usuario, tb_usuarios.nome,
                tb_alugados.data_aluguel, tb_alugados.data_devolucao, tb_alugados.valor,
                tb_livros.id_livro, tb_livros.titulo
            FROM
                tb_livros
            JOIN tb_itens_alugados
                ON tb_livros.id_livro = tb_itens_alugados.id_livro
            JOIN tb_alugados
                ON tb_itens_alugados.id_aluguel = tb_alugados.id_aluguel
            JOIN tb_usuarios
                ON tb_usuarios.id_usuario = tb_alugados.id_usuario
            WHERE tb_alugados.data_aluguel BETWEEN '2024-11-01'AND '2024-11-30'
            ORDER BY tb_alugados.data_aluguel;
"""

subprocess.run('cls', shell=True)
df_usuarios = pd.read_sql(query, engine)
print(df_usuarios)
'''