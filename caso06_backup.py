# Importa uma biblioteca necessária para as operações deste exercício.
import json
# Importa uma biblioteca necessária para as operações deste exercício.
import logging
# Importa uma função, classe ou recurso específico de outro módulo.
from datetime import datetime
# Importa uma função, classe ou recurso específico de outro módulo.
from pathlib import Path
# Importa uma função, classe ou recurso específico de outro módulo.
from conexao import conectar

# Define/atualiza `RETENCAO` com o valor calculado nesta linha.
RETENCAO = 5
# Define/atualiza `ARQUIVO_REMOTO` com o valor calculado nesta linha.
ARQUIVO_REMOTO = "dispositivo.cfg"

# Registra uma mensagem no arquivo de log com o nível de severidade correspondente.
logging.basicConfig(
    # Define/atualiza `filename` com o valor calculado nesta linha.
    filename="backup.log",
    # Define/atualiza `level` com o valor calculado nesta linha.
    level=logging.INFO,
    # Define/atualiza `format` com o valor calculado nesta linha.
    format="%(asctime)s %(levelname)s %(message)s",
# Executa esta instrução como parte do fluxo do exercício.
)


# Define uma função reutilizável; os parâmetros recebem os dados necessários para executar esta tarefa.
def fazer_backup(dispositivo):
    # Define/atualiza `pasta` com o valor calculado nesta linha.
    pasta = Path("backups") / dispositivo["nome"]
    # Cria a pasta de destino; exist_ok evita erro caso ela já exista.
    pasta.mkdir(parents=True, exist_ok=True)

    # Define/atualiza `nome` com o valor calculado nesta linha.
    nome = datetime.now().strftime("%Y-%m-%d_%H%M%S.cfg")
    # Define/atualiza `destino` com o valor calculado nesta linha.
    destino = pasta / nome

    # Cria ou armazena o objeto/resultado que será utilizado nas próximas operações.
    cliente = conectar(dispositivo)
    # Guarda a sessão SFTP para transferir ou manipular arquivos remotamente.
    sftp = None
    # Inicia um bloco protegido para permitir o tratamento de possíveis falhas.
    try:
        # Guarda a sessão SFTP para transferir ou manipular arquivos remotamente.
        sftp = cliente.open_sftp()
        # Define/atualiza `caminho_remoto` com o valor calculado nesta linha.
        caminho_remoto = f"/home/{dispositivo['usuario']}/{ARQUIVO_REMOTO}"
        # Executa uma operação de arquivo remoto por meio do protocolo SFTP.
        sftp.get(caminho_remoto, str(destino))
    # Garante a execução deste bloco, ocorrendo sucesso ou erro; normalmente libera recursos.
    finally:
        # Verifica uma condição e executa o bloco somente se ela for verdadeira.
        if sftp:
            # Encerra a sessão SFTP e libera o canal utilizado para transferência de arquivos.
            sftp.close()
        # Fecha a conexão SSH e libera os recursos associados.
        cliente.close()

    # Mantém somente os cinco arquivos mais recentes.
    # Define/atualiza `arquivos` com o valor calculado nesta linha.
    arquivos = sorted(pasta.glob("*.cfg"))
    # Define/atualiza `antigos` com o valor calculado nesta linha.
    antigos = arquivos[:-RETENCAO]
    # Percorre os elementos da coleção, executando o bloco para cada item.
    for arquivo in antigos:
        # Executa esta instrução como parte do fluxo do exercício.
        arquivo.unlink()

    # Devolve o resultado ao ponto em que a função foi chamada.
    return destino, len(antigos)


# Abre o arquivo em um contexto controlado; ele será fechado automaticamente ao sair do bloco.
with open("inventario.json", encoding="utf-8") as arquivo:
    # Define/atualiza `inventario` com o valor calculado nesta linha.
    inventario = json.load(arquivo)

# Percorre os elementos da coleção, executando o bloco para cada item.
for dispositivo in inventario:
    # Inicia um bloco protegido para permitir o tratamento de possíveis falhas.
    try:
        # Executa esta instrução como parte do fluxo do exercício.
        destino, removidos = fazer_backup(dispositivo)
        # Registra uma mensagem no arquivo de log com o nível de severidade correspondente.
        logging.info("%s: backup OK em %s", dispositivo["nome"], destino)
        # Exibe uma informação no terminal para acompanhar o resultado da execução.
        print(f"{dispositivo['nome']}: OK -> {destino} (removidos: {removidos})")
    # Captura uma exceção para tratar o erro sem encerrar inesperadamente o programa.
    except Exception as erro:
        # Registra uma mensagem no arquivo de log com o nível de severidade correspondente.
        logging.error("%s: backup FALHOU (%s)", dispositivo["nome"], erro)
        # Exibe uma informação no terminal para acompanhar o resultado da execução.
        print(f"{dispositivo['nome']}: FALHA ({type(erro).__name__}: {erro})")
