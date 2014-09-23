#!/bin/bash
#
# Caro eu do futuro,
# se vc está lendo esse script, significa que ele está falhando miseravelmente.
# Conselho de amigo: nem se de ao trabalho de corrigir. Ele não funciona pq foi muito malfeito mesmo.
# Recomece do zero.
# 
# Sinceramente,
# Eu.
# 
# 
# 
# PS: e essa barba  
# PS2: vc vai aachar muito util ter deixado as char muito util ter deixado as linhas do SAM começando com @
# PS3: significado das flags do SAM -> "sam flags explain"
# PS4: o script assume que vc já possui a seguinte estrutura:
#        NGS_lab/fastq/ERR001268_1.filt.fastq.gz
#        NGS_lab/fastq/ERR001268_2.filt.fastq.gz
#        NGS_lab/reference/chr22.fa
#        NGS_lab/reference/bwa/0.6.1/chr22.fa -> ../../chr22.fa
 

workDir=$HOME/cursoOntario/NGS_lab
currDir=`pwd`

cd $workDir/analysis/bwa/0.6.1
#
# ### 1) vamos indexar o fasta de referencia
# 
# bwa index $workDir/reference/bwa/0.6.1/chr22.fa
# 
# ### 2) alinhar os reads ao genoma indexado
# 
# 
# for x in 1 2; do
#     bwa aln -t 15 reference/bwa/0.6.1/chr22.fa \
#         fastq/ERR001268_$x.filt.fastq.gz \
#         > ERR001268_$x.sai
# done
# 
# ### 3) combinar os reads em um SAM
# 
# bwa sampe \
#     -r "@RG\tID:ER001268\tSM:Sample1\tLB:library1\tPL:Illumina\tPU:NONE" \
#     reference/bwa/0.6.1/chr22.fa \
#     ERR001268_1.sai \
#     ERR001268_2.sai \
#     fastq/ERR001268_1.filt.fastq.gz \
#     fastq/ERR001268_2.filt.fastq.gz \
#     > ERR001268.sam
# 
# #### 4) SAM 2 BAM
# 
# samtools view -Sbo ERR001268.bam ERR001268.sam
# echo "[tip] check your bam with samtools view -h" 1>&2
# echo "[tip] if it is ok, u may delete the sam file and save space" 1>&2
# 
# ### 5) Sorted BAM
# 
# samtools sort ERR001268.bam ERR001268_sort 
# 
# 
# ### 6) Remove PCR duplicates 
# 
# samtools rmdup ERR001268_sort.bam ERR001268_sort_rmdup.bam 
# ### for SE experiments, u may use the flag -s



# ===== 4th day ===== #
# =====   SNV   ===== #

### 7) generate raw VCF

mkdir -p $workDir/analysis/vcf
cd $workDir/analysis/vcf

# samtools mpileup -uf $workDir/reference/chr22.fa \
#     $workDir/analysis/bwa/0.6.1/ERR001268_sort_rmdup.bam | \
#     bcftools view -bvcg - > var.raw.bcf
# 
# ## without the -v flag, the bcf will contain information about all bases 
# ## convert the bcf (binary) to vcf
# 
# bcftools view var.raw.bcf > var.unfiltered.vcf
# 
# ### 8) filter the VCF
# vcfutils varFilter -Q15 -d10 var.unfiltered.vcf | \
#     awk '$6 > 30' > var.filtered.vcf 

### 9) identify newly discovered
intersectBed -v -a var.filtered.vcf -b $workDir/reference/dbSNP137.chr22.vcf  > newVar.vcf


###  annotation: convert to annovar format and use \
###  scripts to annotate the vcf
cd $currDir

