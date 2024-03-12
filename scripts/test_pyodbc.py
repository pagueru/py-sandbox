#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Habita as configurações inicias para todo projeto
import config as cg

logger = cg.configurar_logger()
cg.limpar_terminal(False)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

import pyodbc
import pandas as pd

# Configurar a conexão com o banco de dados
database_name = 'LILITH'
dados_conexao = (
    'Driver={SQL Server};'
    'Server=Raphael-PC;'
    f'Database={database_name}'
)

# Estabelecer a conexão
conexao = pyodbc.connect(dados_conexao)
print('Conexão concluída!')

# Criar um cursor
cursor = conexao.cursor()

# Definir o comando SQL
comando = '''
    SELECT *
    FROM TB_PAGBANK
'''

# Executar o comando SQL e obter os resultados
cursor.execute(comando)
resultados = cursor.fetchall()

# Criar um DataFrame com os resultados
df = pd.DataFrame.from_records(resultados, columns=[desc[0] for desc in cursor.description])

# Imprimir o DataFrame
print(df)