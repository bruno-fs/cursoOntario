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


from subprocess import call
from collections import OrderedDict
import sys
import os
import re

def run(command):
    """run a command in bash. for non-zero status, print an error and exit"""
    print >>sys.stderr, "[running]", command
    status = call(command, shell=True)
    if status != 0:
        print >>sys.stderr, "Child was terminated by signal", status
        sys.exit("[error] {}".format(command))
    else:
        print >>sys.stderr, "[DONE] {}".format(command)

### setting up the directories
### EDIT rna_home to match the path/to/your rna-seq_tutorial folder

rna_home = '/work/megs/bruno/single_cell/rna-seq' # <--- EDIT THIS PATH
rna_data_dir = rna_home + '/data'
trans_idx_dir = rna_home + "/alignments/tophat/trans_idx"

run('mkdir -p ' + trans_idx_dir)


### get the data
### index the reference genome

# run(bowtie2-build rna_home/refs/hg19/bwt/9/9/9.fa 9)



samples = OrderedDict()
runs = {}

for line in open('chosen_samples'):
    if not re.match('#', line):
        grupo, sample, run_names = line.split()
        if grupo not in samples:
            samples[grupo] = []
        #else:
        samples[grupo].append(sample)
        runs[sample] = run_names.split(",")


## ==================== ##
## ====== tophat2 ===== ##
## ==================== ##


th_dir = rna_home + "/alignments/tophat"
bwt_dir = rna_home + "/refs/ens77/bwt"

ref_gtf = rna_home + "/refs/ens77/genes/Mus_musculus.GRCm38.77.gtf"
ensg_genes   = trans_idx_dir + "/ENSG_Genes"
bwt_idx = bwt_dir + "/Mus_musculus"
#genome_fasta = rna_home + "/refs/ens77/fasta/Mus_musculus.GRCm38.dna_sm.primary_assembly.fa.gz"
genome_fasta = bwt_idx + ".fa"

# os.chdir(th_dir)
# 
# for group in samples:
#     for sample in samples[group]:
#         reads1 = ",".join([ "{}/{}_1.fastq.gz".format(rna_data_dir, file) for file in runs[sample] ])
#         reads2 = ",".join([ "{}/{}_2.fastq.gz".format(rna_data_dir, file) for file in runs[sample] ])
# 
# 
#         tophat = ("tophat2 -p 16" +
#                 #" --mate-inner-dist 80" +\
#                 #" --mate-std-dev 38" +\
#                 #" --segment-length 18" +\
#                 " --rg-id={0} --rg-sample={1}" +
#                 " -o {1} -G {2}" +
#                 " --transcriptome-index {3} {4}" +
#                 " {5} {6}")
# 
# 
#         tophat = tophat.format(group, sample, ref_gtf, ensg_genes, bwt_idx, reads1, reads2)
#         # format index           0      1        2         3          4        5      6
# 
#         run(tophat)
# 
# ## ==================== ##
# ## ==== cufflinks ===== ##
# ## ==================== ##
# # 
# 
exp_dir = rna_home + "/expression"
# run('mkdir -p ' + exp_dir)
# os.chdir(exp_dir)
# 
# for group in samples:
#     for sample in samples[group]:
# 
#         cufflinks = ("cufflinks -p 16" +
#             " -o {0} --GTF {1}" +
#             " --no-update-check" +
#             " {2}/{0}/accepted_hits.bam")
# 
#         cufflinks = cufflinks.format(sample, ref_gtf, th_dir)
#         ## format index                0        1       2
# 
#         run(cufflinks)
# 
# ## ==================== ##
# ## ==== cuffmerge ===== ##
# ## ==================== ##
# 
# 
# run("find . -name transcripts.gtf > assembly_GTF_list.txt")
# 
# cuffmerge = "cuffmerge -p 8 -o merged -g {} -s {} assembly_GTF_list.txt"
# 
# cuffmerge = cuffmerge.format(ref_gtf, genome_fasta)
# 
# 
# run(cuffmerge)

## ==================== ##
## ===== cuffdiff ===== ##
## ==================== ##


de_dir = rna_home + "/de/reference_only"
run("mkdir -p " + de_dir)

os.chdir(th_dir)

cuffdiff = "cuffdiff -p 8 -L {} -o {} --no-update-check {}/merged/merged.gtf"

labels = ",".join([ group for group in samples ])

cuffdiff = cuffdiff.format(labels, de_dir, exp_dir)

for group in samples:
    cuffdiff += " " + ",".join([ '{}/accepted_hits.bam'.format(sample) for sample in samples[group] ])

run(cuffdiff)


