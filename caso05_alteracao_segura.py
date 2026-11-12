# Importa uma biblioteca necessária para as operações deste exercício.
import json
# Importa uma biblioteca necessária para as operações deste exercício.
import re
# Importa uma função, classe ou recurso específico de outro módulo.
from conexao import conectar

# Define/atualiza `CHAVE` com o valor calculado nesta linha.
CHAVE = "ntp_server"
# Define/atualiza `VALOR` com o valor calculado nesta linha.
VALOR = "10.0.0.50"


# Define uma função reutilizável; os parâmetros recebem os dados necessários para executar esta tarefa.
def validar(chave, valor):
    # Documenta a finalidade da função ou do trecho.
    """Aceita somente caracteres simples para os parâmetros."""
    # Define/atualiza `padrao` com o valor calculado nesta linha.
    padrao = r"[A-Za-z0-9_.-]+"
    # Verifica uma condição e executa o bloco somente se ela for verdadeira.
    if not re.fullmatch(padrao, chave) or not re.fullmatch(padrao, valor):
        # Gera uma exceção para sinalizar que a operação não pode continuar normalmente.
        raise ValueError("Chave ou valor contém caracteres não permitidos.")


# Define uma função reutilizável; os parâmetros recebem os dados necessários para executar esta tarefa.
def aplicar(dispositivo, chave, valor):
    # Define/atualiza `caminho` com o valor calculado nesta linha.
    caminho = f"/home/{dispositivo['usuario']}/dispositivo.cfg"
    # Cria ou armazena o objeto/resultado que será utilizado nas próximas operações.
    cliente = conectar(dispositivo)
    # Guarda a sessão SFTP para transferir ou manipular arquivos remotamente.
    sftp = None

    # Inicia um bloco protegido para permitir o tratamento de possíveis falhas.
    try:
        # Guarda a sessão SFTP para transferir ou manipular arquivos remotamente.
        sftp = cliente.open_sftp()

        # Guarda uma cópia antes de alterar.
        # Abre um recurso em contexto controlado, garantindo seu fechamento ao sair do bloco.
        with sftp.open(caminho, "rb") as remoto:
            # Define/atualiza `original` com o valor calculado nesta linha.
            original = remoto.read()

        # Define/atualiza `caminho_backup` com o valor calculado nesta linha.
        caminho_backup = caminho + ".bak"
        # Abre um recurso em contexto controlado, garantindo seu fechamento ao sair do bloco.
        with sftp.open(caminho_backup, "wb") as backup:
            # Executa esta instrução como parte do fluxo do exercício.
            backup.write(original)

        # Define/atualiza `texto` com o valor calculado nesta linha.
        texto = original.decode("utf-8")
        # Define/atualiza `linhas` com o valor calculado nesta linha.
        linhas = [linha for linha in texto.splitlines() if linha.strip()]
        # Define/atualiza `nova_linha` com o valor calculado nesta linha.
        nova_linha = f"{chave}={valor}"

        # Atualiza a linha existente ou acrescenta se ainda não existir.
        # Define/atualiza `atualizadas` com o valor calculado nesta linha.
        atualizadas = []
        # Define/atualiza `encontrou` com o valor calculado nesta linha.
        encontrou = False
        # Percorre os elementos da coleção, executando o bloco para cada item.
        for linha in linhas:
            # Verifica uma condição e executa o bloco somente se ela for verdadeira.
            if linha.startswith(chave + "="):
                # Verifica uma condição e executa o bloco somente se ela for verdadeira.
                if not encontrou:
                    # Executa esta instrução como parte do fluxo do exercício.
                    atualizadas.append(nova_linha)
                    # Define/atualiza `encontrou` com o valor calculado nesta linha.
                    encontrou = True
            # Executa este caminho quando nenhuma condição anterior foi atendida.
            else:
                # Executa esta instrução como parte do fluxo do exercício.
                atualizadas.append(linha)

        # Verifica uma condição e executa o bloco somente se ela for verdadeira.
        if not encontrou:
            # Executa esta instrução como parte do fluxo do exercício.
            atualizadas.append(nova_linha)

        # Define/atualiza `conteudo` com o valor calculado nesta linha.
        conteudo = ("\n".join(atualizadas) + "\n").encode("utf-8")

        # Inicia um bloco protegido para permitir o tratamento de possíveis falhas.
        try:
            # Abre um recurso em contexto controlado, garantindo seu fechamento ao sair do bloco.
            with sftp.open(caminho, "wb") as remoto:
                # Executa esta instrução como parte do fluxo do exercício.
                remoto.write(conteudo)

            # Confere se a linha foi gravada exatamente uma vez.
            # Abre um recurso em contexto controlado, garantindo seu fechamento ao sair do bloco.
            with sftp.open(caminho, "r") as remoto:
                # Define/atualiza `conferido` com o valor calculado nesta linha.
                conferido = remoto.read().decode("utf-8").splitlines()

            # Verifica uma condição e executa o bloco somente se ela for verdadeira.
            if conferido.count(nova_linha) != 1:
                # Gera uma exceção para sinalizar que a operação não pode continuar normalmente.
                raise RuntimeError("A verificação da configuração falhou.")

            # Devolve o resultado ao ponto em que a função foi chamada.
            return "APLICADO"
        # Captura uma exceção para tratar o erro sem encerrar inesperadamente o programa.
        except Exception:
            # Restaura o conteúdo original se alguma etapa falhar.
            # Abre um recurso em contexto controlado, garantindo seu fechamento ao sair do bloco.
            with sftp.open(caminho, "wb") as remoto:
                # Executa esta instrução como parte do fluxo do exercício.
                remoto.write(original)
            # Devolve o resultado ao ponto em que a função foi chamada.
            return "REVERTIDO: falha na verificação"

    # Garante a execução deste bloco, ocorrendo sucesso ou erro; normalmente libera recursos.
    finally:
        # Verifica uma condição e executa o bloco somente se ela for verdadeira.
        if sftp:
            # Encerra a sessão SFTP e libera o canal utilizado para transferência de arquivos.
            sftp.close()
        # Fecha a conexão SSH e libera os recursos associados.
        cliente.close()


# Executa esta instrução como parte do fluxo do exercício.
validar(CHAVE, VALOR)

# Abre o arquivo em um contexto controlado; ele será fechado automaticamente ao sair do bloco.
with open("inventario.json", encoding="utf-8") as arquivo:
    # Define/atualiza `inventario` com o valor calculado nesta linha.
    inventario = json.load(arquivo)

# Percorre os elementos da coleção, executando o bloco para cada item.
for dispositivo in inventario:
    # Inicia um bloco protegido para permitir o tratamento de possíveis falhas.
    try:
        # Exibe uma informação no terminal para acompanhar o resultado da execução.
        print(f"{dispositivo['nome']}: {aplicar(dispositivo, CHAVE, VALOR)}")
    # Captura uma exceção para tratar o erro sem encerrar inesperadamente o programa.
    except Exception as erro:
        # Exibe uma informação no terminal para acompanhar o resultado da execução.
        print(f"{dispositivo['nome']}: FALHA ({type(erro).__name__}: {erro})")
