'''
- A ideia do script é verificar em todas as pastas de scripts quais são os scripts que eu fiz (scripts com a string 'Raphael Coelho');
- Os diretórios das pastas de scripts estão no campo 'Caminho' do arquivo C:/Users/rapha/Desktop/Github/py-sandbox/data/diretorio.xlsx;
- Preciso percorrer esse campo e verificar quais arquivos estão dentro de cada pasta;
- Após tudo preparado, deve copiar os arquivos que correspondem a string desejada para uma pasta de destino
'''

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Permite funcionalidades para interações com o sistema
import os
import sys

# Corrige o diretório de trabalho para chamar a importações de .utils
import configurar_script as cg
cg.configurar_path()

# Importa as funcionalidades padrões do projeto
from utils.utils import *

# Configura o logger e limpa o terminal
#logger = logging.getLogger(__name__)
logger = configurar_logger(__name__)
limpar_terminal(True)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

#### --> Adicionar comentárioss por bibliteca
import pandas as pd
import shutil
from typing import NewType, Union, List
from pathlib import Path

# Obtém o nome do script
nome_script = Path(__file__).name

# Obtém o diretório completo do script com o nome do arquivo .py
diretorio_completo_script_arquivo = Path(__file__).parent

# Obtém o diretório da pasta do script
diretorio_pasta_script = Path(__file__).parent.parent

# Mensagem de inicialização
logger.info(f'Iniciando o script {format_1(nome_script)} no diretório {format_2(diretorio_completo_script_arquivo)}.')


# Normaliza o diretório
def trata_diretorio(caminho: str) -> Path:
    try:
        return Path(os.path.normpath(caminho))
    except Exception as e:
        logger.error(f'Erro ao normalizar o diretório {format_3(caminho)}:\n{e}\n')
        finaliza_script_com_erro()

# Verifica se uma string está presente em um arquivo
def busca_string_em_arquivo(caminho_arquivo: Path, texto_procurado: str) -> bool:
    
    trata_diretorio(caminho_arquivo)
    
    encodings = ['utf-8', 'latin-1']  # Tentar com UTF-8 e Latin-1
    for encoding in encodings:
        try:
            with open(file=caminho_arquivo, mode='r', encoding=encoding) as arquivo:
                conteudo = arquivo.read()
                if texto_procurado in conteudo:
                    return True
        except UnicodeDecodeError:
            continue  # Se falhar, tentar com o próximo encoding
    return False

# Verifica se uma pasta existe e, se não, criá-la
def definir_diretorio_saida(diretorio: Path = Path.home() / 'Desktop' / 'teste') -> Path:
    return Path(diretorio)
    
# Função para percorrer todos os arquivos em uma pasta com uma extensão específica   
def percorrer_arquivos_em_pasta(diretorio_raiz: Path, string_pesquisa: str, extensao: str) -> list:
    
    arquivos_com_string_pesquisa = []
    diretorio_arquivos = trata_diretorio(diretorio_raiz)
    lista_de_arquivos = list(diretorio_arquivos.glob(f'*{extensao}'))
    
    if valida_extensao_de_texto(extensao):
        if not lista_de_arquivos:
            logger.info(f'Nenhum arquivo com a extensão {format_1(extensao)} foi encontrado no diretório {format_2(diretorio_arquivos)}.')
            finaliza_script()
        elif len(lista_de_arquivos) == 1:
            logger.info(f'Foi encontrado {format_4(1)} arquivo com a extensão {format_1(extensao)} na pasta {format_2(diretorio_arquivos)}.')
        elif len(lista_de_arquivos) > 1:
            logger.info(f'Foram encontrados {format_4(len(lista_de_arquivos))} arquivos com a extensão {format_1(extensao)} na pasta {format_2(diretorio_arquivos)}.')
    
    # Verifica se a string de pesquisa está presente em cada arquivo
    try:
        for arquivo in lista_de_arquivos:
            if busca_string_em_arquivo(arquivo, string_pesquisa):
                arquivos_com_string_pesquisa.append(arquivo)
    except Exception as e:
        logger.error(f'Erro ao pesquisar arquivos:\n{e}\n')
    
    return list(arquivos_com_string_pesquisa)
       
# Função para mover arquivos para o diretório de saída
def copiar_arquivos_para_saida(lista_de_arquivos: List[Path], diretorio_saida: Path, sobrescrever: bool = True, mostrar_arquivos: bool = True) -> None:
    arquivos_ignorados = 0
    arquivos_copiados = 0
    
    for arquivo in lista_de_arquivos:
        if not sobrescrever and (diretorio_saida / arquivo.name).exists():
            if mostrar_arquivos:
                logger.info(f'O arquivo {format_1(arquivo.name)} já existe no diretório de saída {format_2(diretorio_saida)}.')
            arquivos_ignorados += 1
            continue
        
        try:
            shutil.copy2(arquivo, diretorio_saida)
            if mostrar_arquivos:
                logger.info(f'O arquivo {format_1(arquivo.name)} foi movido para {format_2(diretorio_saida)} com sucesso.')
            arquivos_copiados += 1
        except Exception as e:
            logger.error(f'Erro ao mover o arquivo {arquivo.name} para {diretorio_saida}:\n{e}\n')
    
    # Exibe o número total de arquivos ignorados e copiados
    if arquivos_ignorados > 0:
        logger.info(f'Total de arquivos ignorados: {format_4(str(arquivos_ignorados))}')
    if arquivos_copiados > 0:
        logger.info(f'Total de arquivos copiados: {format_4(str(arquivos_copiados))}')
                 

def ler_diretorios_de_excel(caminho_arquivo_excel: str, nome_coluna: str = 'Caminho') -> list:
    try:
        # Caixa alta da coluna
        nome_coluna = nome_coluna.upper()
        
        # Carrega o arquivo Excel
        df = pd.read_excel(caminho_arquivo_excel)
        
        # Retorna os diretórios da coluna especificada
        return df[nome_coluna].tolist()
    
    except Exception as e:
        logger.error(f'Erro ao ler diretórios do arquivo Excel "{caminho_arquivo_excel}":\n{e}\n')
        finaliza_script_com_erro()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Define a main
def main() -> None:
     
    # Diretorios de entrada e de saída de arquivos .sql
    diretorio_scripts_entrada: Path = Path(r'C:\Users\rapha\Desktop\Input_Python\scripts_auto_service')
    diretorio_scripts_saida: Path = definir_diretorio_saida(r'C:\Users\rapha\Desktop\Output_Python\arquivos_sql')
        
    # Caminho do arquivo Excel com os diretórios que srão percorridos
    caminho_arquivo_excel: Path = diretorio_pasta_script / 'data' / 'pesquisa_arquivos_sql' / 'diretorios.xlsx'
    lista_de_diretorios = ler_diretorios_de_excel(caminho_arquivo_excel)
    
    # String e formato do arquivo de pesquisa
    string_pesquisa: str = str('Raphael Coelho')
    extensao_arquivo_pesquisa: FileExtension = '.sql'
    
    # Lista os arquivos encontrados com a string e extensão especificados e os copia para o diretório de saída
    arquivos_com_string_pesquisa: list = percorrer_arquivos_em_pasta(
                                            diretorio_raiz = diretorio_scripts_entrada,
                                            string_pesquisa = string_pesquisa,
                                            extensao = extensao_arquivo_pesquisa
                                         )
    # Copia os arquivos para o diretório de saída
    
    copiar_arquivos_para_saida(
        lista_de_arquivos = arquivos_com_string_pesquisa,
        diretorio_saida = diretorio_scripts_saida,
        sobrescrever = False,
        mostrar_arquivos = True
    )
    finaliza_script()
    
    # Define o diretório de saída dos arquivos .sql encontrados
    try:
        definir_diretorio_saida()
    except TypeError:
        logger.error(f'Para utilizar a função "{definir_diretorio_saida.__name__}" é necessário informar um diretório válido como argumento.')
        finaliza_script_com_erro()
        
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Executa a main
if __name__ == '__main__':
    main()

    
    
    # Restaure a saída padrão e a saída de erro padrão
    #sys.stdout.close()
    #sys.stderr.close()