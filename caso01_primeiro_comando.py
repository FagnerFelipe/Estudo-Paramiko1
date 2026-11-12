# Importa uma função, classe ou recurso específico de outro módulo.
from conexao import conectar, executar

# Define/atualiza `dispositivo` com o valor calculado nesta linha.
dispositivo = {
    # Executa esta instrução como parte do fluxo do exercício.
    "nome": "R1",
    "host": "127.0.0.1",
    "porta": 22,
    "usuario": "r1",}

# Define/atualiza `comandos` com o valor calculado nesta linha.
comandos = ["whoami", "hostname", "uptime -p", "comando-inexistente"]

# Cria ou armazena o objeto/resultado que será utilizado nas próximas operações.
cliente = conectar(dispositivo)
# Inicia um bloco protegido para permitir o tratamento de possíveis falhas.
try:
    # Percorre os elementos da coleção, executando o bloco para cada item.
    for comando in comandos:
        # Armazena o código de retorno do comando; normalmente zero indica sucesso.
        codigo, saida, erro = executar(cliente, comando)

        # Exibe uma informação no terminal para acompanhar o resultado da execução.
        print(f"$ {comando}")
        print(f"Código: {codigo}")
        print(f"Saída: {saida or '(vazia)'}")
        print(f"Erro: {erro or '(vazio)'}")
        print()
# Garante a execução deste bloco, ocorrendo sucesso ou erro; normalmente libera recursos.
finally:
    # Fecha a conexão SSH e libera os recursos associados.
    cliente.close()
