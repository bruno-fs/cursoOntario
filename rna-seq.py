#!/usr/bin/env python2
#
# Dependencies: bowtie2, tophat2, cufflinks2 and rna-seq_tutorial folder (check the README for links)
# Feel free to clone and edit this script to match your needs ;)
#
# ToDo: add arguments to control whether run the pipeline or print the commands

__author__ = "Bruno Souza"
__credits__ = ["Fouad Yousif", "bioinformatics.ca"]
__maintainer__ = "Bruno Souza"
__email__ = "fsouza dot bruno at usp dot br"


import os
from collections import OrderedDict

### setting up the directories
### EDIT rna_home to match the path/to/your rna-seq_tutorial folder

rna_home = '/home/bruno/cursoOntario/RNA/rna-seq_tutorial' # <--- EDIT THIS PATH
rna_data_dir = rna_home + "/data"
trans_idx_dir = rna_home + "/alignments/tophat/trans_idx"

os.system('mkdir -p '+ trans_idx_dir)

### get the data
### index the reference genome

# os.system(bowtie2-build rna_home/refs/hg19/bwt/9/9/9.fa 9)



samples = OrderedDict()
runs = {}

for line in open('chosen_samples'):
    grupo, sample, run_names = line.split()
    if grupo not in samples: 
        samples[grupo] = []
    else:
        samples[grupo].append(sample)
        runs[sample] = run_names.split(",")


## ==================== ##
## ====== tophat2 ===== ##
## ==================== ##


th_dir = rna_home + "/alignments/tophat"
bwt_dir = rna_home + "/refs/hg19/bwt/9"

ref_gtf = rna_home + "/refs/hg19/genes/genes_chr9.gtf"
ensg_genes   = trans_idx_dir + "/ENSG_Genes"
bwt_idx = bwt_dir + "/9"
genome_fasta = rna_home + "/refs/hg19/fasta/9/9.fa"

os.chdir(th_dir)





for group in samples:
    for sample in samples[group]:
        reads1 = ",".join([ "{}/{}_1.fastq.gz".format("fastq_folder", file) for file in runs[sample] ])
        reads2 = ",".join([ "{}/{}_2.fastq.gz".format("fastq_folder", file) for file in runs[sample] ])
       

        tophat = ("tophat2 -p 8" +
                #" --mate-inner-dist 80" +\
                #" --mate-std-dev 38" +\
                #" --segment-length 18" +\
                " --rg-id={0} --rg-sample={1}" +
                " -o {1} -G {2}" +
                " --transcriptome-index {3} {4}" +
                " {5} {6}" )

     
        tophat = tophat.format(group, sample, ref_gtf, ensg_genes, bwt_idx, reads1, reads2)
        # format index           0      1        2         3          4        5      6

        print("[running] " + tophat)
        os.system(tophat)

## ==================== ##
## ==== cufflinks ===== ##
## ==================== ##


exp_dir = rna_home + "/expression"
os.system('mkdir -p ' + exp_dir)
os.chdir(exp_dir)

for group in samples:
    for sample in samples[group]:

        cufflinks = ("cufflinks -p 8" +
            " -o {0} --GTF {1}" +
            " --no-update-check" +
            " {2}/{0}/accepted_hits.bam")

        cufflinks = cufflinks.format(sample, ref_gtf, th_dir)
        ## format index                0        1       2

        print("[running] " + cufflinks)
        os.system(cufflinks)

## ==================== ##
## ==== cuffmerge ===== ##
## ==================== ##


os.system("find . -name transcripts.gtf > assembly_GTF_list.txt")

cuffmerge = "cuffmerge -p 8 -o merged -g {} -s {} assembly_GTF_list.txt"

cuffmerge = cuffmerge.format(ref_gtf, genome_fasta)


print("[running] " + cuffmerge)
os.system(cuffmerge)

## ==================== ##
## ===== cuffdiff ===== ##
## ==================== ##


de_dir = rna_home + "/de/reference_only"
os.system("mkdir -p " + de_dir)

os.chdir(th_dir)

cuffdiff = "cuffdiff -p 8 -L {} -o {} --no-update-check {}/merged/merged.gtf"

labels = ",".join([ group for group in samples ])

cuffdiff = cuffdiff.format(labels, de_dir, exp_dir)

for group in samples:
    cuffdiff += " " + ",".join([ '{}/accepted_hits.bam'.format(sample) for sample in samples[group] ])

print("[running] " + cuffdiff)
os.system(cuffdiff)


