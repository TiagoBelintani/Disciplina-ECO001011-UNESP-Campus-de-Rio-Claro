# Redução do tamanho de arquivos FASTQ para uso didático

Guia prático para **reduzir o tamanho de arquivos FASTQ** provenientes do NCBI SRA, com foco em **subamostragem**, **trimagem** e **boas práticas** para aulas e testes computacionais.

Este material é complementar aos tutoriais de **Conda** e **download de dados SRA**.

---

## Índice

1. [Objetivo](#objetivo)  
2. [Por que reduzir arquivos FASTQ](#por-que-reduzir-arquivos-fastq)  
3. [Visão geral das estratégias](#visão-geral-das-estratégias)  
4. [Estratégia 1: Subamostragem de reads (recomendada)](#estratégia-1-subamostragem-de-reads-recomendada)  
5. [Estratégia 2: Número fixo de reads](#estratégia-2-número-fixo-de-reads)  
6. [Estratégia 3: Trimagem e filtragem](#estratégia-3-trimagem-e-filtragem)  
7. [Compressão dos arquivos](#compressão-dos-arquivos)  
8. [Fluxo didático recomendado](#fluxo-didático-recomendado)  
9. [O que evitar em aulas](#o-que-evitar-em-aulas)  
10. [Resumo comparativo](#resumo-comparativo)  
11. [Referências](#referências)

---

## Objetivo

Este tutorial tem como objetivo:

- Reduzir o tamanho de arquivos FASTQ para facilitar execução em sala de aula
- Diminuir tempo de processamento e uso de memória
- Preservar o realismo dos dados biológicos
- Padronizar datasets didáticos

---

## Por que reduzir arquivos FASTQ

Arquivos FASTQ completos geralmente:

- Possuem dezenas de milhões de reads
- São grandes (vários GB)
- Demandam alto custo computacional

Para aulas, isso causa:
- Execuções lentas
- Falhas por falta de memória
- Frustração para alunos iniciantes

---

## Visão geral das estratégias

Existem três abordagens principais:

- **Subamostragem de reads** (mais recomendada)
- **Limitação do número de reads**
- **Trimagem e filtragem de qualidade**

Compressão é complementar, mas não reduz custo computacional.

---

## Estratégia 1: Subamostragem de reads (recomendada)

### Descrição

Mantém apenas uma **fração aleatória** das leituras originais, preservando:

- Estrutura FASTQ
- Dados paired-end
- Variabilidade biológica

Ideal para aulas e demonstrações.

---

### Ferramenta: `seqtk`

#### Instalação
```bash
conda install -c bioconda seqtk
```

---

### Exemplo: manter 5% das reads

```bash
seqtk sample -s100 SRR12345678_1.fastq 0.05 > SRR12345678_1.sub.fastq
seqtk sample -s100 SRR12345678_2.fastq 0.05 > SRR12345678_2.sub.fastq
```

Parâmetros:
- `-s100`: semente fixa (reprodutibilidade)
- `0.05`: fração de reads (5%)

Percentuais recomendados:
- Demonstração rápida: 1–2%
- Aula prática completa: 2–5%

---

## Estratégia 2: Número fixo de reads

### Descrição

Seleciona um número absoluto de reads, independente do tamanho original.

Útil quando se deseja padronizar o dataset.

---

### Exemplo: 100.000 reads

```bash
seqtk sample -s100 SRR12345678_1.fastq 10000 > SRR12345678_1.100k.fastq
seqtk sample -s100 SRR12345678_2.fastq 10000 > SRR12345678_2.100k.fastq
```

---

## Estratégia 3: Trimagem e filtragem

### Descrição

Remove:
- Adaptadores
- Bases de baixa qualidade
- Reads muito curtas

Reduz o tamanho e melhora a qualidade, mas **menos eficiente** que subamostragem.

---

### Ferramenta: `fastp`

#### Instalação
```bash
conda install -c bioconda fastp
```

---

### Exemplo de uso

```bash
fastp   -i SRR12345678_1.fastq   -I SRR12345678_2.fastq   -o SRR12345678_1.trim.fastq   -O SRR12345678_2.trim.fastq   --length_required 50   --thread 4   --html fastp_report.html
```

---

## Compressão dos arquivos

### Descrição

Reduz apenas o espaço em disco.

Não reduz tempo de execução.

```bash
gzip *.fastq
```

---

## Fluxo didático recomendado

```text
FASTQ original
   ↓
Subamostragem (1–5%)
   ↓
FASTQ reduzido
   ↓
FastQC / montagem / filogenia
```

---

## O que evitar em aulas

- Trabalhar com FASTQ completos
- Usar dados muito grandes sem subamostragem
- Misturar subamostragem e trimagem sem explicação conceitual
- Alterar manualmente arquivos FASTQ

---

## Resumo comparativo

| Estratégia | Redução de tamanho | Mantém realismo | Uso didático |
|----------|------------------|------------------|--------------|
| Subamostragem | Alta | Alta | Recomendada |
| Número fixo | Alta | Média | Recomendada |
| Trimagem | Média | Alta | Opcional |
| Compressão | Disco apenas | Alta | Complementar |

---

## Referências

- Seqtk  
  https://github.com/lh3/seqtk
- Fastp  
  https://github.com/OpenGene/fastp

---
