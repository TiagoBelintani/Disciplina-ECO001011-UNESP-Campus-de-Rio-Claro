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

```bash
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

verifique a instalação do Gzip e sra-tools

```bash
conda install bioconda::sra-tools
```

em seguida

```bash
gzip --version
```

Instalar
```bash
conda install conda-forge::gzip
```


```bash
while read SRR; do
  fasterq-dump $SRR --split-files --threads 4 --outdir raw-fastq
  gzip raw-fastq/${SRR}*.fastq
done < srr_list.txt
```

Acessar dados pré-processados

Salvar na pasta raw-fastq

```bash
https://mega.nz/file/oRBGFBrQ#AuWgPbEPMY_8llbiBYBIPgX26x9G7JwPM245bzElCR8
```
---
## Verificação de Integridade e Quantificação

Para contar o número de reads em cada arquivo .fastq.gz:

```bash
for i in raw-fastq/*.fastq.gz; do
  echo "$i"
  gunzip -c "$i" | wc -l | awk '{print $1/4}'
done
```

---

## Limpeza com Trim Galore (local)

<div align="justify">
A limpeza de dados de sequenciamento de nova geração (NGS) é um passo crucial para garantir a qualidade e a confiabilidade das análises subsequentes. Ferramentas como o <a href="https://github.com/FelixKrueger/TrimGalore">Trim Galore</a> e o <a href="https://github.com/timflutre/trimmomatic">Trimmomatic</a> atuam removendo sequências adaptadoras e filtrando leituras de baixa qualidade, que podem introduzir ruído ou enviesar resultados. Durante o processo de sequenciamento, é comum que resíduos técnicos, como adaptadores não removidos ou bases com qualidade deteriorada nas extremidades, se acumulem nas leituras. Esses artefatos, se não tratados, podem levar a alinhamentos incorretos, montagem de genomas incompleta e interpretações equivocadas dos dados biológicos.
</div>


Instalar
```bash
conda install bioconda::trim-galore
```
Testar

```bash
trim-galore -v
```
exemplo
```bash
trim_galore -v

                        Quality-/Adapter-/RRBS-/Speciality-Trimming
                                [powered by Cutadapt]
                                  version 0.6.10

                               Last update: 02 02 2023
```
Executar a ferramenta em loop

```bash
for r1 in raw-fastq/*_1.fastq.gz; do
  sample=$(basename $r1 _1.fastq.gz)
  trim_galore --paired     raw-fastq/${sample}_1.fastq.gz     raw-fastq/${sample}_2.fastq.gz     --cores 4     --gzip     --output_dir clean-fastq/${sample}
done
```

---
## Montagem dos Dados com SPAdes

<div align="justify">
No fluxo de análise de dados no PHYLUCE, a etapa de montagem é responsável por reconstruir sequências contíguas (contigs) a partir das leituras limpas de sequenciamento. 
Para isso, o PHYLUCE oferece suporte a diferentes programas de montagem, todos integrados por meio de scripts próprios, mantendo um padrão de entrada e saída.

Os montadores disponíveis no <a href="https://phyluce.readthedocs.io/en/latest/">Phyluce</a> incluem:

[SPAdes](https://github.com/ablab/spades): geralmente a opção recomendada. É fácil de instalar, produz resultados consistentes e costuma apresentar melhor desempenho na maioria dos conjuntos de dados processados com PHYLUCE.

[Velvet](https://github.com/dzerbino/velvet): indicado para montagens de genomas menores ou dados com boa cobertura, sendo eficiente e rápido em cenários menos complexos.

[ABySS](https://pmc.ncbi.nlm.nih.gov/articles/PMC5411771/): voltado para conjuntos de dados maiores ou genomas mais complexos, capaz de lidar com grandes volumes de leituras.

Para utilizar o SPAdes dentro do PHYLUCE, o comando típico é:
</div>

```bash
phyluce_assembly_assemblo_spades \ 
  --conf assembly.conf \ %+
  --output spades-assemblies \
  --cores 12 \
  --memory 64
```

**Explicação dos parâmetros:**

```bash
--conf assembly.conf → Arquivo de configuração que lista as amostras, os caminhos para os arquivos FASTQ e parâmetros opcionais de montagem.

--output spades-assemblies → Pasta onde os resultados da montagem serão salvos. Cada amostra terá seu próprio diretório com os contigs.

--cores 12 → Número de núcleos de CPU a serem usados, acelerando o processamento.

--memory 64 → Quantidade de memória RAM (em GB) disponível para a execução do SPAdes.

Após a execução, a pasta de saída conterá os contigs prontos para as próximas etapas, como identificação e extração dos loci alvo.
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


  
