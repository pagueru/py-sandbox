# O módulo subprocess permite que os comandos sejam executados em segundo plano
import subprocess

# Lista de comandos a serem executados
comandos = [
    'echo "Hello, world!"',
    'ls -l',
    'git status'
]

# Itera sobre a lista de comandos e executa cada um deles
for comando in comandos:
    """
    A função subprocess.run() permite executar comandos no sistema
    operacional a partir de um script Python.
    """
    subprocess.run(comando, shell=True)  # shell=True torna o comando executável