# INSTALL.md — Instalação do Linux (Ubuntu) no Windows com WSL  
**Guia passo a passo para alunos iniciantes**

## Objetivo

Este documento descreve, **do zero**, o processo de instalação do **Linux (Ubuntu)** no Windows utilizando o **Windows Subsystem for Linux (WSL)**, com base no **tutorial oficial da Microsoft**.

O guia foi elaborado para **alunos sem conhecimento prévio** em Linux, terminal ou administração de sistemas, que realizarão a instalação **sozinhos**, fora de sala de aula.

O procedimento utiliza o método **oficial e recomendado atualmente**, baseado no comando `wsl --install`.

Este material tem caráter **didático e institucional**, adequado para uso em disciplinas.

---

## Índice

1. [Antes de começar](#1-antes-de-começar)  
2. [Verificar a versão do Windows](#2-verificar-a-versão-do-windows)  
3. [Abrir o PowerShell como administrador](#3-abrir-o-powershell-como-administrador)  
4. [Instalar o WSL](#4-instalar-o-wsl)  
5. [Instalar a distribuição Ubuntu](#5-instalar-a-distribuição-ubuntu)  
6. [Primeira execução do Ubuntu](#6-primeira-execução-do-ubuntu)  
7. [Verificar se a instalação funcionou](#7-verificar-se-a-instalação-funcionou)  
8. [Comandos básicos úteis](#8-comandos-básicos-úteis)  
9. [Problemas comuns](#9-problemas-comuns)  

---

## 1. Antes de começar

✔ Funciona para Windows 10 e Windows 11  
✔ Não requer conhecimento prévio de Linux  
✔ Não utiliza máquina virtual tradicional  

### Requisitos mínimos

- Windows 10 versão **2004 ou superior**  
- Windows 11 (qualquer versão)  
- **4 GB de RAM** (8 GB recomendado)  
- Conexão com a internet  
- Permissão de **Administrador** no computador  

---

## 2. Verificar a versão do Windows

1. Pressione **Win + R**  
2. Digite `winver`  
3. Pressione **Enter**  

Se aparecer **Windows 10 (2004+)** ou **Windows 11**, continue.

---

## 3. Abrir o PowerShell como administrador

1. Clique no menu **Iniciar**  
2. Digite **PowerShell**  
3. Clique com o botão direito em **Windows PowerShell**  
4. Clique em **Executar como administrador**  
5. Confirme em **Sim**  

---

## 4. Instalar o WSL

📘 Documentação oficial da Microsoft:  
https://learn.microsoft.com/pt-br/windows/wsl/install

No PowerShell, execute:

```powershell
wsl --install
```

Esse comando ativa os componentes necessários do Windows e prepara o sistema para uso do WSL.

Se aparecer a mensagem:

```text
Subsistema do Windows para Linux já está instalado.
```

Isso **não é um erro**.  
👉 Reinicie o computador antes de continuar.

---

## 5. Instalar a distribuição Ubuntu

Após reiniciar o computador, abra novamente o **PowerShell como administrador**.

Liste as distribuições disponíveis:

```powershell
wsl --list --online
```

Escolha a distribuição **Ubuntu-20.04** (versão usada na disciplina) e execute:

```powershell
wsl --install -d Ubuntu-20.04
```

✔ Aguarde o processo finalizar  
✔ Reinicie o computador **se o sistema solicitar**  

---

## 6. Primeira execução do Ubuntu

1. Abra o menu **Iniciar**  
2. Digite **Ubuntu**  
3. Clique em **Ubuntu 20.04 LTS**  

Na primeira execução:

- Crie um **nome de usuário Linux**  
- Crie uma **senha**  

⚠️ Ao digitar a senha, **nada aparece na tela**. Isso é normal.

---

## 7. Verificar se a instalação funcionou

### No PowerShell

```powershell
wsl -l -v
```

Resultado esperado:

```text
NAME            STATE     VERSION
Ubuntu-20.04    Running   2
```

### No Ubuntu

```bash
lsb_release -a
```

Se aparecer **Ubuntu 20.04 LTS**, a instalação foi concluída com sucesso.

---

## 8. Comandos básicos úteis

### No PowerShell

```powershell
wsl
wsl -l -v
wsl --shutdown
```

### No Ubuntu

Abrir a pasta atual no Explorador de Arquivos do Windows:

```bash
explorer.exe .
```

---

## 9. Problemas comuns

- Execute sempre o PowerShell como **Administrador**
- Reinicie o computador se algo não funcionar
- Se o Ubuntu fechar imediatamente:

```powershell
wsl --shutdown
```

---

Documento preparado para uso didático.

**Tiago Belintani — 2026**
