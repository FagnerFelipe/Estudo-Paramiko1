# Importa uma biblioteca necessária para as operações deste exercício.
import json
# Importa uma função, classe ou recurso específico de outro módulo.
from concurrent.futures import ThreadPoolExecutor
# Importa uma função, classe ou recurso específico de outro módulo.
from conexao import conectar, executar

# Define/atualiza `LIMITE_DISCO` com o valor calculado nesta linha.
LIMITE_DISCO = 80
# Define/atualiza `LIMITE_CARGA` com o valor calculado nesta linha.
LIMITE_CARGA = 2.0


# Define uma função reutilizável; os parâmetros recebem os dados necessários para executar esta tarefa.
def verificar(dispositivo):
    # Atualiza o registro com o valor obtido nesta etapa.
    resultado = {
        # Executa esta instrução como parte do fluxo do exercício.
        "nome": dispositivo["nome"],
        "disco": None,
        "carga": None,
        "sshd": None,
        "alertas": [],
        "estado": "OK",
    # Executa esta instrução como parte do fluxo do exercício.
    }

    # Cria ou armazena o objeto/resultado que será utilizado nas próximas operações.
    cliente = None
    # Inicia um bloco protegido para permitir o tratamento de possíveis falhas.
    try:
        # Cria ou armazena o objeto/resultado que será utilizado nas próximas operações.
        cliente = conectar(dispositivo)

        # Executa esta instrução como parte do fluxo do exercício.
        _, disco, _ = executar(
            # Executa esta instrução como parte do fluxo do exercício.
            cliente, "df --output=pcent / | tail -1 | tr -dc '0-9'"
        # Executa esta instrução como parte do fluxo do exercício.
        )
        # Executa esta instrução como parte do fluxo do exercício.
        _, carga, _ = executar(cliente, "cut -d' ' -f1 /proc/loadavg")
        # Armazena o código de retorno do comando; normalmente zero indica sucesso.
        codigo_sshd, _, _ = executar(cliente, "pgrep -x sshd >/dev/null")

        # Atualiza o registro com o valor obtido nesta etapa.
        resultado["disco"] = int(disco)
        # Atualiza o registro com o valor obtido nesta etapa.
        resultado["carga"] = float(carga)
        # Atualiza o registro com o valor obtido nesta etapa.
        resultado["sshd"] = "ativo" if codigo_sshd == 0 else "parado"

        # Verifica uma condição e executa o bloco somente se ela for verdadeira.
        if resultado["disco"] > LIMITE_DISCO:
            # Atualiza o registro com o valor obtido nesta etapa.
            resultado["alertas"].append(f"disco em {resultado['disco']}%")
        # Verifica uma condição e executa o bloco somente se ela for verdadeira.
        if resultado["carga"] > LIMITE_CARGA:
            # Atualiza o registro com o valor obtido nesta etapa.
            resultado["alertas"].append(f"carga alta ({resultado['carga']})")
        # Verifica uma condição e executa o bloco somente se ela for verdadeira.
        if resultado["sshd"] != "ativo":
            # Atualiza o registro com o valor obtido nesta etapa.
            resultado["alertas"].append("serviço sshd parado")

        # Verifica uma condição e executa o bloco somente se ela for verdadeira.
        if resultado["alertas"]:
            # Atualiza o registro com o valor obtido nesta etapa.
            resultado["estado"] = "ALERTA"

    # Captura uma exceção para tratar o erro sem encerrar inesperadamente o programa.
    except Exception as erro:
        # Atualiza o registro com o valor obtido nesta etapa.
        resultado["estado"] = "FALHA"
        # Atualiza o registro com o valor obtido nesta etapa.
        resultado["alertas"].append(type(erro).__name__)
    # Garante a execução deste bloco, ocorrendo sucesso ou erro; normalmente libera recursos.
    finally:
        # Verifica uma condição e executa o bloco somente se ela for verdadeira.
        if cliente:
            # Fecha a conexão SSH e libera os recursos associados.
            cliente.close()

    # Devolve o resultado ao ponto em que a função foi chamada.
    return resultado


# Abre o arquivo em um contexto controlado; ele será fechado automaticamente ao sair do bloco.
with open("inventario.json", encoding="utf-8") as arquivo:
    # Define/atualiza `inventario` com o valor calculado nesta linha.
    inventario = json.load(arquivo)

# Abre um recurso em contexto controlado, garantindo seu fechamento ao sair do bloco.
with ThreadPoolExecutor(max_workers=10) as pool:
    # Atualiza o registro com o valor obtido nesta etapa.
    resultados = list(pool.map(verificar, inventario))

# Exibe uma informação no terminal para acompanhar o resultado da execução.
print(f"{'DISP':<6}{'ESTADO':<9}{'DISCO':<9}{'CARGA':<9}{'SSHD':<9}ALERTAS")
# Exibe uma informação no terminal para acompanhar o resultado da execução.
print("-" * 70)

# Percorre os elementos da coleção, executando o bloco para cada item.
for resultado in resultados:
    # Define/atualiza `disco` com o valor calculado nesta linha.
    disco = f"{resultado['disco']}%" if resultado["disco"] is not None else "-"
    # Define/atualiza `carga` com o valor calculado nesta linha.
    carga = resultado["carga"] if resultado["carga"] is not None else "-"
    # Define/atualiza `alertas` com o valor calculado nesta linha.
    alertas = "; ".join(resultado["alertas"])
    # Exibe uma informação no terminal para acompanhar o resultado da execução.
    print(
        # Executa esta instrução como parte do fluxo do exercício.
        f"{resultado['nome']:<6}{resultado['estado']:<9}"
        f"{disco:<9}{str(carga):<9}{(resultado['sshd'] or '-'):<9}{alertas}"
    # Executa esta instrução como parte do fluxo do exercício.
    )
