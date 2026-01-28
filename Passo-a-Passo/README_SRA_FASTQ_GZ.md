# Tutorial: Filogenômica com Elementos Ultraconservados (UCEs) — **Execução Local**

> **Versão LOCAL (Linux / macOS / WSL)**  
> Este tutorial descreve **todo o pipeline UCE**, desde o download dos dados até as análises filogenéticas.

---

## 📌 Índice

- [Visão geral do fluxo](#visão-geral-do-fluxo)
- [Requisitos](#requisitos)
- [Ambientes Conda](#ambientes-conda)
- [Estrutura de diretórios](#estrutura-de-diretórios)
- [Acesso aos dados (NCBI SRA)](#acesso-aos-dados-ncbi-sra)
- [Verificação de integridade](#verificação-de-integridade-e-quantificação)
- [Limpeza com Trim Galore / Trimmomatic](#limpeza-com-trim-galore-local)
- [Montagem dos dados (PHYLUCE)](#montagem-dos-dados-trimados)
- [Montagem com Velvet](#montagem-com-velvet-recomendada-no-macos)
- [Identificação de loci UCE](#identificação-de-loci-uce)
- [Alinhamento (MAFFT)](#alinhamento-mafft)
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

---

## Requisitos

- Linux / macOS / Windows (WSL)
- Conda / Miniconda
- ≥ 16 GB RAM recomendado
- ≥ 50 GB espaço em disco

---

## Ambientes Conda

```bash
conda activate bioinfo_didatico
```

---

## Estrutura de diretórios

```bash
uce_treinamento/
├── raw-fastq/
├── clean-fastq/
├── assembly/
├── probes/
├── taxon-set/
│   └── all/
└── log/
```

---

## Acesso aos dados (NCBI SRA)

**BioProject:** PRJNA1161786  
https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SRP561602

---

## Limpeza com Trim Galore (local)

```bash
conda install -c bioconda trim-galore
```

```bash
for r1 in raw-fastq/*_R1.fastq.gz; do
  sample=$(basename "$r1" _R1.fastq.gz)
  mkdir -p clean-fastq/"$sample"
  trim_galore --paired     raw-fastq/"${sample}_R1.fastq.gz"     raw-fastq/"${sample}_R2.fastq.gz"     --cores 4     --gzip     --output_dir clean-fastq/"$sample"
done
```

---

## Montagem dos dados "trimados"

PHYLUCE: https://phyluce.readthedocs.io/en/latest/

---

## Montagem com Velvet (recomendada no macOS)

```bash
conda install -c bioconda velvet
```

```bash
phyluce_assembly_assemblo_velvet   --output assembly   --kmer 31   --cores 4   --log-path log   --config samples.conf
```

---

## Identificação de loci UCE

```bash
phyluce_assembly_match_contigs_to_probes   --contigs assembly/contigs   --probes probes/probes.fasta   --output uce-matches   --min-coverage 80   --min-identity 80
```

---

## Alinhamento (MAFFT)

```bash
phyluce_align_seqcap_align   --input taxon-set/all/all-taxa-incomplete.fasta   --output taxon-set/all/mafft   --aligner mafft   --cores 4   --incomplete-matrix   --no-trim
```

---


- Tiago Belintani 2026

