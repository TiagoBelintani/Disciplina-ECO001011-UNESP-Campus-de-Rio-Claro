<img width="1168" height="76" alt="image" src="https://github.com/user-attachments/assets/85761180-ceb7-4147-a373-baab2abdd3ef" />

# Tutorial: Filogenômica com Elementos Ultraconservados (UCEs) — **Execução Local**

> **Versão LOCAL (Linux / macOS / WSL)**  
> Este tutorial descreve **todo o pipeline UCE**, desde o download dos dados até as análises filogenéticas.

---

## 📌 Índice (atalhos rápidos)

- [Visão geral do fluxo](#visão-geral-do-fluxo)
- [Requisitos](#requisitos)
- [Ambientes Conda](#ambientes-conda)
- [Estrutura de diretórios](#estrutura-de-diretórios)
- [Acesso aos dados (NCBI SRA)](#acesso-aos-dados-ncbi-sra)
- [Verificação de integridade](#verificação-de-integridade-e-quantificação)
- [Limpeza com Trim Galore / Trimmomatic](#limpeza-com-trim-galore-local)
- [Montagem dos dados (PHYLUCE)](#montagem-dos-dados-trimados)
- [Montagem com Velvet](#montagem-dos-dados-com-spades)
- [Identificação de loci UCE](#identificação-de-loci-uce)
- [Alinhamento e filtragem](#alinhamento-mafft)
- [Inferência filogenética](#gene-trees-iq-tree-3-local)
- [Referências](#referências)

---

## Visão geral do fluxo

1. Download dos dados (SRA → FASTQ.GZ)  
2. Controle de qualidade e limpeza (Trim Galore / Trimmomatic)  
3. Montagem de contigs (Velvet ou SPAdes via PHYLUCE)  
4. Identificação de loci UCE (PHYLUCE)  
5. Extração de FASTAs e filtragem por ocupância  
6. Alinhamento (MAFFT)  
7. Poda interna (Gblocks)  
8. Matrizes finais  
9. Inferência filogenética  
   - Gene trees (IQ-TREE 3)  
   - Species tree (ASTRAL)  
   - Concatenado (IQ-TREE 3)  
   - Bayesiano (MrBayes)  

---

## Requisitos

- Linux / macOS / Windows (WSL)
- Conda / Miniconda
- ≥ 16 GB RAM recomendado
- ≥ 50 GB espaço em disco (dependente do dataset)

---

## Ambientes Conda

Ativar ambiente principal:

```bash
conda activate bioinfo_didatico
ou (forma explícita):

source ~/miniconda3/bin/activate bioinfo_didatico
Estrutura de diretórios
uce_treinamento/
├── raw-fastq/
├── clean-fastq/
├── assembly/
├── probes/
├── taxon-set/
│   └── all/
└── log/
Criar a estrutura:

mkdir -p raw-fastq clean-fastq assembly probes taxon-set/all log
Acessar o projeto:

cd uce_treinamento
Acesso aos dados (NCBI SRA)
BioProject: PRJNA1161786
🔗 https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SRP561602

Criar lista de SRRs:

nano srr_list.txt
Exemplo:

SRR32233422
Download local (FASTQ.GZ)
Instalar dependências:

conda install -c bioconda sra-tools
conda install -c conda-forge gzip
Download em lote:

while read SRR; do
  fasterq-dump $SRR --split-files --threads 4 --outdir raw-fastq
  gzip raw-fastq/${SRR}*.fastq
done < srr_list.txt
Verificação de Integridade e Quantificação
for i in raw-fastq/*.fastq.gz; do
  echo "$i"
  gunzip -c "$i" | wc -l | awk '{print $1/4}'
done
Limpeza com Trim Galore (local)
🔗 Trim Galore: https://github.com/FelixKrueger/TrimGalore
🔗 Trimmomatic: https://github.com/timflutre/trimmomatic

Opção 1 — Trim Galore
Instalar:

conda install -c bioconda trim-galore
Executar:

for r1 in raw-fastq/*_R1.fastq.gz; do
  sample=$(basename "$r1" _R1.fastq.gz)

  mkdir -p clean-fastq/"$sample"

  trim_galore --paired \
    raw-fastq/"${sample}_R1.fastq.gz" \
    raw-fastq/"${sample}_R2.fastq.gz" \
    --cores 4 \
    --gzip \
    --output_dir clean-fastq/"$sample"
done
Segunda Opção — Trimmomatic
conda install -c bioconda trimmomatic
for r1 in raw-fastq/*_R1.fastq.gz; do
  sample=$(basename "$r1" _R1.fastq.gz)

  mkdir -p clean-fastq/"$sample"

  trimmomatic PE \
    -threads 4 \
    -phred33 \
    raw-fastq/"${sample}_R1.fastq.gz" \
    raw-fastq/"${sample}_R2.fastq.gz" \
    clean-fastq/"$sample"/"${sample}_R1_paired.fastq.gz" \
    clean-fastq/"$sample"/"${sample}_R1_unpaired.fastq.gz" \
    clean-fastq/"$sample"/"${sample}_R2_paired.fastq.gz" \
    clean-fastq/"$sample"/"${sample}_R2_unpaired.fastq.gz" \
    ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 \
    LEADING:3 \
    TRAILING:3 \
    SLIDINGWINDOW:4:20 \
    MINLEN:20
done
Montagem dos dados "trimados"
🔗 PHYLUCE: https://phyluce.readthedocs.io/en/latest/

Importante: o PHYLUCE não monta árvores, apenas prepara dados filogenômicos de forma padronizada.

Instalação do PHYLUCE
🔗 Releases: https://github.com/faircloth-lab/phyluce/releases

conda env create -n phyluce-1.7.3 --file phyluce-1.7.3-py36-Linux-conda.yml
conda activate phyluce-1.7.3
Organização dos FASTQs por espécie
Criar rename_map.tsv (TAB entre colunas):

SRR32233423	Arbanitis_rapax
SRR32233424	Galeosoma_sp
...
Script de organização:

BASE="clean-fastq"

while read srr species; do
  INDIR="$BASE/$srr"
  OUTDIR="$BASE/$species/split-adapter-quality-trimmed"

  mkdir -p "$OUTDIR"

  cp "$INDIR/${srr}_R1_paired.fastq.gz" \
     "$OUTDIR/${species}_R1.fastq.gz"

  cp "$INDIR/${srr}_R2_paired.fastq.gz" \
     "$OUTDIR/${species}_R2.fastq.gz"

done < rename_map.tsv
Montagem com Velvet (recomendada no macOS)
conda install -c bioconda velvet
phyluce_assembly_assemblo_velvet \
  --output assembly \
  --kmer 31 \
  --cores 4 \
  --log-path log \
  --config samples.conf
Identificação de loci UCE
phyluce_assembly_match_contigs_to_probes \
  --contigs assembly/contigs \
  --probes probes/probes.fasta \
  --output uce-matches \
  --min-coverage 80 \
  --min-identity 80
Alinhamento (MAFFT)
phyluce_align_seqcap_align \
  --input taxon-set/all/all-taxa-incomplete.fasta \
  --output taxon-set/all/mafft \
  --aligner mafft \
  --cores 4 \
  --incomplete-matrix \
  --no-trim
Referências
Faircloth BC (2016) PHYLUCE. Bioinformatics

Zhang et al. (2018, 2025) ASTRAL

Castresana (2000) Gblocks


Tiago Belintani 2026
