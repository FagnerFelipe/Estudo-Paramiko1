ESTUDO DIRIGIDO - SSH COM PARAMIKO

Arquivos:
- caso01 até caso11: um script Python para cada caso.
- conexao.py: módulo de conexão SSH compartilhado pelos exercícios.
- inventario.json: inventário padrão dos dispositivos R1, R2 e R3.
- inventario_chave.json: deve ser criado no Caso 3, conforme instruções abaixo.
- coleta.sh e referencia.cfg: arquivos auxiliares dos Casos 7 e 8.

PREPARAÇÃO (WSL/UBUNTU)
1. Instale o SSH e o Paramiko:
   sudo apt update
   sudo apt install -y openssh-server python3-venv
   sudo service ssh start

2. Crie os usuários r1, r2, r3 e bastion, caso ainda não existam.
   Para o laboratório do material, a senha inicial é Redes@2026.

3. Crie/ative um ambiente virtual e instale a biblioteca:
   python3 -m venv ~/venv-redes
   source ~/venv-redes/bin/activate
   pip install paramiko

4. Defina a senha no terminal (não dentro do código):
   export SSH_SENHA='Redes@2026'

5. Coloque os arquivos desta pasta no mesmo diretório de trabalho.
   Execute um caso, por exemplo:
   python caso01_primeiro_comando.py

OBSERVAÇÕES
- Os scripts usam os endereços e usuários do laboratório descrito no documento.
- Os arquivos remotos dispositivo.cfg precisam existir em /home/r1, /home/r2 e /home/r3.
- O Caso 3 requer gerar e instalar chaves Ed25519 e criar inventario_chave.json.
- O Caso 10 requer iniciar a segunda instância SSH na porta 2222:
  sudo mkdir -p /run/sshd
  sudo /usr/sbin/sshd -p 2222
- No Caso 8, a referência está em referencia.cfg. Para testar a divergência,
  altere manualmente o snmp_community de um dos dispositivos.
- Os exemplos usam AutoAddPolicy para facilitar o laboratório. Em produção,
  valide as chaves dos servidores com known_hosts.

Os códigos foram organizados e corrigidos para formar scripts Python válidos.
