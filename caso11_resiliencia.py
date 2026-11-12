# Importa uma biblioteca necessária para as operações deste exercício.
import socket
import time
import paramiko
# Importa uma função, classe ou recurso específico de outro módulo.
from conexao import conectar, executar

# Define/atualiza `INVENTARIO_TESTE` com o valor calculado nesta linha.
INVENTARIO_TESTE = [
    # Executa esta instrução como parte do fluxo do exercício.
    {
        # Executa esta instrução como parte do fluxo do exercício.
        "nome": "SAUDAVEL",
        "host": "127.0.0.1",
        "porta": 22,
        "usuario": "r1",
    # Executa esta instrução como parte do fluxo do exercício.
    },
    {
        # Executa esta instrução como parte do fluxo do exercício.
        "nome": "SENHA-ERRADA",
        "host": "127.0.0.1",
        "porta": 22,
        "usuario": "r1",
        "senha": "senha_incorreta",
    # Executa esta instrução como parte do fluxo do exercício.
    },

    {
        # Executa esta instrução como parte do fluxo do exercício.
        "nome": "PORTA-FECHADA",
        "host": "127.0.0.1",
        "porta": 2299,
        "usuario": "r1",

    },
    # Executa esta instrução como parte do fluxo do exercício.
    {
        # Executa esta instrução como parte do fluxo do exercício.
        "nome": "SEM-RESPOSTA",
        "host": "10.255.255.1",
        "porta": 22,
        "usuario": "r1",
    # Executa esta instrução como parte do fluxo do exercício.
    },
# Executa esta instrução como parte do fluxo do exercício.
]

# Define/atualiza `TENTATIVAS` com o valor calculado nesta linha.
TENTATIVAS = 3
# Define/atualiza `ESPERA_BASE` com o valor calculado nesta linha.
ESPERA_BASE = 2


# Define uma função reutilizável; os parâmetros recebem os dados necessários para executar esta tarefa.
def classificar(erro):
    # Documenta a finalidade da função ou do trecho.
    """Retorna categoria, causa provável e se deve tentar novamente."""
    # Verifica uma condição e executa o bloco somente se ela for verdadeira.
    if isinstance(erro, paramiko.AuthenticationException):
        # Devolve o resultado ao ponto em que a função foi chamada.
        return "AUTENTICAÇÃO", "usuário ou senha inválidos", False

    # Verifica uma condição e executa o bloco somente se ela for verdadeira.
    if isinstance(erro, paramiko.ssh_exception.NoValidConnectionsError):
        # Devolve o resultado ao ponto em que a função foi chamada.
        return "CONEXÃO RECUSADA", "serviço SSH parado ou porta bloqueada", False

    # Verifica uma condição e executa o bloco somente se ela for verdadeira.
    if isinstance(erro, (socket.timeout, TimeoutError)):
        # Devolve o resultado ao ponto em que a função foi chamada.
        return "TIMEOUT", "equipamento sem resposta, rota ausente ou firewall", True

    # Verifica uma condição e executa o bloco somente se ela for verdadeira.
    if isinstance(erro, socket.gaierror):
        # Devolve o resultado ao ponto em que a função foi chamada.
        return "ENDEREÇO INVÁLIDO", "falha ao resolver o endereço", False

    # Verifica uma condição e executa o bloco somente se ela for verdadeira.
    if isinstance(erro, paramiko.SSHException):
        # Devolve o resultado ao ponto em que a função foi chamada.
        return "ERRO SSH", f"falha de protocolo: {erro}", True

    # Devolve o resultado ao ponto em que a função foi chamada.
    return "FALHA", f"{type(erro).__name__}: {erro}", False


# Define uma função reutilizável; os parâmetros recebem os dados necessários para executar esta tarefa.
def conectar_com_retry(dispositivo):
    # Define/atualiza `ultima_falha` com o valor calculado nesta linha.
    ultima_falha = None

    # Percorre os elementos da coleção, executando o bloco para cada item.
    for tentativa in range(1, TENTATIVAS + 1):
        # Inicia um bloco protegido para permitir o tratamento de possíveis falhas.
        try:
            # Devolve o resultado ao ponto em que a função foi chamada.
            return conectar(dispositivo, timeout=4), tentativa, None
        # Captura uma exceção para tratar o erro sem encerrar inesperadamente o programa.
        except Exception as erro:
            # Executa esta instrução como parte do fluxo do exercício.
            categoria, causa, repetir = classificar(erro)
            # Define/atualiza `ultima_falha` com o valor calculado nesta linha.
            ultima_falha = (categoria, causa, tentativa)

            # Verifica uma condição e executa o bloco somente se ela for verdadeira.
            if not repetir or tentativa == TENTATIVAS:
                # Interrompe imediatamente o laço atual.
                break

            # Define/atualiza `espera` com o valor calculado nesta linha.
            espera = ESPERA_BASE * (2 ** (tentativa - 1))
            # Exibe uma informação no terminal para acompanhar o resultado da execução.
            print(
                # Executa esta instrução como parte do fluxo do exercício.
                f"[{dispositivo['nome']}] tentativa {tentativa} falhou. "
                # Executa esta instrução como parte do fluxo do exercício.
                f"Nova tentativa em {espera}s."
            # Executa esta instrução como parte do fluxo do exercício.
            )
            # Aguarda o intervalo indicado antes de continuar a execução.
            time.sleep(espera)

    # Devolve o resultado ao ponto em que a função foi chamada.
    return None, None, ultima_falha


# Adiciona uma linha de resultado ao relatório final.
relatorio = []

# Percorre os elementos da coleção, executando o bloco para cada item.
for dispositivo in INVENTARIO_TESTE:
    # Executa esta instrução como parte do fluxo do exercício.
    cliente, tentativa, falha = conectar_com_retry(dispositivo)

    # Verifica uma condição e executa o bloco somente se ela for verdadeira.
    if cliente:
        # Inicia um bloco protegido para permitir o tratamento de possíveis falhas.
        try:
            # Define/atualiza `hostname` com o valor calculado nesta linha.
            hostname = executar(cliente, "hostname")[1]
            # Adiciona uma linha de resultado ao relatório final.
            relatorio.append(
                # Executa esta instrução como parte do fluxo do exercício.
                (dispositivo["nome"], "OK", f"hostname={hostname} (tentativa {tentativa})")
            # Executa esta instrução como parte do fluxo do exercício.
            )
        # Garante a execução deste bloco, ocorrendo sucesso ou erro; normalmente libera recursos.
        finally:
            # Fecha a conexão SSH e libera os recursos associados.
            cliente.close()
    # Executa este caminho quando nenhuma condição anterior foi atendida.
    else:
        # Executa esta instrução como parte do fluxo do exercício.
        categoria, causa, tentativas = falha
        # Adiciona uma linha de resultado ao relatório final.
        relatorio.append(
            # Executa esta instrução como parte do fluxo do exercício.
            (dispositivo["nome"], categoria, f"{causa} (tentativas: {tentativas})")
        # Executa esta instrução como parte do fluxo do exercício.
        )

# Exibe uma informação no terminal para acompanhar o resultado da execução.
print("\n=== RELATÓRIO FINAL ===")
# Percorre os elementos da coleção, executando o bloco para cada item.
for nome, estado, detalhe in relatorio:
    # Exibe uma informação no terminal para acompanhar o resultado da execução.
    print(f"{nome:<16} {estado:<20} {detalhe}")
