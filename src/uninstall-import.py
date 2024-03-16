#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Habita as configurações inicias para todo projeto
import config as cg

logger = cg.configurar_logger()
cg.limpar_terminal(False)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

import tkinter as tk
from tkinter import filedialog

# Função para lidar com o botão de seleção de arquivo
def selecionar_arquivo():
    arquivo_selecionado = filedialog.askopenfilename()
    logger.info(f'Arquivo selecionado: {arquivo_selecionado}')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#


# Permite a execução de comandos do sistema operacional a partir de um programa Python.
import subprocess

# Define a função para desinstalar os pacotes
def desinstalar_pacotes(entrada,nome_arquivo):

    print('funcionou')
    # Abre o arquivo e percorre cada linha
    '''with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            pacote = linha.split()[0]  # Extrair o nome do pacote
            subprocess.run(['pip', 'uninstall', '-y', pacote])  # Desinstalar o pacote'''

    logger.info('Todos os pacotes foram desinstalados.')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Chama a função para desinstalar os pacotes
if __name__ == '__main__':
    
    # Registrando a entrada do usuário
    logger.info('Você tem a opção de desinstalar os pacotes de acordo com os pacotes que você tem instalados.\n')
    
    entrada = input('--> Digite "y" para executar a função ou "n" para cancelar: ')
    print('')
    
    # Registrando a entrada do usuário
    logger.info(f'Entrada do usuário: "{entrada}"')
    
    # Cria uma instância oculta do Tkinter
    root = tk.Tk()
    
    #Make the window jump above all
    root.wm_attributes('-topmost',True)
    
    # Abre a janela de seleção de arquivo
    root.withdraw()
    arquivo_selecionado = filedialog.askopenfilename()

    # Exibe o arquivo selecionado
    logger.info(f'Arquivo selecionado: {arquivo_selecionado}')

    # Chama a função para desinstalar os pacotes do arquivo
    if entrada.lower() in ('y','yes'):
        desinstalar_pacotes(entrada,arquivo_selecionado)
    elif entrada.lower() in ('n','no'):
        logger.info('Função cancelada.')
    else:
        logger.info('Entrada inválida.')