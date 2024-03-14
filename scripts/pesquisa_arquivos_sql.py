#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

'''
- A ideia do script é verificar em todas as pastas de scripts quais são os scripts que eu fiz (scripts com a string 'Raphael Coelho');
- Os diretórios das pastas de scripts estão no campo 'Caminho' do arquivo C:/Users/rapha/Desktop/Github/py-sandbox/data/diretorio.xlsx;
- Preciso percorrer esse campo e verificar quais arquivos estão dentro de cada pasta;
- Após tudo preparado, deve copiar os arquivos que correspondem a string desejada para uma pasta de destino
'''

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Corrige o diretório de trabalho para chamar a importações da pasta .utils
import configurar_path as cg
cg.configurar_path()

# Importa as funcionalidades padrões do projeto
from utils.utils import *

# Configura o logger e limpa o terminal
#logger = logging.getLogger(__name__)
limpar_terminal(True)
logger = configurar_logger(__name__, 'debug')
logger_manual(logging.getLevelName(logger.level))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

#### --> Adicionar comentárioss por bibliteca
import shutil
from pathlib import Path

# Obtém o nome do script
nome_script = Path(__file__).name

# Obtém o diretório completo do script com o nome do arquivo .py
diretorio_completo_script_arquivo = Path(__file__).parent

# Obtém o diretório da pasta do script
diretorio_pasta_script = Path(__file__).parent.parent

# Mensagem de inicialização
logger.info(f'Iniciando o script {cyan(nome_script)} no diretório {green(diretorio_completo_script_arquivo)}.')

# Define se deve mostrar o log de execução das funções
logger_execucao_funcao = 'info'

@erro_execucao(logger_execucao_funcao)
def printar():
    print('teste')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Normaliza o diretório
@erro_execucao(logger_execucao_funcao)
def trata_diretorio(caminho: str) -> Path:
    try:
        return Path(os.path.normpath(caminho))
    except Exception as e:
        logger.error(f'Erro ao normalizar o diretório {red(caminho)}:\n{e}\n')
        finaliza_script_com_erro()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Verifica se uma pasta existe e, se não, criá-la
@erro_execucao(logger_execucao_funcao)
def definir_diretorio_saida(diretorio: Path = Path.home() / 'Desktop' / 'teste') -> Path:
    try:
        Path(diretorio)
    except Exception as e:
        logger.error(f'Erro ao definir o diretório {red(diretorio)}:\n{e}\n')
    return Path(diretorio)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Verifica se uma string está presente em um arquivo
@erro_execucao(logger_execucao_funcao)
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
   
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
    
# Função para percorrer todos os arquivos em uma pasta com uma extensão específica   
@erro_execucao(logger_execucao_funcao)
def percorrer_arquivos_em_pasta(diretorio_raiz: Path, string_pesquisa: str, extensao: str) -> list:

    if isinstance(diretorio_raiz, list):
        logger.info(f'Iniciando a busca de arquivos com a extensão {cyan(extensao)} na {cyan('lista de diretórios inserida')}.') 
    else:
        logger.info(f'Iniciando a busca de arquivos com a extensão {cyan(extensao)} no diretório {green(diretorio_raiz)}.') 

    arquivos_com_string_pesquisa = []
    
    for diretorio in diretorio_raiz:
        lista_de_arquivos = Path(diretorio).glob(f'*{extensao}')
        lista_de_arquivos = list(lista_de_arquivos)
        
        if valida_extensao_de_texto(extensao):
            if Path(diretorio).is_dir():
                logger.info(f'O diretório é válido: {green(diretorio)}')
                if not lista_de_arquivos:
                    logger.info(f'Nenhum arquivo com a extensão {cyan(extensao)} foi encontrado no diretório {green(diretorio)}.')
                elif len(lista_de_arquivos) == 1:
                    logger.info(f'Foi encontrado {magenta(1)} arquivo com a extensão {cyan(extensao)} na pasta {green(diretorio)}.')
                elif len(lista_de_arquivos) > 1:
                    logger.info(f'Foram encontrados {magenta(len(lista_de_arquivos))} arquivos com a extensão {cyan(extensao)} na pasta {green(diretorio)}.')
            else:
                logger.error(f'O diretório não é válido: {red(diretorio)}')
        
        try:
            for arquivo in lista_de_arquivos:
                logger.debug(f'Arquivo encontrado: {cyan(arquivo.name)}')
                if busca_string_em_arquivo(Path(arquivo), string_pesquisa):
                    arquivos_com_string_pesquisa.append(arquivo)
        except Exception as e:
            logger.error(f'Erro ao pesquisar arquivos:\n{e}\n')
    
    return arquivos_com_string_pesquisa

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
       
# Função para mover arquivos para o diretório de saída
@erro_execucao(logger_execucao_funcao)
def copiar_arquivos_para_saida(lista_de_arquivos: List[Path], diretorio_saida: Path, sobrescrever: bool = True, mostrar_arquivos: bool = True) -> None:
    arquivos_ignorados = 0
    arquivos_copiados = 0
    
    for arquivo in lista_de_arquivos:
        if not sobrescrever and (diretorio_saida / arquivo.name).exists():
            if mostrar_arquivos:
                logger.info(f'O arquivo {cyan(arquivo.name)} já existe no diretório de saída {green(diretorio_saida)}.')
            arquivos_ignorados += 1
            continue
        
        try:
            shutil.copy2(arquivo, diretorio_saida)
            if mostrar_arquivos:
                logger.info(f'O arquivo {cyan(arquivo.name)} foi movido para {green(diretorio_saida)} com sucesso.')
            arquivos_copiados += 1
        except Exception as e:
            logger.error(f'Erro ao mover o arquivo {cyan(arquivo.name)} para {green(diretorio_saida)}:\n{e}\n')
    
    # Exibe o número total de arquivos ignorados e copiados
    if arquivos_ignorados > 0:
        logger.info(f'Total de arquivos ignorados: {magenta(str(arquivos_ignorados))}')
    if arquivos_copiados > 0:
        logger.info(f'Total de arquivos copiados: {magenta(str(arquivos_copiados))}')
  
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
                 
# Função para ler diretórios de um arquivo Excel
@erro_execucao(logger_execucao_funcao)
def ler_diretorios_de_excel(caminho_arquivo_excel: str, nome_coluna: str = 'Caminho') -> list:
    try:
        # Caixa alta da coluna
        nome_coluna = nome_coluna.upper()
        
        # Carrega o arquivo Excel
        df = pd.read_excel(caminho_arquivo_excel)
        
        # Retorna os diretórios da coluna especificada
        return list(df[nome_coluna].tolist())
    
    except Exception as e:
        logger.error(f'Erro ao ler diretórios do arquivo Excel {cyan(caminho_arquivo_excel)}:\n{e}\n')
        finaliza_script_com_erro()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Define a main
def main() -> None:
     
    # Diretorios de entrada e de saída de arquivos .sql
    diretorio_scripts_entrada: Path = Path(r'C:\Users\rapha\Desktop\Input_Python\scripts_auto_service')

    # Define o diretório de saída
    diretorio_scripts_saida: Path = definir_diretorio_saida(r'C:\Users\rapha\Desktop\Output_Python\arquivos_sql')
        
    # Caminho do arquivo Excel com os diretórios que srão percorridos
    caminho_arquivo_excel: Path = diretorio_pasta_script / 'data' / 'pesquisa_arquivos_sql' / 'diretorios.xlsx'
    lista_de_diretorios: list = ler_diretorios_de_excel(caminho_arquivo_excel)
    
    # String e formato do arquivo de pesquisa
    string_pesquisa: str = str('Raphael Coelho')
    extensao_arquivo_pesquisa: FileExtension = '.sql'
    
    # Lista os arquivos encontrados com a string e extensão especificados e os copia para o diretório de saída
    arquivos_com_string_pesquisa: list = percorrer_arquivos_em_pasta(
                                            diretorio_raiz = lista_de_diretorios,
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
        logger.error(f'Para utilizar a função {definir_diretorio_saida.__name__} é necessário informar um diretório válido como argumento.')
        finaliza_script_com_erro()
          
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Executa o script chamando a função main
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(f'Erro durante a execução do script: {e}')
    
    
    # Restaure a saída padrão e a saída de erro padrão
    #sys.stdout.close()
    #sys.stderr.close()