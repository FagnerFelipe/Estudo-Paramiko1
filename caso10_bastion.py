# Importa uma função, classe ou recurso específico de outro módulo.
from conexao import conectar, executar

# O bastion recebe a primeira conexão SSH.
# Define/atualiza `bastion` com o valor calculado nesta linha.
bastion = {
    # Executa esta instrução como parte do fluxo do exercício.
    "nome": "BASTION",
    # Executa esta instrução como parte do fluxo do exercício.
    "host": "127.0.0.1",
    # Executa esta instrução como parte do fluxo do exercício.
    "porta": 22,
    # Executa esta instrução como parte do fluxo do exercício.
    "usuario": "bastion",
# Executa esta instrução como parte do fluxo do exercício.
}

# O equipamento interno está disponível pela porta 2222 através do túnel.
# Define/atualiza `alvo` com o valor calculado nesta linha.
alvo = {
    # Executa esta instrução como parte do fluxo do exercício.
    "nome": "R1-INTERNO",
    # Executa esta instrução como parte do fluxo do exercício.
    "host": "127.0.0.1",
    # Executa esta instrução como parte do fluxo do exercício.
    "porta": 2222,
    # Executa esta instrução como parte do fluxo do exercício.
    "usuario": "r1",
# Executa esta instrução como parte do fluxo do exercício.
}

# Define/atualiza `cliente_bastion` com o valor calculado nesta linha.
cliente_bastion = conectar(bastion)
# Define/atualiza `cliente_alvo` com o valor calculado nesta linha.
cliente_alvo = None
# Define/atualiza `canal` com o valor calculado nesta linha.
canal = None

# Inicia um bloco protegido para permitir o tratamento de possíveis falhas.
try:
    # Define/atualiza `transporte` com o valor calculado nesta linha.
    transporte = cliente_bastion.get_transport()

    # O bastion abre um canal TCP até o equipamento interno.
    # Define/atualiza `canal` com o valor calculado nesta linha.
    canal = transporte.open_channel(
        # Executa esta instrução como parte do fluxo do exercício.
        "direct-tcpip",
        # Define/atualiza `dest_addr` com o valor calculado nesta linha.
        dest_addr=(alvo["host"], alvo["porta"]),
        # Define/atualiza `src_addr` com o valor calculado nesta linha.
        src_addr=("127.0.0.1", 0),
    # Executa esta instrução como parte do fluxo do exercício.
    )

    # A segunda sessão SSH passa pelo canal criado acima.
    # Define/atualiza `cliente_alvo` com o valor calculado nesta linha.
    cliente_alvo = conectar(alvo, sock=canal)

    # Exibe uma informação no terminal para acompanhar o resultado da execução.
    print("Usuário:", executar(cliente_alvo, "whoami")[1])
    # Exibe uma informação no terminal para acompanhar o resultado da execução.
    print("Hostname:", executar(cliente_alvo, "hostname")[1])
    # Exibe uma informação no terminal para acompanhar o resultado da execução.
    print("Conexão SSH vista pelo destino:", executar(
        # Executa esta instrução como parte do fluxo do exercício.
        cliente_alvo, "echo $SSH_CONNECTION"
    # Executa esta instrução como parte do fluxo do exercício.
    )[1])

# Garante a execução deste bloco, ocorrendo sucesso ou erro; normalmente libera recursos.
finally:
    # Verifica uma condição e executa o bloco somente se ela for verdadeira.
    if cliente_alvo:
        # Executa esta instrução como parte do fluxo do exercício.
        cliente_alvo.close()
    # Verifica uma condição e executa o bloco somente se ela for verdadeira.
    if canal:
        # Fecha o canal SSH utilizado nesta comunicação.
        canal.close()
    # Executa esta instrução como parte do fluxo do exercício.
    cliente_bastion.close()
