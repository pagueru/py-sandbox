from pyspark.sql import SparkSession

# Configure a sessão Spark
spark = SparkSession.builder \
    .appName("Consulta SQL Server com PySpark") \
    .config("spark.driver.extraClassPath", "/path/to/sqljdbc42.jar") \
    .getOrCreate()

# Define as credenciais de acesso
nome_usuario = None
senha_usuario = None

# Define as variáveis de referência ao banco e tabela
server = 'RAPHAEL-PC'
database = 'dbLilith'
nome_tabela = 'TB_FILMES'
nome_banco_tabela = f'{database}..{nome_tabela}'
url = f"jdbc:sqlserver://{server};databaseName={database};integratedSecurity=false"

# Configurações de conexão
properties = {
    "user": nome_usuario,
    "password": senha_usuario,
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# Carregar os dados da tabela
df = spark.read.jdbc(url=url, table=nome_tabela, properties=properties)

# Mostrar os dados
df.show()

# Fechar a sessão Spark
spark.stop()