# Importa uma biblioteca necessária para as operações deste exercício.
import json
import os
from conexao import conectar, executar

# Remove a senha do processo para testar somente a chave pública.
# Consulta ou altera recursos do ambiente do sistema operacional.
os.environ.pop("SSH_SENHA", None)

# Abre o arquivo em um contexto controlado; ele será fechado automaticamente ao sair do bloco.
with open("inventario_chave.json", encoding="utf-8") as arquivo:
    # Define/atualiza `inventario` com o valor calculado nesta linha.
    inventario = json.load(arquivo)

# Percorre os elementos da coleção, executando o bloco para cada item.
for dispositivo in inventario:
    # Cria ou armazena o objeto/resultado que será utilizado nas próximas operações.
    cliente = None
    # Inicia um bloco protegido para permitir o tratamento de possíveis falhas.
    try:
        # Cria ou armazena o objeto/resultado que será utilizado nas próximas operações.
        cliente = conectar(dispositivo)
        # Define/atualiza `usuario` com o valor calculado nesta linha.
        usuario = executar(cliente, "whoami")[1]
        # Exibe uma informação no terminal para acompanhar o resultado da execução.
        print(f"{dispositivo['nome']}: autenticado por chave como {usuario}")
    # Captura uma exceção para tratar o erro sem encerrar inesperadamente o programa.
    except Exception as erro:
        # Exibe uma informação no terminal para acompanhar o resultado da execução.
        print(f"{dispositivo['nome']}: FALHA ({type(erro).__name__}: {erro})")
    # Garante a execução deste bloco, ocorrendo sucesso ou erro; normalmente libera recursos.
    finally:
        # Verifica uma condição e executa o bloco somente se ela for verdadeira.
        if cliente:
            # Fecha a conexão SSH e libera os recursos associados.
            cliente.close()

# Teste negativo: aponta para uma chave privada inexistente.
# Define/atualiza `invalido` com o valor calculado nesta linha.
invalido = dict(inventario[0], chave="/tmp/chave_que_nao_existe")
# Inicia um bloco protegido para permitir o tratamento de possíveis falhas.
try:
    # Executa esta instrução como parte do fluxo do exercício.
    conectar(invalido)
# Captura uma exceção para tratar o erro sem encerrar inesperadamente o programa.
except Exception as erro:
    # Exibe uma informação no terminal para acompanhar o resultado da execução.
    print(f"Teste com chave inválida: {type(erro).__name__}: {erro}")
