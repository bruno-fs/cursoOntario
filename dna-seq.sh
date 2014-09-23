#!/bin/bash
#
# script based on DNA-seq classes from "Introduction to Bioinformatics", 
# presented by Paul Boultros, Fouad and Julie 
#
# this script assumes your NGS_lab folder has the following structure:
# 
# NGS_lab
# ├── analysis
# │   ├── bwa
# │   │   └── 0.6.2
# │   └── snv
# ├── fastq
# │   ├── ERR001268_1.filt.fastq.gz
# │   └── ERR001268_2.filt.fastq.gz
# └── reference
#     ├── bwa
#     │    └── 0.6.2
#     │           └── chr22.fa -> ../../chr22.fa
#     ├── chr22.fa
#     └── dbSNP137.chr22.vcf

 
# =================== #
# ===== 3rd day ===== #
# ===== DNA-seq ===== #
# =================== #


workDir=$HOME/cursoOntario/NGS_lab
cd $workDir/analysis/bwa/0.6.2

### 1) index the reference fasta

bwa index $workDir/reference/bwa/0.6.2/chr22.fa

### 2) align the reads


for x in 1 2; do
    bwa aln -t 15 reference/bwa/0.6.2/chr22.fa \
        fastq/ERR001268_$x.filt.fastq.gz \
        > ERR001268_$x.sai
done

### 3) combine both reads in a single SAM

bwa sampe \
    -r "@RG\tID:ER001268\tSM:Sample1\tLB:library1\tPL:Illumina\tPU:NONE" \
    reference/bwa/0.6.2/chr22.fa \
    ERR001268_1.sai ERR001268_2.sai \
    fastq/ERR001268_1.filt.fastq.gz \
    fastq/ERR001268_2.filt.fastq.gz \
    > ERR001268.sam

### 4) SAM 2 BAM

samtools view -Sbo ERR001268.bam ERR001268.sam
echo "[tip] check your bam with samtools view -h" 1>&2
echo "[tip] if it is ok, u may delete the sam file and save space" 1>&2

### 5) Sorted BAM

samtools sort ERR001268.bam ERR001268_sort 


### 6) Remove PCR duplicates 

samtools rmdup ERR001268_sort.bam ERR001268_sort_rmdup.bam 

### for SE experiments, u may use the flag -s


# =================== #
# ===== 4th day ===== #
# =====   SNV   ===== #
# =================== #

### 7) generate raw VCF

cd $workDir/analysis/snv

samtools mpileup -uf $workDir/reference/chr22.fa \
     $workDir/analysis/bwa/0.6.1/ERR001268_sort_rmdup.bam | \
     bcftools view -bvcg - > var.raw.bcf
 
 ## without the -v flag, the bcf will contain information about all bases 
 ## convert the bcf (binary) to vcf
 
bcftools view var.raw.bcf > var.unfiltered.vcf
 
### 8) filter the VCF
vcfutils varFilter -Q15 -d10 var.unfiltered.vcf | \
     awk '$6 > 30' > var.filtered.vcf 

### 9) identify newly discovered variants
intersectBed -v -a var.filtered.vcf -b $workDir/reference/dbSNP137.chr22.vcf  > newVar.vcf


###  annotation: convert to annovar format and use \
###  scripts to annotate the vcf

