# INSTALL.md — Instalação do WSL 1 (Ubuntu) no Windows 10 e Windows 11

## Objetivo

Este documento descreve exclusivamente o processo de instalação e verificação do **Windows Subsystem for Linux (WSL 1)** com **Ubuntu**.  
O guia é destinado a usuários iniciantes e tem caráter **didático e institucional**, adequado para uso em disciplinas que utilizam Linux via WSL.

Não inclui instalação de Conda, softwares científicos ou pipelines de análise.

---

## Índice

1. [Pré-requisitos](#1-pré-requisitos)
2. [Verificação da versão do Windows](#2-verificação-da-versão-do-windows)
3. [Instalação do WSL](#3-instalação-do-wsl)
4. [Configuração do WSL 1](#4-configuração-do-wsl-1)
5. [Instalação do Ubuntu](#5-instalação-do-ubuntu)
6. [Configuração inicial do Ubuntu](#6-configuração-inicial-do-ubuntu)
7. [Verificação da instalação](#7-verificação-da-instalação)
8. [Comandos úteis](#8-comandos-úteis)
9. [Solução de problemas](#9-solução-de-problemas)

---

## 1. Pré-requisitos

### Requisitos do sistema

- Windows 10 versão 1607 ou superior  
- Windows 11 (qualquer versão)  
- Mínimo de 4 GB de memória RAM (8 GB ou mais recomendado)  
- Pelo menos 10 GB de espaço livre em disco  
- **Não é necessário virtualização**  
- Permissão de administrador no Windows  

O WSL 1 **não depende de recursos de virtualização** e é compatível com máquinas mais antigas ou com virtualização desativada.

---

## 2. Verificação da versão do Windows

1. Pressione `Win + R`  
2. Digite `winver` e pressione Enter  
3. Verifique:
   - Windows 10: versão 1607 ou superior  
   - Windows 11: qualquer versão  

---

## 3. Instalação do WSL

Abra o **PowerShell como Administrador** e execute:

```powershell
wsl --install --no-distribution
```

Este comando habilita os componentes necessários do Windows para o WSL.

Reinicie o computador quando solicitado.

---

## 4. Configuração do WSL 1

Após reiniciar, abra novamente o PowerShell e execute:

```powershell
wsl --set-default-version 1
```

Verifique o status:

```powershell
wsl --status
```

O campo **Default Version** deve indicar o valor **1**.

---

## 5. Instalação do Ubuntu

1. Abra a **Microsoft Store**  
2. Procure por **Ubuntu 22.04 LTS** (ou outra versão LTS recomendada pelo curso)  
3. Clique em **Instalar**  

Após a instalação, abra o aplicativo **Ubuntu** pelo menu Iniciar.

---

## 6. Configuração inicial do Ubuntu

Na primeira execução:

1. Aguarde a finalização da instalação  
2. Crie um nome de usuário Linux  
3. Defina uma senha  

Após a configuração, o terminal estará pronto para uso.

---

## 7. Verificação da instalação

No terminal do Ubuntu, execute:

```bash
lsb_release -a
uname -a
```

No PowerShell, execute:

```powershell
wsl -l -v
```

A distribuição Ubuntu deve aparecer com **Version 1**.

---

## 8. Comandos úteis

### No PowerShell

```powershell
wsl -l -v
wsl --shutdown
```

### No Ubuntu

Abrir o diretório atual no Explorador de Arquivos do Windows:

```bash
explorer.exe .
```

---

## 9. Solução de problemas

### Ubuntu abre e fecha imediatamente

- Execute no PowerShell:
  ```powershell
  wsl --shutdown
  ```
- Abra o Ubuntu novamente

### Versão incorreta do WSL

Caso o Ubuntu esteja rodando em WSL 2 e o curso exija WSL 1:

```powershell
wsl --set-version Ubuntu 1
```

(Substitua `Ubuntu` pelo nome exato da distribuição exibido em `wsl -l`.)

### Erros de instalação

- Reinicie o sistema após habilitar o WSL  
- Verifique se o Windows está atualizado  
- Execute o PowerShell sempre como Administrador  

---

Documento preparado para uso didático e institucional.

**Tiago Belintani — 2026**  
*Brave the Sun*
