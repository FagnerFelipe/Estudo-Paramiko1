# Script de coleta executado no equipamento remoto.
# Executa o comando indicado no shell.
#!/bin/bash
# Exibe a data e hora atuais do equipamento.
echo "Data: $(date '+%F %T')"
# Exibe o nome do equipamento remoto.
echo "Host: $(hostname)"
# Identifica o usuário que executa o script.
echo "Usuário: $(whoami)"
# Consulta o percentual de uso do disco raiz e remove espaços/símbolos extras.
echo "Disco /: $(df --output=pcent / | tail -1 | tr -d ' %')%"
