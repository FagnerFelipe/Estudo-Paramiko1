# Importa uma biblioteca necessária para as operações deste exercício.
import hashlib
# Importa uma biblioteca necessária para as operações deste exercício.
import json
# Importa uma função, classe ou recurso específico de outro módulo.
from conexao import conectar, executar

# Define/atualiza `LOCAL` com o valor calculado nesta linha.
LOCAL = "coleta.sh"
# Define/atualiza `REMOTO` com o valor calculado nesta linha.
REMOTO = "coleta.sh"


# Define uma função reutilizável; os parâmetros recebem os dados necessários para executar esta tarefa.
def sha256_local(caminho):
    # Armazena o resumo criptográfico usado para conferir a integridade do arquivo.
    hash_arquivo = hashlib.sha256()
    # Abre o arquivo em um contexto controlado; ele será fechado automaticamente ao sair do bloco.
    with open(caminho, "rb") as arquivo:
        # Percorre os elementos da coleção, executando o bloco para cada item.
        for bloco in iter(lambda: arquivo.read(8192), b""):
            # Armazena o resumo criptográfico usado para conferir a integridade do arquivo.
            hash_arquivo.update(bloco)
    # Devolve o resultado ao ponto em que a função foi chamada.
    return hash_arquivo.hexdigest()


# Define uma função reutilizável; os parâmetros recebem os dados necessários para executar esta tarefa.
def distribuir(dispositivo, hash_local):
    # Cria ou armazena o objeto/resultado que será utilizado nas próximas operações.
    cliente = conectar(dispositivo)
    # Guarda a sessão SFTP para transferir ou manipular arquivos remotamente.
    sftp = None

    # Inicia um bloco protegido para permitir o tratamento de possíveis falhas.
    try:
        # Guarda a sessão SFTP para transferir ou manipular arquivos remotamente.
        sftp = cliente.open_sftp()
        # Define/atualiza `caminho_remoto` com o valor calculado nesta linha.
        caminho_remoto = f"/home/{dispositivo['usuario']}/{REMOTO}"
        # Executa uma operação de arquivo remoto por meio do protocolo SFTP.
        sftp.put(LOCAL, caminho_remoto)
        # Executa uma operação de arquivo remoto por meio do protocolo SFTP.
        sftp.chmod(caminho_remoto, 0o755)
    # Garante a execução deste bloco, ocorrendo sucesso ou erro; normalmente libera recursos.
    finally:
        # Verifica uma condição e executa o bloco somente se ela for verdadeira.
        if sftp:
            # Encerra a sessão SFTP e libera o canal utilizado para transferência de arquivos.
            sftp.close()

    # Armazena o código de retorno do comando; normalmente zero indica sucesso.
    codigo, saida, erro = executar(cliente, f"sha256sum {caminho_remoto}")
    # Verifica uma condição e executa o bloco somente se ela for verdadeira.
    if codigo != 0:
        # Gera uma exceção para sinalizar que a operação não pode continuar normalmente.
        raise RuntimeError(erro or "Não foi possível calcular o hash remoto.")

    # Armazena o resumo criptográfico usado para conferir a integridade do arquivo.
    hash_remoto = saida.split()[0]
    # Verifica uma condição e executa o bloco somente se ela for verdadeira.
    if hash_remoto != hash_local:
        # Devolve o resultado ao ponto em que a função foi chamada.
        return "ABORTADO: hash diferente"

    # Armazena o código de retorno do comando; normalmente zero indica sucesso.
    codigo, saida, erro = executar(cliente, f"bash {caminho_remoto}")
    # Verifica uma condição e executa o bloco somente se ela for verdadeira.
    if codigo != 0:
        # Devolve o resultado ao ponto em que a função foi chamada.
        return f"Arquivo íntegro, mas houve falha na execução: {erro}"

    # Devolve o resultado ao ponto em que a função foi chamada.
    return "ÍNTEGRO E EXECUTADO\n" + saida


# Armazena o resumo criptográfico usado para conferir a integridade do arquivo.
hash_local = sha256_local(LOCAL)
# Exibe uma informação no terminal para acompanhar o resultado da execução.
print(f"Hash local: {hash_local}\n")

# Abre o arquivo em um contexto controlado; ele será fechado automaticamente ao sair do bloco.
with open("inventario.json", encoding="utf-8") as arquivo:
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
        # Exibe uma informação no terminal para acompanhar o resultado da execução.
        print(f"[{dispositivo['nome']}] {distribuir(dispositivo, hash_local)}\n")
    # Captura uma exceção para tratar o erro sem encerrar inesperadamente o programa.
    except Exception as erro:
        # Exibe uma informação no terminal para acompanhar o resultado da execução.
        print(f"[{dispositivo['nome']}] FALHA ({type(erro).__name__}: {erro})")
    # Garante a execução deste bloco, ocorrendo sucesso ou erro; normalmente libera recursos.
    finally:
        # Verifica uma condição e executa o bloco somente se ela for verdadeira.
        if cliente:
            # Fecha a conexão SSH e libera os recursos associados.
            cliente.close()
