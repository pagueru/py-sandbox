import pandas as pd
import os
import locale
from os import getenv
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Configura o idioma para português
locale.setlocale(locale.LC_TIME, 'pt_BR')

# Obtém os valores para as variáveis através do arquivo tokens.env
load_dotenv('tokens.env')

# Carregamento e Leitura do arquivo para DataFrame
caminho_do_arquivo = getenv(r'CAMINHO_ARQUIVO')
leitura_da_tabela = pd.read_excel(caminho_do_arquivo)

# Exemplo: ['Nortriptilina', 'Clomipramina', 'Melatonina', 'Vitamina', 'Ritalina', 'Teste']
lista_de_medicamentos = leitura_da_tabela['MEDICAMENTOS'].str.capitalize().tolist()

# Adiciona um índice a lista_medicamento: ['1. Nortriptilina', '2. Clomipramina', '3. Melatonina', '4. Vitamina', '5. Ritalina', '6. Teste']
lista_de_medicamentos_enumerada = [f'{i + 1}. {medicamento}' for i, medicamento in enumerate(lista_de_medicamentos)]





# Tratamento_de_exceções
def tratamento_de_exceções():

    os.system('cls')
    try:
        leitura_da_tabela

    except pd.errors.EmptyDataError as mensagem_error:
        print('A tabela parecer estar vazia 😥')
        print(f'Segue a mensagem de erro: {mensagem_error}')        
        return None, None

    except FileNotFoundError as mensagem_error:
        print('O arquivo parece não ter sido encontrado 😥')
        print(f'Segue a mensagem de erro: {mensagem_error}')          
        return None, None

    except Exception as mensagem_error:
        print(f'Ocorreu um erro na leitura da tabela 😥')
        print(f'Segue a mensagem de erro: {mensagem_error}')   
        return None, None

# Obter_indice_medicamento
def obter_indice_medicamento(nome_do_medicamento):
    """
    Obtém o índice da linha correspondente ao medicamento na tabela.

    Parameters:
    - nome_do_medicamento (str): O nome do medicamento a ser procurado.

    Returns:
    - list: Uma lista contendo os índices das linhas correspondentes ao medicamento.
    """
    
    fg_obter_indice = leitura_da_tabela.index[leitura_da_tabela['MEDICAMENTOS'].str.capitalize() == nome_do_medicamento.capitalize()].tolist()

    if not fg_obter_indice:
        return []

    return fg_obter_indice

# Atualizar tabela
def carregar_arquivo():

    for linha, coluna in leitura_da_tabela.iterrows():
        if not pd.isnull(coluna['MEDICAMENTOS']):
            fg_dupla = coluna['FG_DUPLA']
            estoque = coluna['ESTOQUE_ATT']

            dt_fim = (datetime.now() + timedelta(days=estoque if fg_dupla == 1 else estoque/2)).strftime('%Y-%m-%d')
            dias_faltantes = (datetime.strptime(dt_fim, '%Y-%m-%d') - datetime.now()).days

            leitura_da_tabela.at[linha, 'DT_FIM'] = dt_fim
            leitura_da_tabela.at[linha, 'DIAS_FALTANTES'] = dias_faltantes

    leitura_da_tabela.to_excel(caminho_do_arquivo, index=False) #salvamento da tabela

# Lista de medicamentos
def obter_lista_medicamentos():

    try:
        return lista_de_medicamentos
    
    except Exception as e:
        print(f'Erro ao ler a tabela do Excel: {e}')
        return []

# Consultar medicamentos
def consultar_medicamento():

    # Tratamento dos erros no carregamento da tabela
    tratamento_de_exceções()
 
    while True :

        # Input do usuário
        input_medicamento = str(input('Digite o nome do medicamento: ')).capitalize()

        # Obtém o índice da linha correspondente ao medicamento na tabela
        indice_linha = obter_indice_medicamento(input_medicamento)
        
        if not indice_linha:
            continue


        # Se o índice for 0 ou se o usuário optar por tentar novamente
        if not indice_linha or (not indice_linha and not input_medicamento):
            #os.system('cls')
            print(f'Parece que o medicamento {input_medicamento} não existe. 😥\n')
            print('Gostaria de tentar novamente ou retornar ao menu?')
            print('1. Tentar novamente')
            print('2. Retornar ao menu')
            escolha_binaria = input('\n➔ ')

            if escolha_binaria not in ['1', '2']:
                print('Opção inválida')
                continue

            elif escolha_binaria == '1':
                consultar_medicamento()

            elif escolha_binaria == '2':
                menu_numérico()  

        # Carregamento dos dias faltantes para acabar
        dias_faltantes = int(leitura_da_tabela.at[indice_linha[0], 'DIAS_FALTANTES'])
        dt_fim = leitura_da_tabela.at[indice_linha[0], 'DT_FIM']       
        dt_fim = datetime.strptime(dt_fim, '%Y-%m-%d').strftime('%A, dia %d/%m')

        # Erro caso não encontre o medicamento na tabela
        if dias_faltantes <= 0:
            #os.system('cls')
            print(f'\nParece que o medicamento {input_medicamento} acabou no dia {dt_fim}  😥')
            break

        elif dias_faltantes == 0:
            #os.system('cls')
            print(f'\nParece que o medicamento {input_medicamento} acaba hoje 😨')
            break

        elif dias_faltantes is not None:
            input_medicamento = input_medicamento.capitalize()
            #os.system('cls')
            print(f'Faltam {dias_faltantes} dias para o medicamento \033[4m{input_medicamento}\033[0m acabar (previsto para {dt_fim})')
        break

# Adicionar medicamento
def adicionar_medicamento():

    # Tratamento dos erros no carregamento da tabela
    tratamento_de_exceções()

    input_medicamento = input('Qual o nome do medicamento que será adicionado? ').capitalize()


    if input_medicamento in leitura_da_tabela:
        print(f'O medicamento {input_medicamento} já existe.')
        print('\nO que gostaria de fazer?')
        print('1. Alterar o medicamento escolhido')
        print('2. Escolher um novo nome')
        opcao_alteracao = input('\nDigite o número correspondente à opção desejada: ')

        if opcao_alteracao == '1':
            alterar_medicamento(caminho_do_arquivo)

        elif opcao_alteracao == '2':
            adicionar_medicamento(caminho_do_arquivo)

    unidades = int(input('Quantas unidades uma nova cartela ou caixa possui? '))
    estoque = int(input('Quantas unidades você tem hoje? '))
    opcao_binaria = input('O medicamento será dividido entre vocês 2? (S/N): ').upper()
    fg_dupla = opcao_binaria
    fg_dupla = 1 if fg_dupla == 'S' else 2
    dt_att = datetime.now().strftime('%Y-%m-%d')

    dt_fim = (datetime.now() + timedelta(days=estoque if fg_dupla == 1 else estoque/2)).strftime('%Y-%m-%d')
    dias_faltantes = (datetime.strptime(dt_fim, '%Y-%m-%d') - datetime.now()).days


    novo_medicamento = pd.DataFrame({
        'MEDICAMENTOS': [input_medicamento.capitalize()],
        'UNIDADES': [unidades],
        'ESTOQUE_ATT': [estoque],
        'FG_DUPLA': [fg_dupla],
        'DT_ATT': [dt_att],
        'DT_FIM': [dt_fim],
        'DIAS_FALTANTES': [dias_faltantes]
    })

    try:
        tabela_atualizada = pd.concat([leitura_da_tabela, novo_medicamento], ignore_index=True)
        tabela_atualizada.to_excel(caminho_do_arquivo, index=False)
        print(f'Medicamento {input_medicamento} adicionado com sucesso!')
        return
    except Exception as e:
        print(f'Erro ao adicionar o medicamento: {e}')

# Alterar medicamento
def alterar_medicamento():
    
    while True:

        tratamento_de_exceções()

        input_medicamento = input('Digite o nome do medicamento a ser alterado: ').lower().capitalize()


        
        # Procura o índice da linha que contém o medicamento
        indice_linha = leitura_da_tabela.index[leitura_da_tabela['MEDICAMENTOS'] == input_medicamento].tolist()


        if not indice_linha:
            print(f'Medicamento não encontrado.')
            continue

        # Defina a flag_sair antes do segundo loop
        flag_sair = False

        while True:
            print('\nEscolha o que deseja modificar:')
            print('1. Nome do medicamento')
            print('2. Unidades')
            print('3. Estoque')
            print('4. Uso dividido')
            opcao_alteracao = input('\nDigite o número correspondente à opção desejada: ')

            if opcao_alteracao not in ['1', '2', '3', '4']:
                print('Opção inválida.')
                continue

            elif opcao_alteracao == '1':
                novo_nome = input('Digite o novo nome do medicamento: ')
                leitura_da_tabela.at[indice_linha[0], 'MEDICAMENTOS'] = str(novo_nome)

            elif opcao_alteracao == '2':
                nova_unidade = input('Digite a quantidade de comprimidos ou cápsulas: ')
                leitura_da_tabela.at[indice_linha[0], 'UNIDADES'] = int(nova_unidade)
                print('Quantidade alterada com sucesso!')

            elif opcao_alteracao == '3':
                novo_estoque = input('Digite o valor do estoque atual: ')
                leitura_da_tabela.at[indice_linha[0], 'ESTOQUE_ATT'] = int(novo_estoque)
                print('Estoque atual alterado com sucesso!')

            elif opcao_alteracao == '4':
                print('\nComo gostaria de tomar o medicamento?')
                print('1. Se o medicamento for tomado sozinho')
                print('2. Se o medicamento for dividido entre vocês dois')
                novo_dupla = input('\nDigite o número correspondente à opção desejada: ')
                leitura_da_tabela.at[indice_linha[0], 'FG_DUPLA'] = int(novo_dupla)
                print('Duplicidades do medicamento alterado com sucesso!')

            else:
                print('\nOpção inválida.')
                continue

            # Perguntar ao usuário sobre as opções
            while True:
                print('\nGostaria de realizar mais alterações? ')
                print('1. Realizar mais alterações no mesmo medicamento')
                print('2. Realizar alterações em outro medicamento')
                print('3. Retornar para o menu principal')
                print('4. Finalizar as consultas')
                opcao_alteracao = input('\nDigite o número correspondente à opção desejada: ')

                if opcao_alteracao not in ['1', '2', '3', '4']:
                    print('Opção inválida.')
                    continue

                elif opcao_alteracao == '1':
                    break

                elif opcao_alteracao == '2':
                    flag_sair = True
                    break

                elif opcao_alteracao == '3':
                    leitura_da_tabela.to_excel(caminho_do_arquivo, index=False)
                    menu_numérico(caminho_do_arquivo)
                    return

                elif opcao_alteracao == '4':
                    print('\n### Encerrando a consulta ###\n')
                    exit()

            # Verificar flag_sair antes de sair do primeiro loop
            if flag_sair:
                break

# Remover medicamento
def remover_medicamento():
    try:
        tabela
    except Exception as e:
        print(f'Erro ao ler a tabela do Excel: {e}')
        return

    nome_medicamento = input('Digite o nome do medicamento que deseja remover: ').lower().capitalize()

    # Converte todos os nomes da tabela para minúsculas e aplica capitalize()
    tabela['MEDICAMENTOS'] = tabela['MEDICAMENTOS'].str.lower().apply(lambda x: x.capitalize())

    # Procura o índice da linha que contém o medicamento
    indice_linha = tabela.index[tabela['MEDICAMENTOS'] == nome_medicamento].tolist()

    if not indice_linha:
        print('Medicamento não encontrado.')
        return

    # Mostra as informações do medicamento a ser removido
    print('\nInformações do medicamento a ser removido:')

    medicamento_remover = tabela.loc[indice_linha[0]]

    for coluna, valor in medicamento_remover.items():
        print(f'{coluna}: {valor}')


    # Pede confirmação para remoção
    opcao_binaria = input('\nTem certeza de que deseja remover este medicamento? (S/N): ').upper()

    if opcao_binaria == 'S':
        tabela = tabela.drop(indice_linha[0], axis=0).reset_index(drop=True)
        tabela.to_excel(caminho_do_arquivo, index=False)
        print(f'Medicamento "{nome_medicamento}" removido com sucesso!')

    elif opcao_binaria == 'N':
        print('Remoção cancelada.')

    else:
        print('Opção inválida.')

# Menu principal de escolhas
def menu_numérico():

    fg_encontrado = 0

    while True:
        os.system('cls')
        print('Escolha uma das opções:')
        print('1. Consultar um medicamento')
        print('2. Adicionar um novo medicamento')
        print('3. Listar todos os medicamentos')
        print('4. Modificar um medicamento')
        print('5. Apagar um medicamento')       
        opção_do_menu = input('\nDigite o número correspondente à opção desejada: ')

        if opção_do_menu not in ['1','2','3','4','5']:
            print('Opção inválida.')
            continue
        
        elif opção_do_menu == '1':
            consultar_medicamento()

        elif opção_do_menu == '2':
            adicionar_medicamento(caminho_do_arquivo)

        elif opção_do_menu == '3':
            lista_medicamentos = obter_lista_medicamentos(caminho_do_arquivo)
            print('\nLista de medicamentos disponíveis:')
            for medicamento in lista_medicamentos:
                print(medicamento)

        elif opção_do_menu == '4':
            alterar_medicamento(caminho_do_arquivo)

        elif opção_do_menu == '5':
            remover_medicamento(caminho_do_arquivo)

        while True:
            print('\nGostaria de realizar outra operação?')
            print('1. Sim')
            print('2. Não')
            opção_binaria = input('\n➔ ')

            if opção_binaria not in ['1', '2']:
                #os.system('cls')
                print('Opção inválida\n')
                
            elif opção_binaria == '1':
                break
            elif opção_binaria == '2':
                exit()


    
def main():
    tratamento_de_exceções()
    carregar_arquivo()
    menu_numérico()


if __name__ == "__main__":
    main()