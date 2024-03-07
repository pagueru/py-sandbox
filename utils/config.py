#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
import logging

# Configura o logger para retorno de mensagens de erro e informações no terminal
def configurar_logger() -> logging.Logger:
    try:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO) 
        logger = logging.getLogger(__name__) 
        logger.setLevel(logging.INFO) 
        logger.info('Configuração do Logger executada com sucesso.')
    except Exception as e:
        logger.error(f'Erro ao criar o logger:\n{e}')
    return logger

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
import os
import subprocess

# Configura a funcionalidade para limpar o terminal
def limpar_terminal() -> None:
    try:
        # Configura o logger
        logger = configurar_logger()
        
        # Detecta automaticamente o comando de limpeza do terminal
        limpar_comando = 'cls' if os.name == 'nt' else 'clear' # 'nt' para Windows e 'clear' para Linux ou macOS
        
        # Executa o comando de limpeza do terminal
        subprocess.call(limpar_comando, shell=True)
        
        logger.info('Terminal limpo com sucesso.')
    except Exception as e:
        logger.error(f'Erro ao limpar o terminal:\n{e}')
        