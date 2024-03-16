# Corrige o diretório de trabalho para chamar a importações da pasta .utils
import configurar_path as cg
cg.configurar_path()

# Importa as funcionalidades padrões do projeto
from utils.utils import *

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

from pathlib import Path

limpar_terminal()
print('')

# Obtém o nome do script
nome_script = Path(__file__).name
print(f'--nome_script: {nome_script}')

# Obtém o diretório completo do script com o nome do arquivo .py
diretorio_completo_script_arquivo = Path(__file__).parent
print(f'--diretorio_completo_script_arquivo: {diretorio_completo_script_arquivo}')

# Obtém o diretório completo do script com o nome do arquivo .py
diretorio_completo_script = Path(__file__).resolve()

# Obtém o diretório da pasta do script
diretorio_pasta_script = Path(__file__).parent.parent
print(f'--diretorio_pasta_script: {diretorio_pasta_script}')

# Obtém o diretório de projetos
diretorio_de_projetos = Path(__file__).parent.parent.parent
print(f'--diretorio_de_projetos: {diretorio_de_projetos}')

# Obtém o diretório da pasta do usuário
diretorio_home = Path.home()
print(f'--diretorio_home: {diretorio_home}')


# Pesquisar a pasta "pasta_alvo" em pastas parentes
def pesquisar_pasta_alvo_em_pastas_parentes(pasta_atual,pasta_alvo):
    while True:
        for pasta in pasta_atual.parents:
            pasta = pasta / 'pesquisa_arquivos_sql'
            if pasta.name == pasta_alvo:
                print(f"Pasta '{pasta_alvo}' encontrada em '{pasta}'")   
                return False

print('')

pasta_atual = Path(__file__).parent
pesquisar_pasta_alvo_em_pastas_parentes(pasta_atual,'pesquisa_arquivos_sql')

print('')

def pesquisar_arquivo_em_pastas_parentes(pasta_atual, nome_arquivo):
    while True:
        for pasta in pasta_atual.parents:
            pasta = pasta / 'data' / 'pesquisa_arquivos_sql'
            for arquivo in pasta.iterdir():
                if arquivo.name == nome_arquivo:
                    print(f'Arquivo "{nome_arquivo}" encontrado em "{pasta}"')
                    return arquivo

pasta_atual = Path(__file__).parent
arquivo_encontrado = pesquisar_arquivo_em_pastas_parentes(pasta_atual, 'diretorios.xlsx')