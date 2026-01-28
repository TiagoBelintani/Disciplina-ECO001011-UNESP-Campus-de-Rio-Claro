## 📌 Índice

- [Visão geral do fluxo](#visão-geral-do-fluxo)
- [Requisitos](#requisitos)
- [Ambientes Conda](#ambientes-conda)
- [Estrutura de diretórios](#estrutura-de-diretórios)
- [Acesso aos dados (NCBI SRA)](#acesso-aos-dados-ncbi-sra)
- [Verificação de Integridade e Quantificação](#verificação-de-integridade-e-quantificação)
- [Limpeza com Trim Galore (local)](#limpeza-com-trim-galore-local)
- [Primeira Opção - Trimgalore](#primeira-opção---trimgalore)
- [Segunda Opção - Trimmomatic](#segunda-opção---trimmomatic)
- [Montagem dos dados "trimados"](#montagem-dos-dados-trimados)
- [Montagem dos Dados com SPAdes](#montagem-dos-dados-com-spades)
- [Passos Práticos](#passos-práticos)
- [Preparar o Arquivo de Configuração](#1-preparar-o-arquivo-de-configuração)
- [Identificação de loci UCE](#identificação-de-loci-uce)
- [Extração de loci](#extração-de-loci)
- [Alinhamento (MAFFT)](#alinhamento-mafft)
- [Poda interna com Gblocks](#poda-interna-com-gblocks)
- [Matrizes por ocupância (ex.: 75%)](#matrizes-por-ocupância-ex-75)
- [Gene trees (IQ-TREE 3, local)](#gene-trees-iq-tree-3-local)
- [Species tree (ASTRAL local)](#species-tree-astral-local)
- [Concatenado (IQ-TREE 3)](#concatenado-iq-tree-3)
- [Bayesiano (MrBayes, local)](#bayesiano-mrbayes-local)
- [Observação final](#observação-final)
- [Referências](#referências)

apenas arruma este link os topicos sem mudar porra nenhuma reveja este .md sem mudancas mais arrumando pontos preciso problematicos e gere o hyperlinks no inicio <img width="1168" height="76" alt="image" src="https://github.com/user-attachments/assets/85761180-ceb7-4147-a373-baab2abdd3ef" /># Tutorial: Filogenômica com Elementos Ultraconservados (UCEs) — **Execução Local**


> **Versão LOCAL (Linux / macOS / WSL)**  
> Este tutorial descreve **todo o pipeline UCE** desde o download dos dados até as análises filogenéticas,


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
Download 
```bash
 fasterq-dump SRR32233423 --split-files --threads 4 --outdir raw-fastq
```

Acessar dados pré-processados

Salvar na pasta raw-fastq

```bash
https://mega.nz/file/oRBGFBrQ#AuWgPbEPMY_8llbiBYBIPgX26x9G7JwPM245bzElCR8
```
Organizar diretório e preparar

```bash
unzip DADOS_Idiopidae-20260125T191837Z-3-001.zip
---
mv DADOS_Idiopidae/*.gz ~/uce_treinamento/raw-fastq
---
ls
---
Apagar dado reduntante

rm -rf SRR32233422_1.fastq.gz SRR32233422_2.fastq.gz
```


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

# Primeira Opção - Trimgalore

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
```
Checagem 

```bash
for d in clean-fastq/SRR32*/; do
  echo ">>> $(basename "$d")"
  ls "$d"/*val_*.fq.gz 2>/dev/null | wc -l
done

```
Contar quantas amostras têm trimming completo

```bash
find clean-fastq/SRR32* -name "*_val_1.fq.gz" | wc -l
find clean-fastq/SRR32* -name "*_val_2.fq.gz" | wc -l
```

---
# Segunda Opção - Trimmomatic


Instalar Trimmomatic no ambiente bioinfo_didatico

```bash
conda install bioconda::trimmomatic
```

Exucutar  a trimmagem dos dados

**importante verificar o diretório**

```bash
pwd
```
No diretório ~/uce_treinamento

Executar
```bash
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
```

Este script:

percorre todas as amostras, remove adaptadores, corta regiões de baixa qualidade, descarta reads curtas e gera FASTQs limpos pareados, prontos para análises filogenômicas.

---

Finalizar o ambiente

```bash
conda deactivate
```

# Montagem dos dados "trimados"

### Phyluce <https://phyluce.readthedocs.io/en/latest/tutorials/index.html>


**PHYLUCE (PHYlogenetic estimation Using Loci from UltraConserved Elements)** é um conjunto integrado de ferramentas em Python desenvolvido para processar, organizar e analisar dados de captura de alvos — especialmente Elementos Ultraconservados (UCEs) e AHE/exons — com o objetivo de inferência filogenética em larga escala.

Em termos práticos, o PHYLUCE automatiza o caminho entre dados brutos de sequenciamento e matrizes filogenéticas, permitindo:
(i) montar contigs a partir de leituras,
(ii) identificar quais contigs correspondem aos loci-alvo (probes),
(iii) extrair e organizar esses loci por táxon,
(iv) alinhar sequências homólogas e
(v) gerar matrizes filtradas por ocupância para análises concatenadas ou baseadas em árvores gênicas.

Do ponto de vista conceitual, o PHYLUCE não infere árvores; ele prepara dados filogenômicos de forma padronizada e reprodutível. Seu papel central é garantir homologia correta entre loci, controle de qualidade e consistência na construção de supermatrizes e conjuntos de alinhamentos multi-locus, que depois são analisados por programas como IQ-TREE, RAxML, ASTRAL ou MrBayes.

Criar o ambiente Conda para o PHYLUCE

Acessar versões disponíveis

Acessar diretório

```bash
cd ~/uce_treinamento/programas
```

```bash
https://github.com/faircloth-lab/phyluce/releases
```

```bash
Linux

wget https://raw.githubusercontent.com/faircloth-lab/phyluce/v1.7.3/distrib/phyluce-1.7.3-py36-Linux-conda.yml

conda env create -n phyluce_1.7.3 --file phyluce-1.7.3-py36-Linux-conda.yml
```
Iniciar ambiente

```bash
conda activate phyluce_1.7.3
```

Testar

```bash
phylu<tab> enter
```

Preparar pastas
Arquivo de mapeamento (SRR → espécie)

Garanta que você tem este arquivo EXATAMENTE assim (TAB entre colunas):

```bash
nano rename_map.tsv
```
colar 
```bash
SRR32233422	Moggridgea_crudeni
SRR32233423	Arbanitis_rapax
SRR32233424	Galeosoma_sp
SRR32392845	Idiops_fryi
SRR32392846	Idiops_rohdei
SRR32392847	Idiops_rastratus
SRR32392848	Idiops_camelus
SRR32392849	Idiops_guri
SRR32392850	Idiops_petiti
SRR32392851	Idiops_germaini
SRR32392852	Cteniza_sp
SRR32392853	Idiops_clarus
SRR32392854	Neocteniza_toba
SRR32392855	Titanidiops_sp
SRR32392856	Segregara_transvaalensis
SRR32392857	Heligmomerus_sp
SRR32392858	Gorgyrella_namaquensis
SRR32392859	Ctenolophus_sp
SRR32392860	Idiops_sp3
SRR32392861	Idiops_sp2
SRR32392862	Idiops_pretoriae
SRR32392863	Idiops_kanonganus
SRR32392864	Idiops_carajas
SRR32392865	Idiops_pirassununguensis
```
Mover, renomear e organizar

No diretório uce_treinamento

```bash
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
```



Cheque uma espécie:
```bash
ls clean-fastq/Arbanitis_rapax/split-adapter-quality-trimmed
```

Esperado:
```bash
Arbanitis_rapax_R1.fastq.gz
Arbanitis_rapax_R2.fastq.gz
```

Cheque várias:

```bash
find clean-fastq -name "*_R1.fastq.gz" | wc -l
```

Deve dar 24 

Apagar as pastas SRR

```bash
rm -rf clean-fastq/SRR*
```

Isso limpa a bagunça sem risco.
---
## Montagem dos Dados com SPAdes


<div align="justify">
No fluxo de análise de dados no PHYLUCE, a etapa de montagem é responsável por reconstruir sequências contíguas (contigs) a partir das leituras limpas de sequenciamento. 
Para isso, o PHYLUCE oferece suporte a diferentes programas de montagem, todos integrados por meio de scripts próprios, mantendo um padrão de entrada e saída.

Os montadores disponíveis no <a href="https://phyluce.readthedocs.io/en/latest/">Phyluce</a> incluem:

[SPAdes](https://github.com/ablab/spades): geralmente a opção recomendada. É fácil de instalar, produz resultados consistentes e costuma apresentar melhor desempenho na maioria dos conjuntos de dados processados com PHYLUCE.

[Velvet](https://github.com/dzerbino/velvet): indicado para montagens de genomas menores ou dados com boa cobertura, sendo eficiente e rápido em cenários menos complexos.

[ABySS](https://pmc.ncbi.nlm.nih.gov/articles/PMC5411771/): voltado para conjuntos de dados maiores ou genomas mais complexos, capaz de lidar com grandes volumes de leituras.

Para utilizar o Velvet dentro do PHYLUCE, o comando típico é:
</div>

```bash
phyluce_assembly_assemblo_velvet \ 
  --conf assembly.conf \ 
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

# Passos Práticos

## 1. Preparar o Arquivo de Configuração

<div align="justify"> 
O arquivo `assembly.conf` é essencial para que o <a href="https://phyluce.readthedocs.io/en/latest/">Phyluce</a> saiba onde encontrar os arquivos de leituras já limpas de cada amostra.  

Ele deve conter uma lista com o nome da amostra e o caminho para o diretório `split-adapter-quality-trimmed` correspondente.

Pode ser facilmente construido usando um editor de tabelas (excel ou outro pacote).

ou automaticamente
```bash
BASE="clean-fastq"
OUT="samples.conf"

echo "[samples]" > "$OUT"

for d in $BASE/*/split-adapter-quality-trimmed; do
  species=$(basename "$(dirname "$d")")
  echo "${species}:$(pwd)/${d}" >> "$OUT"
done
```

Criar uma pasta de log

```bash
mkdir log
```


## Iniciar as montagens 

```bash
conda activate phyluce-1.7.3
```

```bash
conda install -c bioconda velvet
```

```bash
phyluce_assembly_assemblo_velvet --output assembly --kmer 31 --cores 4 --log-path log  --config samples.conf
```

montangens

```bash
https://mega.nz/folder/pBQS0LDZ#iNkC7iV3r9N1se5PXo_exg
```

## Identificação de loci UCE

Acesar as probes 

```bash
https://mega.nz/file/dcogTRJC#0Eu5D4N2J9Wf0VNfgwNPDlBCoblrVsTqBySwTNjZv3s
```

Salvar as probes em `probes/probes.fasta`.

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


  

