# Instalação do Conda e Criação de Ambiente Didático

Guia didático para **instalação do Conda (Miniconda)** e **criação de ambientes isolados**, destinado a aulas práticas de bioinformática, filogenômica e genômica em Linux, WSL ou macOS.

---

## Índice

1. [Objetivo](#objetivo)  
2. [O que é o Conda](#o-que-é-o-conda)  
3. [Por que usar ambientes Conda](#por-que-usar-ambientes-conda)  
4. [Sistemas compatíveis](#sistemas-compatíveis)  
5. [Download do Miniconda](#download-do-miniconda)  
6. [Instalação do Miniconda](#instalação-do-miniconda)  
7. [Inicialização do Conda](#inicialização-do-conda)  
8. [Atualização do Conda](#atualização-do-conda)  
9. [Criação de um ambiente didático](#criação-de-um-ambiente-didático)  
10. [Ativação e desativação do ambiente](#ativação-e-desativação-do-ambiente)  
11. [Instalação de programas no ambiente](#instalação-de-programas-no-ambiente)  
12. [Verificação do ambiente](#verificação-do-ambiente)  
13. [Boas práticas](#boas-práticas)  
14. [Problemas comuns](#problemas-comuns)  
15. [Referências](#referências)

---

## Objetivo

Este tutorial tem como objetivo:

- Instalar o **Miniconda**
- Compreender o funcionamento do **Conda**
- Criar ambientes isolados para bioinformática
- Padronizar o ambiente computacional da disciplina
- Evitar conflitos entre softwares

---

## O que é o Conda

O **Conda** é um gerenciador de pacotes e ambientes que permite instalar softwares científicos de forma reprodutível e isolada.

Ele é amplamente utilizado em bioinformática por facilitar a instalação de ferramentas complexas sem necessidade de compilação manual.

---

## Por que usar ambientes Conda

Ambientes Conda permitem:

- Isolar versões de programas
- Evitar conflitos entre dependências
- Garantir reprodutibilidade das análises
- Padronizar o ambiente entre alunos

Cada projeto ou disciplina pode ter seu próprio ambiente.

---

## Sistemas compatíveis

Este guia é válido para:

- Linux
- WSL (Windows Subsystem for Linux)
- macOS (Intel ou Apple Silicon)

---

## Download do Miniconda

Acesse o site oficial:

https://docs.conda.io/en/latest/miniconda.html

Escolha a versão:

- **Miniconda3 Linux x86_64** (Linux / WSL)
- **Miniconda3 macOS x86_64** (Mac Intel)
- **Miniconda3 macOS arm64** (Apple Silicon)

---

## Instalação do Miniconda

### Linux / WSL

```bash
bash Miniconda3-latest-Linux-x86_64.sh
```

### macOS

```bash
bash Miniconda3-latest-MacOSX-x86_64.sh
```

Durante a instalação:
- Aceite a licença
- Mantenha o diretório padrão
- Responda **yes** para inicializar o Conda

---

## Inicialização do Conda

Após a instalação:

```bash
source ~/.bashrc
```

Verifique:

```bash
conda --version
```

---

## Atualização do Conda

```bash
conda update -n base -c defaults conda
```

---

## Criação de um ambiente didático

Criação de um ambiente chamado `bioinfo_didatico`:

```bash
conda create -n bioinfo_didatico python=3.10
```

Ativação:

```bash
conda activate bioinfo_didatico
```

---

## Ativação e desativação do ambiente

Ativar:

```bash
conda activate bioinfo_didatico
```

Desativar:

```bash
conda deactivate
```

---

## Instalação de programas no ambiente

Exemplo de instalação de ferramentas comuns:

```bash
conda install -c bioconda -c conda-forge   fastqc   fastp   sra-tools   mafft   iqtree
```

---

## Verificação do ambiente

```bash
which fastqc
which fasterq-dump
which iqtree
```

Todos os comandos devem apontar para o diretório do ambiente Conda.

---

## Boas práticas

- Um ambiente por disciplina ou projeto
- Não instalar pacotes no ambiente `base`
- Documentar versões utilizadas
- Exportar o ambiente quando necessário

Exportar:

```bash
conda env export > bioinfo_didatico.yml
```

---

## Problemas comuns

### Conda não reconhecido
```bash
source ~/.bashrc
```

### Ambiente não ativa
- Verifique se o nome está correto
- Use `conda env list`

### Conflitos de dependência
- Criar um novo ambiente
- Evitar misturar canais desnecessários

---

## Referências

- Documentação oficial Conda  
  https://docs.conda.io/
- Bioconda  
  https://bioconda.github.io/

---
