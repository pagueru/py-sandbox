#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Inicializa o colorama
from colorama import init, Fore, Back, Style
init(autoreset=True)

def sublinhado(texto: str = '') -> str:
    '''Formata o texto para sublinhado no terminal.'''
    texto: str = str('\033[4m' + str(texto) + Style.RESET_ALL)
    return texto

def negrito(texto: str = '') -> str:
    '''Formata o texto para negrito no terminal.'''
    texto: str = str(Style.BRIGHT + str(texto) + Style.RESET_ALL)
    return texto

def italico(texto: str = '') -> str:
    '''Formata o texto para italico no terminal.'''
    texto: str = str('\x1B[3m' + str(texto) + Style.RESET_ALL)
    return texto

def format_1(texto: str = '') -> str:
    '''Formata o texto cyan no terminal.'''
    texto: str = str(Fore.CYAN + str(texto) + Style.RESET_ALL)
    return texto

def format_2(texto: str = '') -> str:
    '''Formata o texto green no terminal.'''
    texto: str = str(Fore.GREEN + str(texto) + Style.RESET_ALL)
    return texto

def format_3(texto: str = '') -> str:
    '''Formata o texto red no terminal.'''
    texto: str = str(Fore.RED + str(texto) + Style.RESET_ALL)
    return texto

def format_4(texto: str = '') -> str:
    '''Formata o texto magenta no terminal.'''
    texto: str = str(Fore.MAGENTA + str(texto) + Style.RESET_ALL)
    return texto

    
# Mapeia os níveis de log para cores correspondentes 
def format_logging(levelname: str):
    colors = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA
    }
    return f'{colors.get(levelname, "")}{levelname}{Style.RESET_ALL}'

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Habilita o logging para retorno de mensagens de erro e informações no terminal
import logging 

# class ColorFormatter(logging.Formatter):
#     # Mapeia os níveis de log para cores correspondentes
#     COLORS = {
#         'DEBUG': Fore.CYAN,
#         'INFO': Fore.WHITE,
#         'WARNING': Fore.YELLOW,
#         'ERROR': Fore.RED,
#         'CRITICAL': Fore.MAGENTA
#     }

#     def format(self, record):
#         color = self.COLORS.get(record.levelname, '')
#         if color:
#             record.name = color + record.name
#             record.levelname = color + record.levelname
#             record.msg = color + record.msg
#         return logging.Formatter.format(self, record)

# class ColorLogger(logging.Logger):
#     def __init__(self, name):
#         logging.Logger.__init__(self, name, logging.DEBUG)
#         color_formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
#         console = logging.StreamHandler()
#         console.setFormatter(color_formatter)
#         self.addHandler(console)

# logging.setLoggerClass(ColorLogger)
# logger = logging.getLogger('utils.py')

# def testa_logger_colorama() -> None:
#     logger.info('This is an info message')
#     logger.warning('This is a warning message')
#     logger.debug('This is a debug message')
#     logger.error('This is an error message')


# # Configura o logger para retorno de mensagens de erro e informações no terminal
# def configurar_logger(atributo_nome: str = __name__) -> logging.Logger:
#     try:
#         logging.basicConfig(
#             format='%(asctime)s - %(levelname)s - %(message)s',
#             level=logging.NOTSET,
#             datefmt='%Y-%m-%d %H:%M:%S'
#         )
#         logger: logging.Logger = logging.getLogger(atributo_nome)
#         logger.setLevel(logging.NOTSET)
#     except Exception as e:
#         raise Exception(f'Ocorreu um erro ao confgiurar o logger:\n{e}')
#     return logger


# Configura o logger para retorno de mensagens de erro e informações no terminal
def configurar_logger(atributo_nome: str = __name__) -> logging.Logger:
    try:
        # Define um formatador personalizado
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(levelname_formatted)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )
        
        # Adiciona um filtro para adicionar o levelname formatado
        class LevelnameFormatter(logging.Filter):
            def filter(self, record):
                record.levelname_formatted = format_logging(record.levelname)
                return True
        
        # Cria e configura o logger
        logger: logging.Logger = logging.getLogger(atributo_nome)
        logger.setLevel(logging.DEBUG)
        
        
        # Adiciona o formatador ao logger
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.addFilter(LevelnameFormatter())
        logger.addHandler(handler)
        
    except Exception as e:
        raise Exception(f'Ocorreu um erro ao configurar o logger:\n{e}')
    return logger

# Configura o logger
logger = configurar_logger('utils.py')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Permite funcionalidades para interações com o sistema
import os

# Permite que os comandos sejam executados em segundo plano
import subprocess

# Configura a funcionalidade para limpar o terminal
def limpar_terminal(bool: bool = True) -> None:
    try:

        # Detecta automaticamente o comando de limpeza do terminal
        limpar_comando = 'cls' if os.name == 'nt' else 'clear'  # 'nt' para Windows e 'clear' para Linux ou macOS

        # Executa o comando de limpeza do terminal
        subprocess.run(limpar_comando, shell=True, check=True)

        if bool:
            logger.info('Terminal limpo com sucesso.')
            print('----------------------------------------------------------')
        else:
            logger.error(f'Insira "True" ou "False" como parâmetro')
            
    except subprocess.CalledProcessError as e:
        logger.error(f'Erro ao limpar o terminal:\n{e}')
    except Exception as e:
        logger.exception(f'Erro desconhecido ao limpar o terminal: \n{e}')
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Permite que os comandos sejam executados em segundo plano
import subprocess

 # Permite a tipagem de parâmetros
from typing import List
        
# Permite que os comandos sejam executados em segundo plano
def executar_comandos_bash(comandos: List[str]) -> None:  # type: ignore
    for comando in comandos:
        # Permite executar comandos no sistema operacional a partir de um script Python.
        subprocess.run(comando, shell=True) # shell=True torna o comando executável
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

from tabulate import tabulate as tb
import pandas as pd

# Formatação do DataFrame com bordas redondas
def formatar_dataframe(dataframe: pd.DataFrame, flag: bool=False) -> pd.DataFrame:
    try: 
        if flag:
            print(tb(dataframe, headers='keys', tablefmt='rounded_grid'))
        else:
            print(tb(dataframe.head(), headers='keys', tablefmt='rounded_grid'))
    except Exception as e:
        logger.error(f'Ocorreu um erro ao formatar o DataFrame:\n{e}\n')
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Permite a tipagem de parâmetros
from typing import NewType, NoReturn, Callable

# Finaliza o script
def finaliza_script() -> NoReturn:
    logger.info(f'Finalizando o script...')
    exit()
    
# Finaliza o script com erro
def finaliza_script_com_erro() -> NoReturn:
    logger.info(f'Finalizando o script devido a um erro.')
    exit()

# Declara um tipo extensões de arquivos (exemplo: '.csv', '.txt', '.py'...)
FileExtension = NewType('FileExtension', str)

def valida_extensao_de_texto(extensao: FileExtension) -> bool:
    # Lista de extensões de texto válidas
    text_extensions = ['.sql','.txt', '.csv', '.json', '.xml', '.html', '.md', '.log', '.env', '.yml', '.yaml', '.py']
    
    if extensao.find('.') == -1:
        logger.error(f'A string "{extensao}" não é uma extensão válida de arquivo.')
        exit()

    if extensao.lower() in text_extensions:
        return True
    else:
        logger.info(f'A extensão "{extensao}" não está na lista de extensões válidas. É possível que ocorram erros no script.')
        return True

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Permite funcionalidades para interações com o sistema
import sys

import pathlib as Path

def configurar_arquivo_log(diretorio_do_arquivo: Path = None) -> None:
    
    if diretorio_do_arquivo is None:
        with os.path.dirname(os.getcwd()) as diretorio_raiz:
            diretorio_do_arquivo = os.path.join(diretorio_raiz,'data','log.txt')
            logger.info(f'Arquivo de log definido no diretório: {diretorio_do_arquivo}')
    else:
        sys.stdout = diretorio_do_arquivo
        sys.stderr = diretorio_do_arquivo
        logger.info(f'Arquivo de log definido no diretório: {diretorio_do_arquivo}')


diretorio_do_arquivo = os.path.join(os.path.dirname(os.getcwd()),'data','log.txt')

print(diretorio_do_arquivo)

# Restaure a saída padrão e a saída de erro padrão
#sys.stdout.close()
#sys.stderr.close()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Definição de decorators
from functools import wraps

def erro_execucao(func: Callable) -> Callable:
    '''Decorator para capturar e registrar erros ao executar uma função.'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f'Erro ao executar a função {func.__name__}:\n{e}')
    return wrapper