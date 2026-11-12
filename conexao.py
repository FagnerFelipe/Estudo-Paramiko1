# Importa uma biblioteca necessária para as operações deste exercício.
import os
# Importa uma biblioteca necessária para as operações deste exercício.
import paramiko


# Define uma função reutilizável; os parâmetros recebem os dados necessários para executar esta tarefa.
def conectar(disp, timeout=10, sock=None):
    # Documenta a finalidade da função ou do trecho.
    """Abre uma conexão SSH usando os dados do inventário."""
    # Cria ou armazena o objeto/resultado que será utilizado nas próximas operações.
    cliente = paramiko.SSHClient()
    # Executa esta instrução como parte do fluxo do exercício.
    cliente.load_system_host_keys()
    # Adequado ao laboratório; em produção, valide known_hosts.
    # Executa esta instrução como parte do fluxo do exercício.
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Executa esta instrução como parte do fluxo do exercício.
    cliente.connect(
        # Define/atualiza `hostname` com o valor calculado nesta linha.
        hostname=disp["host"],
        # Define/atualiza `port` com o valor calculado nesta linha.
        port=disp.get("porta", 22),
        # Define/atualiza `username` com o valor calculado nesta linha.
        username=disp["usuario"],
        # Não executa nenhuma ação; funciona como marcador de bloco vazio.
        password=disp.get("senha", os.environ.get("SSH_SENHA")),
        # Define/atualiza `key_filename` com o valor calculado nesta linha.
        key_filename=disp.get("chave"),
        # Define/atualiza `timeout` com o valor calculado nesta linha.
        timeout=timeout,
        # Define/atualiza `banner_timeout` com o valor calculado nesta linha.
        banner_timeout=timeout,
        # Define/atualiza `auth_timeout` com o valor calculado nesta linha.
        auth_timeout=timeout,
        # Define/atualiza `look_for_keys` com o valor calculado nesta linha.
        look_for_keys=False,
        # Define/atualiza `allow_agent` com o valor calculado nesta linha.
        allow_agent=False,
        # Define/atualiza `sock` com o valor calculado nesta linha.
        sock=sock,
    # Executa esta instrução como parte do fluxo do exercício.
    )
    # Devolve o resultado ao ponto em que a função foi chamada.
    return cliente


# Define uma função reutilizável; os parâmetros recebem os dados necessários para executar esta tarefa.
def executar(cliente, comando, timeout=15):
    # Documenta a finalidade da função ou do trecho.
    """Executa um comando e retorna código, saída padrão e saída de erro."""
    # Recebe os três fluxos do comando remoto: entrada, saída padrão e saída de erro.
    stdin, stdout, stderr = cliente.exec_command(comando, timeout=timeout)
    # Define/atualiza `saida` com o valor calculado nesta linha.
    saida = stdout.read().decode(errors="replace").strip()
    # Define/atualiza `erro` com o valor calculado nesta linha.
    erro = stderr.read().decode(errors="replace").strip()
    # Armazena o código de retorno do comando; normalmente zero indica sucesso.
    codigo = stdout.channel.recv_exit_status()
    # Devolve o resultado ao ponto em que a função foi chamada.
    return codigo, saida, erro
