#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Habita as configurações inicias para todo projeto
import config as cg

logger = cg.configurar_logger()
cg.limpar_terminal(False)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Lista de comandos a serem executados
comandos = [
    'echo "Hello, world!"',
    'ls -l',
    'git status'
]

cg.executar_comandos_bash(comandos)