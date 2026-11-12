# Importa uma biblioteca necessária para as operações deste exercício.
import difflib
import json
# Importa uma função, classe ou recurso específico de outro módulo.
from conexao import conectar

# Define/atualiza `IGNORAR` com o valor calculado nesta linha.
IGNORAR = ("hostname=",)


# Define uma função reutilizável; os parâmetros recebem os dados necessários para executar esta tarefa.
def normalizar(linhas):
    # Devolve o resultado ao ponto em que a função foi chamada.
    return sorted(
        # Executa esta instrução como parte do fluxo do exercício.
        linha.strip()
        # Percorre os elementos da coleção, executando o bloco para cada item.
        for linha in linhas
        # Verifica uma condição e executa o bloco somente se ela for verdadeira.
        if linha.strip() and not linha.strip().startswith(IGNORAR)
    # Executa esta instrução como parte do fluxo do exercício.
    )


# Define uma função reutilizável; os parâmetros recebem os dados necessários para executar esta tarefa.
def ler_remoto(dispositivo):
    # Cria ou armazena o objeto/resultado que será utilizado nas próximas operações.
    cliente = conectar(dispositivo)
    # Guarda a sessão SFTP para transferir ou manipular arquivos remotamente.
    sftp = None
    # Inicia um bloco protegido para permitir o tratamento de possíveis falhas.
    try:
        # Guarda a sessão SFTP para transferir ou manipular arquivos remotamente.
        sftp = cliente.open_sftp()
        # Define/atualiza `caminho` com o valor calculado nesta linha.
        caminho = f"/home/{dispositivo['usuario']}/dispositivo.cfg"
        # Abre um recurso em contexto controlado, garantindo seu fechamento ao sair do bloco.
        with sftp.open(caminho, "r") as arquivo:
            # Devolve o resultado ao ponto em que a função foi chamada.
            return arquivo.read().decode("utf-8").splitlines()
    # Garante a execução deste bloco, ocorrendo sucesso ou erro; normalmente libera recursos.
    finally:
        # Verifica uma condição e executa o bloco somente se ela for verdadeira.
        if sftp:
            # Encerra a sessão SFTP e libera o canal utilizado para transferência de arquivos.
            sftp.close()
        # Fecha a conexão SSH e libera os recursos associados.
        cliente.close()


# Abre o arquivo em um contexto controlado; ele será fechado automaticamente ao sair do bloco.
with open("referencia.cfg", encoding="utf-8") as arquivo:
    # Define/atualiza `referencia` com o valor calculado nesta linha.
    referencia = normalizar(arquivo.read().splitlines())

# Abre o arquivo em um contexto controlado; ele será fechado automaticamente ao sair do bloco.
with open("inventario.json", encoding="utf-8") as arquivo:
    # Define/atualiza `inventario` com o valor calculado nesta linha.
    inventario = json.load(arquivo)

# Define/atualiza `nao_conformes` com o valor calculado nesta linha.
nao_conformes = 0

# Percorre os elementos da coleção, executando o bloco para cada item.
for dispositivo in inventario:
    # Inicia um bloco protegido para permitir o tratamento de possíveis falhas.
    try:
        # Define/atualiza `atual` com o valor calculado nesta linha.
        atual = normalizar(ler_remoto(dispositivo))
        # Define/atualiza `diferenças` com o valor calculado nesta linha.
        diferencas = list(
            # Executa esta instrução como parte do fluxo do exercício.
            difflib.unified_diff(
                # Executa esta instrução como parte do fluxo do exercício.
                referencia,
                # Executa esta instrução como parte do fluxo do exercício.
                atual,
                # Define/atualiza `fromfile` com o valor calculado nesta linha.
                fromfile="referencia",
                # Define/atualiza `tofile` com o valor calculado nesta linha.
                tofile=dispositivo["nome"],
                # Define/atualiza `lineterm` com o valor calculado nesta linha.
                lineterm="",
            # Executa esta instrução como parte do fluxo do exercício.
            )
        # Executa esta instrução como parte do fluxo do exercício.
        )

        # Verifica uma condição e executa o bloco somente se ela for verdadeira.
        if diferencas:
            # Executa esta instrução como parte do fluxo do exercício.
            nao_conformes += 1
            # Exibe uma informação no terminal para acompanhar o resultado da execução.
            print(f"[{dispositivo['nome']}] NÃO CONFORME")
            # Exibe uma informação no terminal para acompanhar o resultado da execução.
            print("\n".join(diferencas))
        # Executa este caminho quando nenhuma condição anterior foi atendida.
        else:
            # Exibe uma informação no terminal para acompanhar o resultado da execução.
            print(f"[{dispositivo['nome']}] CONFORME")
    # Captura uma exceção para tratar o erro sem encerrar inesperadamente o programa.
    except Exception as erro:
        # Exibe uma informação no terminal para acompanhar o resultado da execução.
        print(f"[{dispositivo['nome']}] FALHA ({type(erro).__name__}: {erro})")

# Exibe uma informação no terminal para acompanhar o resultado da execução.
print(f"\nResumo: {nao_conformes} de {len(inventario)} equipamento(s) fora de conformidade.")
