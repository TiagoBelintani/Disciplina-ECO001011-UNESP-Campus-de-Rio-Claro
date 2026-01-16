# INSTALL.md — Instalação do WSL (Ubuntu) no Windows 10 e Windows 11

## Objetivo

Este documento descreve exclusivamente o processo de instalação e verificação do Windows Subsystem for Linux (WSL 2) com Ubuntu. O guia é destinado a usuários iniciantes e tem caráter didático e institucional, adequado para uso em disciplinas que utilizam Linux via WSL.

Não inclui instalação de Conda, softwares científicos ou pipelines de análise.

---

## Índice

1. Pré-requisitos
2. Verificação da versão do Windows
3. Ativação da virtualização
4. Instalação do WSL
5. Configuração do WSL 2
6. Instalação do Ubuntu
7. Configuração inicial do Ubuntu
8. Verificação da instalação
9. Comandos úteis
10. Solução de problemas

---

## 1. Pré-requisitos

### Requisitos do sistema

* Windows 10 versão 2004 ou superior (Build 19041+)
* Windows 11 (qualquer versão)
* Mínimo de 4 GB de memória RAM (8 GB ou mais recomendado)
* Pelo menos 10 GB de espaço livre em disco
* Virtualização habilitada na BIOS/UEFI
* Permissão de administrador no Windows

---

## 2. Verificação da versão do Windows

1. Pressione Win + R
2. Digite winver e pressione Enter
3. Verifique:

   * Windows 10: versão 2004 ou superior
   * Windows 11: qualquer versão

---

## 3. Ativação da virtualização

### Verificar se a virtualização está ativa

1. Pressione Ctrl + Shift + Esc
2. Acesse a aba Desempenho
3. Selecione CPU
4. Verifique o campo Virtualização

O status deve constar como Ativada.

### Ativar na BIOS/UEFI (se necessário)

1. Reinicie o computador
2. Acesse a BIOS/UEFI (Del, F2, F10 ou Esc, dependendo do fabricante)
3. Ative uma das opções:

   * Intel VT-x / VT-d
   * SVM Mode (AMD)
4. Salve as alterações e reinicie

O WSL 2 não funciona sem virtualização ativa.

---

## 4. Instalação do WSL

Abra o PowerShell como Administrador e execute:

```powershell
wsl --install
```

Este comando habilita os componentes necessários do Windows, define o WSL 2 como versão padrão e instala uma distribuição Linux padrão (Ubuntu).

Reinicie o computador quando solicitado.

---

## 5. Configuração do WSL 2

Após reiniciar, abra novamente o PowerShell e execute:

```powershell
wsl --set-default-version 2
```

Verifique o status:

```powershell
wsl --status
```

O campo Default Version deve indicar o valor 2.

---

## 6. Instalação do Ubuntu

Caso o Ubuntu não tenha sido instalado automaticamente:

1. Abra a Microsoft Store
2. Procure por Ubuntu 22.04 LTS
3. Clique em Instalar

Após a instalação, abra o aplicativo Ubuntu pelo menu Iniciar.

---

## 7. Configuração inicial do Ubuntu

Na primeira execução:

1. Aguarde a finalização da instalação
2. Crie um nome de usuário Linux
3. Defina uma senha

Após a configuração, o terminal estará pronto para uso.

---

## 8. Verificação da instalação

No terminal do Ubuntu, execute:

```bash
lsb_release -a
uname -a
```

No PowerShell, execute:

```powershell
wsl -l -v
```

A distribuição Ubuntu deve aparecer com Version 2.

---

## 9. Comandos úteis

No PowerShell:

```powershell
wsl --shutdown
wsl -l -v
```

No Ubuntu:

```bash
explorer.exe .
```

---

## 10. Solução de problemas

### WSL 2 não inicia

* Verifique se a virtualização está habilitada na BIOS
* Confirme a versão do Windows
* Reinicie o sistema após a instalação

### Ubuntu abre e fecha imediatamente

* Execute wsl --shutdown
* Abra o Ubuntu novamente

---

Documento preparado para uso didático e institucional.


Tiago Belintani 2025 - Brave The Sun
