# Download de dados de sequenciamento do NCBI SRA com SRA Toolkit

Guia didático para **instalação, configuração e uso do SRA Toolkit**, com foco em **`fasterq-dump`**, destinado a atividades práticas em bioinformática e filogenômica.

---

## Índice

1. [Objetivo](#objetivo)  
2. [O que é o NCBI SRA](#o-que-é-o-ncbi-sra)  
3. [Quando usar `fasterq-dump`](#quando-usar-fasterq-dump)  
4. [Ferramenta recomendada](#ferramenta-recomendada)  
5. [Instalação do SRA Toolkit](#instalação-do-sra-toolkit)  
6. [Configuração inicial](#configuração-inicial)  
7. [Organização do projeto](#organização-do-projeto)  
8. [Download de um único SRR](#download-de-um-único-srr)  
9. [Download de múltiplos SRRs](#download-de-múltiplos-srrs)  
10. [Parâmetros importantes](#parâmetros-importantes)  
11. [Verificação dos arquivos](#verificação-dos-arquivos)  
12. [Compactação dos FASTQ](#compactação-dos-fastq)  
13. [Problemas comuns](#problemas-comuns)  
14. [Próximos passos](#próximos-passos)  
15. [Referências](#referências)

---

## Objetivo

Este tutorial tem como objetivo ensinar como:

- Instalar corretamente o **SRA Toolkit**
- Configurar o ambiente para uso seguro
- Entender a diferença entre **SRA** e **GenBank**
- Baixar dados de sequenciamento **brutos (FASTQ)**
- Preparar os arquivos para análises posteriores

---

## O que é o NCBI SRA

O **Sequence Read Archive (SRA)** é o repositório do NCBI que armazena **leituras brutas de sequenciamento** (raw reads), provenientes de plataformas como:

- Illumina  
- Oxford Nanopore  
- PacBio  

Esses dados **não são fornecidos diretamente em FASTA** e precisam ser convertidos para o formato **FASTQ**.

Identificadores comuns:
- `SRR` (NCBI)
- `ERR` (ENA)
- `DRR` (DDBJ)

---

## Quando usar `fasterq-dump`

Use `fasterq-dump` quando:

- Os dados estão depositados no **SRA**
- Você precisa das **leituras brutas**
- Vai realizar montagem, mapeamento ou análises filogenômicas

Não use quando:

- Os dados já estão em **FASTA**
- As sequências vêm do **GenBank**
- Você está usando **loci UCE/AHE já processados**

---

## Ferramenta recomendada

O NCBI recomenda atualmente o uso de:

- **`fasterq-dump`**
- Mais rápido
- Mais estável
- Adequado para grandes volumes de dados

---

## Instalação do SRA Toolkit

### Pré-requisitos

- Linux, WSL ou macOS
- Conda ou Miniconda instalado

### Instalação via Conda

```bash
conda install -c bioconda sra-tools
```

### Verificação

```bash
fasterq-dump --version
```

---

## Configuração inicial

```bash
vdb-config --interactive
```

---

## Organização do projeto

```text
sra_project/
├── sra_accessions.txt
├── fastq/
└── logs/
```

```bash
mkdir -p fastq logs
```

---

## Download de um único SRR

```bash
fasterq-dump SRR12345678 --split-files --threads 4 --outdir fastq
```

---

## Download de múltiplos SRRs

```bash
while read SRR; do
  fasterq-dump "$SRR" --split-files --threads 4 --outdir fastq 2>> logs/fasterq.log
done < sra_accessions.txt
```

---

## Parâmetros importantes

| Parâmetro | Descrição |
|---------|----------|
| `--split-files` | Separa reads pareados |
| `--threads` | Número de CPUs |
| `--outdir` | Diretório de saída |

---

## Verificação dos arquivos

```bash
head fastq/SRR12345678_1.fastq
```

---

## Compactação dos FASTQ

```bash
gzip fastq/*.fastq
```

---

## Problemas comuns

- Falta de espaço em disco
- Download lento
- Acessos inválidos

---

## Próximos passos

- FastQC
- Trimagem
- Montagem
- Filogenômica

---

## Referências

- https://github.com/ncbi/sra-tools  
- https://www.ncbi.nlm.nih.gov/sra
