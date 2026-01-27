# Tutorial: Filogenômica com Elementos Ultraconservados (UCEs) — **Execução Local**

> **Versão LOCAL (Linux / macOS / WSL)**  
> Este tutorial descreve **todo o pipeline UCE** desde o download dos dados até as análises filogenéticas,
> **sem SLURM, sem HPC**, executando diretamente no terminal.
>  
> Ideal para aulas, notebooks pessoais e reprodutibilidade fora de clusters.

---

## Visão geral do fluxo

1. Download dos dados (SRA → FASTQ.GZ)
2. Controle de qualidade e limpeza (Trim Galore)
3. Montagem de contigs (SPAdes via PHYLUCE)
4. Identificação de loci UCE (PHYLUCE)
5. Extração de FASTAs e filtragem por ocupância
6. Alinhamento (MAFFT)
7. Poda interna (Gblocks)
8. Matrizes finais
9. Inferência filogenética:
   - Gene trees (IQ-TREE 3)
   - Species tree (ASTRAL)
   - Concatenado (IQ-TREE 3)
   - Bayesiano (MrBayes)

---

## Requisitos

- Linux / macOS / Windows (WSL)
- Conda / Miniconda
- ≥ 16 GB RAM recomendado
- ≥ 50 GB espaço em disco (depende do dataset)

---

## Ambientes Conda

Iniciar ambiente

```bash
conda activate bioinfo_didatico
```
ou
``bash
source ~/miniconda3/envs/bioinfo_didatico
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
Acessar diretório
```bash
cd uce_treinamento
```
## Criar novos diretórios

```bash
mkdir -p raw-fastq clean-fastq assembly probes taxon-set/all,log
```

---

## Acesso aos dados (NCBI SRA)

**BioProject:** PRJNA1161786  
https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SRP561602

Crie `srr_list.txt` com um SRR por linha.

```bash
nano srr_list.txt
```

copie e cole

```bash
SRR32233422
```

### Download local (FASTQ.GZ)

```bash
while read SRR; do
  fasterq-dump $SRR --split-files --threads 4 --outdir raw-fastq
  gzip raw-fastq/${SRR}*.fastq
done < srr_list.txt
```

---

## Limpeza com Trim Galore (local)

Instalar
```bash
conda install bioconda::trim-galore
```
Testar

```bash
trim-galore --version
```

```bash
for r1 in raw-fastq/*_1.fastq.gz; do
  sample=$(basename $r1 _1.fastq.gz)
  trim_galore --paired     raw-fastq/${sample}_1.fastq.gz     raw-fastq/${sample}_2.fastq.gz     --cores 4     --gzip     --output_dir clean-fastq/${sample}
done
```

---

## Montagem com SPAdes (via PHYLUCE, local)

Criar `assembly.conf` automaticamente:

```bash
echo "[samples]" > assembly.conf
for d in clean-fastq/*; do
  s=$(basename $d)
  echo "$s:$PWD/$d" >> assembly.conf
done
```

Executar montagem:

```bash
phyluce_assembly_assemblo_spades   --conf assembly.conf   --output assembly   --cores 8   --memory 32
```

---

## Identificação de loci UCE

Coloque as probes em `probes/probes.fasta`.

```bash
phyluce_assembly_match_contigs_to_probes   --contigs assembly/contigs   --probes probes/probes.fasta   --output uce-matches   --min-coverage 80   --min-identity 80
```

---

## Extração de loci

Criar lista de táxons:

```bash
echo "[all]" > taxa.conf
ls uce-matches | grep -v sqlite >> taxa.conf
```

Contagem:

```bash
phyluce_assembly_get_match_counts   --locus-db uce-matches/probe.matches.sqlite   --taxon-list-config taxa.conf   --taxon-group all   --incomplete-matrix   --output taxon-set/all/all-taxa-incomplete.conf
```

Extração FASTA:

```bash
phyluce_assembly_get_fastas_from_match_counts   --contigs assembly/contigs   --locus-db uce-matches/probe.matches.sqlite   --match-count-output taxon-set/all/all-taxa-incomplete.conf   --output taxon-set/all/all-taxa-incomplete.fasta   --incomplete-matrix taxon-set/all/all-taxa-incomplete.incomplete
```

---

## Alinhamento (MAFFT)

```bash
phyluce_align_seqcap_align   --input taxon-set/all/all-taxa-incomplete.fasta   --output taxon-set/all/mafft   --aligner mafft   --cores 4   --incomplete-matrix   --no-trim
```

---

## Poda interna com Gblocks

```bash
phyluce_align_get_gblocks_trimmed_alignments_from_untrimmed   --alignments taxon-set/all/mafft   --output taxon-set/all/mafft-gblocks   --b1 0.5 --b2 0.85 --b3 4 --b4 8   --cores 2
```

Limpar cabeçalhos:

```bash
phyluce_align_remove_locus_name_from_files   --alignments taxon-set/all/mafft-gblocks   --output taxon-set/all/mafft-gblocks-clean
```

---

## Matrizes por ocupância (ex.: 75%)

```bash
phyluce_align_get_only_loci_with_min_taxa   --alignments taxon-set/all/mafft-gblocks-clean   --taxa 10   --percent 0.75   --output taxon-set/all/75p
```

---

## Gene trees (IQ-TREE 3, local)

```bash
for aln in taxon-set/all/75p/*.fasta; do
  iqtree3 -s $aln -m MFP -bb 1000 -alrt 1000 -nt 4
done
```

---

## Species tree (ASTRAL local)

```bash
cat taxon-set/all/75p/*.treefile > genes.tree
nw_ed genes.tree 'i & b<=10' o > pruned.tree
astral4 -i pruned.tree -o species.tree
```

---

## Concatenado (IQ-TREE 3)

```bash
phyluce_align_concatenate_alignments   --alignments taxon-set/all/75p   --output taxon-set/all/concat   --phylip
```

```bash
iqtree3 -s taxon-set/all/concat.phylip   -m MFP+MERGE   -bb 1000   -alrt 1000   -nt AUTO
```

---

## Bayesiano (MrBayes, local)

```bash
mb taxon-set/all/concat.nexus
```

Adicionar bloco `begin mrbayes;` conforme necessário.

---

## Observação final

Este tutorial é **100% executável localmente**, sem dependência de SLURM ou HPC.
Para datasets grandes, reduza:
- número de threads
- percentuais de ocupância
- número de réplicas de bootstrap

---

## Referências

- Faircloth BC (2016) PHYLUCE — *Bioinformatics*
- Zhang et al. (2018, 2025) ASTRAL / ASTER
- Castresana (2000) Gblocks


  
