# Importa uma biblioteca necessária para as operações deste exercício.
import time
# Importa uma função, classe ou recurso específico de outro módulo.
from conexao import conectar, executar

# Define/atualiza `dispositivo` com o valor calculado nesta linha.
dispositivo = {
    # Executa esta instrução como parte do fluxo do exercício.
    "nome": "R1",

    "host": "127.0.0.1",
    "usuario": "r1",
    "porta": 22,
# Executa esta instrução como parte do fluxo do exercício.
}

# Define/atualiza `sequencia` com o valor calculado nesta linha.
sequencia = [
    # Executa esta instrução como parte do fluxo do exercício.
    "cd /tmp",
    "pwd",
    "export AMBIENTE=PRODUCAO",
    "echo $AMBIENTE",
]


# Define uma função reutilizável; os parâmetros recebem os dados necessários para executar esta tarefa.
def ler(canal, pausa=0.6):
    # Documenta a finalidade da função ou do trecho.
    """Aguarda um pouco e lê os dados disponíveis no canal."""
    # Aguarda o intervalo indicado antes de continuar a execução.
    time.sleep(pausa)
    # Define/atualiza `dados` com o valor calculado nesta linha.
    dados = ""
    # Repete o bloco enquanto a condição permanecer verdadeira.
    while canal.recv_ready():
        # Executa esta instrução como parte do fluxo do exercício.
        dados += canal.recv(65535).decode(errors="ignore")
        # Aguarda o intervalo indicado antes de continuar a execução.
        time.sleep(0.1)
    # Devolve o resultado ao ponto em que a função foi chamada.
    return dados


# Cria ou armazena o objeto/resultado que será utilizado nas próximas operações.
cliente = conectar(dispositivo)
# Inicia um bloco protegido para permitir o tratamento de possíveis falhas.
try:
    # Exibe uma informação no terminal para acompanhar o resultado da execução.
    print("=== SESSÃO INTERATIVA ===")
    # Define/atualiza `canal` com o valor calculado nesta linha.
    canal = cliente.invoke_shell()
    # Exibe uma informação no terminal para acompanhar o resultado da execução.
    print(ler(canal))  # Descarta/lê o banner inicial.

    # Percorre os elementos da coleção, executando o bloco para cada item.
    for comando in sequencia:
        # Interage diretamente com o canal SSH, enviando ou recebendo dados.
        canal.send(comando + "\n")
        # Exibe uma informação no terminal para acompanhar o resultado da execução.
        print(ler(canal))

    # Fecha o canal SSH utilizado nesta comunicação.
    canal.close()

    # Exibe uma informação no terminal para acompanhar o resultado da execução.
    print("=== EXEC_COMMAND: UM COMANDO POR CHAMADA ===")
    # Percorre os elementos da coleção, executando o bloco para cada item.
    for comando in sequencia:
        # Armazena o código de retorno do comando; normalmente zero indica sucesso.
        codigo, saida, erro = executar(cliente, comando)
        # Exibe uma informação no terminal para acompanhar o resultado da execução.
        print(f"{comando} -> {saida!r} (código {codigo})")
        # Verifica uma condição e executa o bloco somente se ela for verdadeira.
        if erro:
            # Exibe uma informação no terminal para acompanhar o resultado da execução.
            print(f"Erro: {erro}")
# Garante a execução deste bloco, ocorrendo sucesso ou erro; normalmente libera recursos.
finally:
    # Fecha a conexão SSH e libera os recursos associados.
    cliente.close()
