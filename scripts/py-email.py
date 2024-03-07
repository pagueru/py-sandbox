from imap_tools import MailBox, AND, OR, NOT
import email
import sys
import os
import subprocess
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


# Configura a funcionalidade para limpar o terminal
import subprocess

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
        
# Habilita o logging para retorno de mensagens de erro e informações no terminal
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

logger = configurar_logger()
limpar_terminal()
logger = configurar_logger()




# Obtém o nome do script sem o caminho completo
nome_script = os.path.basename(sys.argv[0])

# Limpa o terminal antes de executar o script
# os.system('cls' if os.name == 'nt' else 'clear') # 'nt' para Windows e 'clear' para Linux ou macOS

# Configurações
usuario = 'rcoelho@newbacon.com'
senha = 'lhye rver omwr qwpd'

# Construindo a string de busca
remetente = 'sys_info@newbacon.com'
marcador = 'Tarefas'
data_especifica = datetime.strptime('2024-03-01', '%Y-%m-%d').date()
data_hoje = datetime.now().date()

# Conectando-se ao servidor IMAP do Gmail
mail = MailBox('imap.gmail.com')

# Get date, subject and body len of all emails from INBOX folder
def retornar_todos_emails():
    try:
        with mail.login(usuario, senha) as mailbox:
            for msg in mailbox.fetch():
                print(msg.date, msg.subject, len(msg.text or msg.html), msg.text)
    except Exception as e:
        print(e)

# Filtrar emails por remetente, assunto e label
def retornar_emails_por_filtro(remetente, marcador, data_inicio):
    try:
        with mail.login(usuario, senha, initial_folder='INBOX') as mailbox:
            # Construindo a expressão de filtro
            filter_expression = AND(from_=remetente, gmail_label=marcador, date_gte=data_inicio)
            # Iterando sobre os emails que atendem ao filtro
            for msg in mailbox.fetch(filter_expression):
                msg_html = msg.html
                return msg_html
    except Exception as e:
        print(e)
 
def criar_objeto_beautiful_soup(msg_html):
    # Criar um objeto BeautifulSoup
    soup = BeautifulSoup(msg_html, 'html.parser')
    return soup

def encontrar_partes(soup):

    texto_assunto = soup.title.text
    
    texto_projeto = soup.find('p', class_='lead')
    texto_projeto = texto_projeto.text.strip()

    texto_teste = soup.find('p', class_='CToWUd').text.strip()
    print(texto_projeto)
 
if __name__ == '__main__':
    msg_html = retornar_emails_por_filtro(remetente, marcador, data_hoje)
    soup = criar_objeto_beautiful_soup(msg_html)
    encontrar_partes(soup)