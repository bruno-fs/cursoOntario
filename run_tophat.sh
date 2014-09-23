#!/bin/bash
# 
# this bash script will only run tophat.
# check rna-seq.py to see the whole pipeline.
# 
# 
# ### setting up the directory
# 
# RNA_HOME=$HOME/cursoOntario/RNA/rna-seq_tutorial
# RNA_DATA_DIR=$RNA_HOME/data
# TRANS_IDX_DIR=$RNA_HOME/alignments/tophat/trans_idx
# 
# mkdir -p $TRANS_IDX_DIR
# 
# # ### get the data
# # ### index the reference genome
# # 
# # bowtie2-build $RNA_HOME/refs/hg19/bwt/9/9/9.fa
# # 
# ## ==================== ##
# ## ==== run tophat2 === ##
# ## ==================== ##
# 
# cd $RNA_HOME/alignments/tophat 
# 
# tophat2 -p 8 --mate-inner-dist 80 --mate-std-dev 38 \
#     --segment-length 18 --rg-id=normal --rg-sample=normal_N02 \
#     -o normal_N02 -G $RNA_HOME/refs/hg19/genes/genes_chr9.gtf \
#     --transcriptome-index $TRANS_IDX_DIR/ENSG_Genes $RNA_HOME/refs/hg19/bwt/9/9 \
#     $RNA_DATA_DIR/normal_N02_read1.fasta $RNA_DATA_DIR/normal_N02_read2.fasta
# 
# tophat2 -p 8 --mate-inner-dist 80 --mate-std-dev 38 \
#     --segment-length 18 --rg-id=normal --rg-sample=normal_N03 \
#     -o normal_N03 -G $RNA_HOME/refs/hg19/genes/genes_chr9.gtf \
#     --transcriptome-index $TRANS_IDX_DIR/ENSG_Genes $RNA_HOME/refs/hg19/bwt/9/9 \
#     $RNA_DATA_DIR/normal_N03_read1.fasta $RNA_DATA_DIR/normal_N03_read2.fasta
# 
# 
# tophat2 -p 8 --mate-inner-dist 80 --mate-std-dev 38 \
#     --segment-length 18 --rg-id=normal --rg-sample=normal_N06 \
#     -o normal_N06 -G $RNA_HOME/refs/hg19/genes/genes_chr9.gtf \
#     --transcriptome-index $TRANS_IDX_DIR/ENSG_Genes $RNA_HOME/refs/hg19/bwt/9/9 \
#     $RNA_DATA_DIR/normal_N06_read1.fasta $RNA_DATA_DIR/normal_N06_read2.fasta
# 
# 
# tophat2 -p 8 --mate-inner-dist 80 --mate-std-dev 38 \
#     --segment-length 18 --rg-id=carcinoma --rg-sample=carcinoma_C02 \
#     -o carcinoma_C02 -G $RNA_HOME/refs/hg19/genes/genes_chr9.gtf \
#     --transcriptome-index $TRANS_IDX_DIR/ENSG_Genes $RNA_HOME/refs/hg19/bwt/9/9 \
#     $RNA_DATA_DIR/carcinoma_C02_read1.fasta $RNA_DATA_DIR/carcinoma_C02_read1.fasta
# 
# 
# tophat2 -p 8 --mate-inner-dist 80 --mate-std-dev 38 \
#     --segment-length 18 --rg-id=carcinoma --rg-sample=carcinoma_C03 \
#     -o carcinoma_C03 -G $RNA_HOME/refs/hg19/genes/genes_chr9.gtf \
#     --transcriptome-index $TRANS_IDX_DIR/ENSG_Genes $RNA_HOME/refs/hg19/bwt/9/9 \
#     $RNA_DATA_DIR/carcinoma_C03_read1.fasta $RNA_DATA_DIR/carcinoma_C03_read1.fasta
# 
# 
# tophat2 -p 8 --mate-inner-dist 80 --mate-std-dev 38 \
#     --segment-length 18 --rg-id=carcinoma --rg-sample=carcinoma_C06 \
#     -o carcinoma_C06 -G $RNA_HOME/refs/hg19/genes/genes_chr9.gtf \
#     --transcriptome-index $TRANS_IDX_DIR/ENSG_Genes $RNA_HOME/refs/hg19/bwt/9/9 \
#     $RNA_DATA_DIR/carcinoma_C06_read1.fasta $RNA_DATA_DIR/carcinoma_C06_read1.fasta
# 
# 
# ## ==================== ##
# ## ==== cufflinks ===== ##
# ## ==================== ##
# 
# 
# mkdir $RNA_HOME/expression
# cd $RNA_HOME/expression
# 
# ## I decided to continue the pipeline on python
