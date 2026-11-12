# Importa uma biblioteca necessária para as operações deste exercício.
import csv
import json
from concurrent.futures import ThreadPoolExecutor
# Importa uma função, classe ou recurso específico de outro módulo.
from conexao import conectar, executar

# Define/atualiza `COLUNAS` com o valor calculado nesta linha.
COLUNAS = ["nome", "usuario", "hostname", "kernel", "uptime", "status"]


# Define uma função reutilizável; os parâmetros recebem os dados necessários para executar esta tarefa.
def coletar(dispositivo):
    # Prepara ou atualiza os dados que serão armazenados para este dispositivo.
    registro = {coluna: "" for coluna in COLUNAS}
    registro["nome"] = dispositivo["nome"]
    registro["usuario"] = dispositivo["usuario"]
    # Cria ou armazena o objeto/resultado que será utilizado nas próximas operações.
    cliente = None

    # Inicia um bloco protegido para permitir o tratamento de possíveis falhas.
    try:
        # Cria ou armazena o objeto/resultado que será utilizado nas próximas operações.
        cliente = conectar(dispositivo)
        # Prepara ou atualiza os dados que serão armazenados para este dispositivo.
        registro["usuario"] = executar(cliente, "whoami")[1]
        registro["hostname"] = executar(cliente, "hostname")[1]
        registro["kernel"] = executar(cliente, "uname -r")[1]
        registro["uptime"] = executar(cliente, "uptime -p")[1]
        registro["status"] = "OK"
    # Captura uma exceção para tratar o erro sem encerrar inesperadamente o programa.
    except Exception as erro:
        # Prepara ou atualiza os dados que serão armazenados para este dispositivo.
        registro["status"] = f"FALHA: {type(erro).__name__}"
    # Garante a execução deste bloco, ocorrendo sucesso ou erro; normalmente libera recursos.
    finally:
        # Verifica uma condição e executa o bloco somente se ela for verdadeira.
        if cliente:
            # Fecha a conexão SSH e libera os recursos associados.
            cliente.close()

    # Devolve o resultado ao ponto em que a função foi chamada.
    return registro


# Abre o arquivo em um contexto controlado; ele será fechado automaticamente ao sair do bloco.
with open("inventario.json", encoding="utf-8") as arquivo:
    # Define/atualiza `inventario` com o valor calculado nesta linha.
    inventario = json.load(arquivo)

# Abre um recurso em contexto controlado, garantindo seu fechamento ao sair do bloco.
with ThreadPoolExecutor(max_workers=10) as pool:
    # Atualiza o registro com o valor obtido nesta etapa.
    resultados = list(pool.map(coletar, inventario))

# Abre o arquivo em um contexto controlado; ele será fechado automaticamente ao sair do bloco.
with open("inventario_coletado.csv", "w", newline="", encoding="utf-8") as arquivo:
    # Define/atualiza `escritor` com o valor calculado nesta linha.
    escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)
    # Executa esta instrução como parte do fluxo do exercício.
    escritor.writeheader()
    escritor.writerows(resultados)

# Percorre os elementos da coleção, executando o bloco para cada item.
for resultado in resultados:
    # Exibe uma informação no terminal para acompanhar o resultado da execução.
    print(
        # Executa esta instrução como parte do fluxo do exercício.
        f"{resultado['nome']:<4} "
        f"{resultado['status']:<25} "
        f"{resultado['usuario']:<6} "
        f"{resultado['uptime']}"
    )
