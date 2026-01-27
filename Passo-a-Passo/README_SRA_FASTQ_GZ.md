# Download de dados do NCBI SRA em FASTQ.GZ

Este repositório fornece um **workflow simples, robusto e reprodutível** para baixar dados do **NCBI Sequence Read Archive (SRA)** e gerar arquivos **.fastq.gz**, prontos para análises genômicas (UCE, AHE, WGS, RNA-seq).

O tutorial foi desenhado para **execução local** (Linux, macOS ou Windows via WSL), sem SLURM ou HPC.

---

## Visão geral do fluxo

SRR list (.txt) → fasterq-dump → FASTQ → compressão → FASTQ.GZ

---

## Requisitos

- Conda / Miniconda
- Linux, macOS ou Windows (WSL)
- Espaço em disco suficiente (FASTQs podem ser grandes)

---

## Instalação do SRA Toolkit

```bash
conda create -n sra -c bioconda sra-tools -y
conda activate sra
```

Verifique:

```bash
fasterq-dump --version
```

---

## Estrutura do projeto

```text
.
├── srr_list.txt
├── fastq/
└── logs/
```

Crie os diretórios:

```bash
mkdir -p fastq logs
```

---

## Lista de acessos SRA

Edite `srr_list.txt` com **um SRR por linha**:

```text
SRR32392853
SRR32392854
SRR32392855
```

---

## Download dos dados (gerando FASTQ.GZ)

> O `fasterq-dump` não gera `.gz` diretamente.  
> A compactação é feita logo após o download.

```bash
while read SRR; do
  echo "Baixando ${SRR}..."

  fasterq-dump ${SRR} \
    --split-files \
    --threads 4 \
    --outdir fastq \
    >> logs/fasterq.log 2>&1

  gzip fastq/${SRR}*.fastq
done < srr_list.txt
```

### Resultado esperado

- **Paired-end**
  - SRRxxxx_1.fastq.gz
  - SRRxxxx_2.fastq.gz

- **Single-end**
  - SRRxxxx.fastq.gz

---

## Verificação

```bash
ls -lh fastq
```

Buscar erros:

```bash
grep -i error logs/fasterq.log
```

---

## Dica de performance (opcional)

Use compressão paralela com `pigz`:

```bash
conda install -c conda-forge pigz
```

Substitua `gzip` por:

```bash
pigz fastq/${SRR}*.fastq
```

---

## Observações importantes

- `--split-files` funciona para dados paired-end e single-end
- Nunca execute `gzip` antes do término do download
- Confira espaço em disco antes de iniciar

---

## Referências

- NCBI SRA Toolkit  
  https://github.com/ncbi/sra-tools
