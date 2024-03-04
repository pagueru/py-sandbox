import subprocess

# Define a função para desinstalar os pacotes
def desinstalar_pacotes(nome_arquivo):

    # Abre o arquivo e percorre cada linha
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            pacote = linha.split()[0]  # Extrair o nome do pacote
            subprocess.run(['pip', 'uninstall', '-y', pacote])  # Desinstalar o pacote

    print('Todos os pacotes foram desinstalados.')


# Chama a função para desinstalar os pacotes
if __name__ == "__main__":
    
    # Atribui a variável de diretório
    nome_arquivo = 'lista_de_pacotes.txt'

    # Chama a função para desinstalar os pacotes do arquivo
    desinstalar_pacotes(nome_arquivo)