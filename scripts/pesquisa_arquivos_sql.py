"""
- A ideia do script é verificar em todas as pastas de scripts quais são os scripts que eu fiz, normalmente marcados com meu nome "Raphael Coelho" neles.
- A princípio ele está pegando os casos e salvando em uma pasta diferente
- O intuito final é passar por todos esses arquivos e gerar uma lista .txt pra alimentar uma planilha Excel com os dados para falicitar o rastreio das tarefas
"""

import os
import sys
import shutil

# Função para verificar se a frase está presente no conteúdo do arquivo
def verificar_frase_arquivo(nome_arquivo: str, frase: str):
    encodings = ['utf-8', 'latin-1']  # Tentar com UTF-8 e Latin-1
    for encoding in encodings:
        try:
            with open(file=nome_arquivo, mode='r', encoding=encoding) as arquivo:
                conteudo = arquivo.read()
                if frase in conteudo:
                    return True
        except UnicodeDecodeError as e:
            continue  # Se falhar, tentar com o próximo encoding
        except Exception as e:
            sys.exit()
    return False

# Diretório onde estão os arquivos .sql
diretorio_origem = r'C:\Users\rapha\Desktop\teste'

# Frase a ser procurada nos arquivos
frase_procurada = 'Raphael Coelho'

diretorio_destino = os.path.join(diretorio_origem, 'Arquivos_Com_Frase')
os.makedirs(diretorio_destino, exist_ok=True)

# Listar todos os arquivos na pasta de origem   
arquivos = os.listdir(diretorio_origem)

# Iterar sobre os arquivos e copiar aqueles que contêm a frase
for arquivo in arquivos:
    if arquivo.endswith('.sql'):
        caminho_arquivo_origem = os.path.join(diretorio_origem, arquivo)
        if verificar_frase_arquivo(caminho_arquivo_origem, frase_procurada):
            caminho_arquivo_destino = os.path.join(diretorio_destino, arquivo)
            shutil.copy2(caminho_arquivo_origem, caminho_arquivo_destino)
            print(f'Arquivo "{arquivo}" copiado para a pasta de destino.')

print('Processo concluído.')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Define a main
def main():
    pass

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Executa a main
if __name__ == '__main__':
    main()