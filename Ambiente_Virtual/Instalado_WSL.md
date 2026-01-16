Guia Completo: Instalação do WSL (Ubuntu) no Windows 10 e Windows 11
Índice
Pré-requisitos

Etapa 1: Ativar a Virtualização

Etapa 2: Habilitar o WSL

Etapa 3: Instalar o WSL 2

Etapa 4: Instalar o Ubuntu

Etapa 5: Configuração Inicial

Etapa 6: Verificar Instalação

Etapa 7: Configurações Avançadas

Solução de Problemas

Comandos Úteis

Dicas Finais

Recursos Adicionais

Pré-requisitos
Requisitos do Sistema
Windows 10 versão 2004+ (Build 19041+)

Windows 11 (qualquer versão)

4GB de RAM (8GB+ recomendado)

10GB de espaço livre

Virtualização ativada na BIOS/UEFI

Verificando sua versão do Windows
Pressione Win + R

Digite winver

Confirme se sua versão é compatível

Etapa 1: Ativar a Virtualização (BIOS/UEFI)
Verificar se está ativada
Pressione Ctrl + Shift + Esc

Vá em Desempenho → CPU

Veja o campo Virtualização

Se estiver Habilitado, siga para a Etapa 2.

Se estiver Desabilitado
Reinicie o PC

Entre na BIOS/UEFI (teclas comuns: F2, F10, F12, Del, Esc)

Ative:

Intel VT-x

AMD-V

Salve e saia (F10 na maioria dos casos)

Etapa 2: Habilitar o WSL
Método 1: Interface Gráfica
Win + X → Aplicativos e Recursos

Programas e Recursos

Ativar ou desativar recursos do Windows

Marque:

Plataforma de Máquina Virtual

Subsistema do Windows para Linux

Reinicie

Método 2: PowerShell (Administrador)
powershell
wsl --install
Método 3: Comandos Manuais
powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
Restart-Computer
📥 Etapa 3: Instalar o WSL 2
Definir WSL 2 como padrão
powershell
wsl --set-default-version 2
Se aparecer erro de kernel
Baixe o pacote: https://aka.ms/wsl2kernel

Instale o arquivo wsl_update_x64.msi

Execute novamente:

powershell
wsl --set-default-version 2
🐧 Etapa 4: Instalar o Ubuntu
Método 1: Microsoft Store
Pesquise por Ubuntu

Instale:

Ubuntu (LTS mais recente)

Ubuntu 22.04 LTS

Ubuntu 20.04 LTS

Método 2: Linha de comando
powershell
wsl --list --online
wsl --install -d Ubuntu
# ou
wsl --install -d Ubuntu-22.04
⚙️ Etapa 5: Configuração Inicial
Primeira execução
Abra Ubuntu no menu iniciar

Aguarde a instalação

Criar usuário
Code
Enter new UNIX username: seu_usuario
New password:
Retype new password:
Atualizar pacotes
bash
sudo apt update && sudo apt upgrade -y
🔍 Etapa 6: Verificar Instalação
No PowerShell
powershell
wsl --list --verbose
Saída esperada:

Code
NAME      STATE     VERSION
Ubuntu    Running   2
No Ubuntu
bash
lsb_release -a
🛠️ Etapa 7: Configurações Avançadas
Acessar arquivos do Windows
bash
cd /mnt/c/Users/seu_usuario
Acessar arquivos do Ubuntu no Windows
Code
\\wsl$\Ubuntu\home\seu_usuario
Alterar versão do WSL
powershell
wsl --set-version Ubuntu 2
Configurar recursos (.wslconfig)
Crie o arquivo em:
C:\Users\seu_usuario\.wslconfig

ini
[wsl2]
memory=8GB
processors=4
swap=4GB
localhostForwarding=true
Solução de Problemas Comuns
Erro: “WSL 2 requires an update”
powershell
wsl --update
Distribuição não inicia
powershell
wsl --shutdown
wsl -l -v
wsl -d Ubuntu
Problemas de rede
powershell
wsl --shutdown
netsh winsock reset
netsh int ip reset all
netsh winhttp reset proxy
ipconfig /flushdns
Erro 0x80070003
powershell
wsl --import Ubuntu C:\wsl\Ubuntu caminho_do_tarball
Comandos Úteis
Gerenciamento
powershell
wsl --list --verbose
wsl --shutdown
wsl --terminate Ubuntu
wsl --unregister Ubuntu
wsl --export Ubuntu ubuntu_backup.tar
wsl --import UbuntuNew C:\wsl\UbuntuNew ubuntu_backup.tar
No Ubuntu
bash
exit
# ou Ctrl + D
Estrutura de Pastas Recomendada
Code
/home/seu_usuario/
├── projetos/
├── documentos/
└── scripts/
Terminal do Windows (Opcional)
Windows Terminal
Instale pela Microsoft Store

Configure como padrão

Personalize temas e fontes

VS Code + WSL
Instale a extensão Remote - WSL

Abra uma janela WSL pelo botão ><

Dicas Finais
bash
sudo apt update && sudo apt upgrade -y
sudo apt install pacote
sudo apt remove pacote
Configurar Git
bash
git config --global user.name "Seu Nome"
git config --global user.email "email@exemplo.com"
Backup
powershell
wsl --export Ubuntu ubuntu_backup_$(Get-Date -Format "yyyyMMdd").tar
📚 Recursos Adicionais
Documentação Oficial do WSL

Repositório GitHub do WSL

Wiki do Ubuntu no WSL

Avisos Importantes
Não edite arquivos do Linux pelo Windows

Faça backups antes de alterações grandes

WSL 2 usa máquina virtual real (mais consumo de RAM)

Instalação Concluída
Agora você tem um ambiente Ubuntu completo rodando no Windows.
Para iniciar, digite Ubuntu no menu iniciar ou use:

powershell
wsl
Se quiser, posso gerar uma versão com capa, badges, sumário automático, ou até transformar isso em um README profissional de repositório. Quer deixar ainda mais bonito ou organizado?

sim faca isso
Perfeito, Tiago — preparei um README.md  profissional, com capa, badges, sumário automático, seções organizadas, e mantendo tudo pronto para você copiar e colar no GitHub.

Ficou com cara de documentação oficial, mas acessível para iniciantes.
Aproveitei para deixar o texto mais limpo, consistente e elegante.

A seguir está o arquivo completo em Markdown, pronto para uso.

Guia Completo: Instalação do WSL (Ubuntu) no Windows 10 e Windows 11
https://raw.githubusercontent.com/microsoft/WSL/master/DistributionIcons/WSL.png

<p align="center">
<strong>Ambiente Linux completo dentro do Windows — simples, rápido e poderoso.</strong>
</p>

Badges

https://img.shields.io/badge/Ubuntu-22.04-orange
https://img.shields.io/badge/Windows-10%20%7C%2011-0078D6
https://img.shields.io/badge/Guia-Completo-success

📚 Sumário
Pré-requisitos

Etapa 1: Ativar a Virtualização

Etapa 2: Habilitar o WSL

Etapa 3: Instalar o WSL 2

Etapa 4: Instalar o Ubuntu

Etapa 5: Configuração Inicial

Etapa 6: Verificar Instalação

Etapa 7: Configurações Avançadas

Solução de Problemas

Comandos Úteis

Estrutura de Pastas Recomendada

Terminal e VS Code

Dicas Finais

Recursos Adicionais

Avisos Importantes

Pré-requisitos
Requisitos do Sistema
Windows 10 2004+ (Build 19041+)

Windows 11 (qualquer versão)

4GB de RAM (8GB recomendado)

10GB de espaço livre

Virtualização ativada na BIOS/UEFI

Verificar versão do Windows
Pressione Win + R

Digite winver

Confirme se sua versão é compatível

Etapa 1: Ativar a Virtualização
Verificar se está ativa
Abra o Gerenciador de Tarefas (Ctrl + Shift + Esc)

Aba Desempenho → CPU

Veja o campo Virtualização

Se estiver Desabilitada, ative na BIOS:

Teclas comuns: F2, F10, F12, Del, Esc

Ative:

Intel VT-x

AMD AMD-V

Etapa 2: Habilitar o WSL
Método 1 — Interface Gráfica
Win + X → Aplicativos e Recursos

Programas e Recursos

Ativar ou desativar recursos do Windows

Marque:

Subsistema do Windows para Linux

Plataforma de Máquina Virtual

Reinicie

Método 2 — PowerShell (Admin)
powershell
wsl --install
Método 3 — Comandos Manuais
powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
Restart-Computer
Etapa 3: Instalar o WSL 2
Definir como padrão
powershell
wsl --set-default-version 2
Se aparecer erro de kernel
Baixe o pacote oficial:
https://aka.ms/wsl2kernel

Depois:

powershell
wsl --set-default-version 2
Etapa 4: Instalar o Ubuntu
Método 1 — Microsoft Store (Recomendado)
Pesquise por Ubuntu

Instale:

Ubuntu (LTS mais recente)

Ubuntu 22.04 LTS

Ubuntu 20.04 LTS

Método 2 — Linha de comando
powershell
wsl --list --online
wsl --install -d Ubuntu
# ou
wsl --install -d Ubuntu-22.04
⚙️ Etapa 5: Configuração Inicial
Criar usuário
Code
Enter new UNIX username: seu_usuario
New password:
Retype new password:
Atualizar pacotes
bash
sudo apt update && sudo apt upgrade -y
🔍 Etapa 6: Verificar Instalação
No Windows
powershell
wsl --list --verbose
No Ubuntu
bash
lsb_release -a
🛠️ Etapa 7: Configurações Avançadas
Acessar arquivos do Windows
bash
cd /mnt/c/Users/seu_usuario
Acessar arquivos do Ubuntu no Windows
Code
\\wsl$\Ubuntu\home\seu_usuario
Alterar versão da distro
powershell
wsl --set-version Ubuntu 2
Configurar recursos (.wslconfig)
Crie em:
C:\Users\seu_usuario\.wslconfig

ini
[wsl2]
memory=8GB
processors=4
swap=4GB
localhostForwarding=true
Solução de Problemas
WSL 2 requires an update
powershell
wsl --update
Distribuição não inicia
powershell
wsl --shutdown
wsl -l -v
wsl -d Ubuntu
Problemas de rede
powershell
wsl --shutdown
netsh winsock reset
netsh int ip reset all
netsh winhttp reset proxy
ipconfig /flushdns
Erro 0x80070003
powershell
wsl --import Ubuntu C:\wsl\Ubuntu caminho_do_tarball
Comandos Úteis
Gerenciamento
powershell
wsl --list --verbose
wsl --shutdown
wsl --terminate Ubuntu
wsl --unregister Ubuntu
wsl --export Ubuntu ubuntu_backup.tar
wsl --import UbuntuNew C:\wsl\UbuntuNew ubuntu_backup.tar
No Ubuntu
bash
exit
📁 Estrutura de Pastas Recomendada
Code
/home/seu_usuario/
├── projetos/
├── documentos/
└── scripts/
Terminal e VS Code
Windows Terminal
Instale pela Microsoft Store

Configure como padrão

Personalize temas e fontes

VS Code + WSL
Instale a extensão Remote - WSL

Abra uma janela WSL pelo botão ><

Dicas Finais
Atualizações
bash
sudo apt update && sudo apt upgrade -y
Instalar/Remover pacotes
bash
sudo apt install pacote
sudo apt remove pacote
Configurar Git
bash
git config --global user.name "Seu Nome"
git config --global user.email "email@exemplo.com"
Backup automático
powershell
wsl --export Ubuntu ubuntu_backup_$(Get-Date -Format "yyyyMMdd").tar
📚 Recursos Adicionais
Documentação Oficial do WSL

Repositório GitHub do WSL

Wiki do Ubuntu no WSL

Avisos Importantes
Não edite arquivos do Linux pelo Windows

Faça backups antes de alterações grandes

WSL 2 usa máquina virtual real (mais RAM)

Instalação Concluída
Agora você tem um ambiente Ubuntu completo rodando no Windows.
Para iniciar:

powershell
wsl

Tiago Belintani 2025 - Brave The Sun
