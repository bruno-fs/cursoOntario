#!/usr/bin/python2
# fouad.yousif@oicr.on.ca fouad.makadsi@gmail.com
#
# edit the RNA_HOME path to match yours
# uncomment the os.system commands in order to run
#
#
# ToDo: add arguments to control whether run the pipeline or
# print the commands


import os

### setting up the directories

RNA_HOME = '/home/bruno/cursoOntario/RNA/rna-seq_tutorial'
RNA_DATA_DIR = RNA_HOME + "/data"
TRANS_IDX_DIR = RNA_HOME + "/alignments/tophat/trans_idx"

os.system('mkdir -p '+ TRANS_IDX_DIR)

# ### get the data
# ### index the reference genome
#
# # bowtie2-build $RNA_HOME/refs/hg19/bwt/9/9/9.fa

## ==================== ##
## ====== tophat2 ===== ##
## ==================== ##


th_dir = RNA_HOME + "/alignments/tophat"
ref_gtf = RNA_HOME + "/refs/hg19/genes/genes_chr9.gtf"
ensg_genes   = TRANS_IDX_DIR + "/ENSG_Genes"
bowtie_index = RNA_HOME + "/refs/hg19/bwt/9/9"

os.chdir(th_dir)

samples = { 'normal'    : ['_N02', '_N03', '_N06'],
            'carcinoma' : ['_C02', '_C03', '_C06'] }

for group in samples:
    for sample in samples[group]:
        tophat = "tophat2 -p 8" +\
            " --mate-inner-dist 80" +\
            " --mate-std-dev 38" +\
            " --segment-length 18" +\
            " --rg-id={0} --rg-sample={0}{1}" +\
            " -o {0}{1} -G {2}" +\
            " --transcriptome-index {3} " +\
            "{4}/{0}{1}_read1.fasta {4}/{0}{1}_read2.fasta"

        tophat = tophat.format(group, sample, ref_gtf, ensg_genes, RNA_DATA_DIR)

        # os.system(tophat)
        print(tophat)



## ==================== ##
## ==== cufflinks ===== ##
## ==================== ##


exp_dir = RNA_HOME + "/expression"
os.system('mkdir -p ' + exp_dir)
os.chdir(exp_dir)

for group in samples:
    for sample in samples[group]:

        cufflinks = "cufflinks -p 8 -o " + \
            group + sample + " --GTF " + \
            ref_gtf + " --no-update-check " + \
            th_dir + "/" + group + sample + "/accepted_hits.bam"

        # os.system(cufflinks)
        print(cufflinks)





## ==================== ##
## ==== cuffmerge ===== ##
## ==================== ##


os.system("ls -l " + exp_dir + "/*/transcripts.gtf | cut -f9 -d' ' > " + exp_dir + "/assembly_GTF_list.txt")

cuffmerge = "cuffmerge -p 8 -o " + exp_dir + \
    "/merged -g " + RNA_HOME + \
    "/refs/hg19/genes/genes_chr9.gtf -s " \
    + RNA_HOME + "/refs/hg19/bwt/9/ " \
    + exp_dir + "/assembly_GTF_list.txt"

# os.system(cuffmerge)
print(cuffmerge)

## ==================== ##
## ===== cuffdiff ===== ##
## ==================== ##


de_dir = RNA_HOME + "/de/reference_only"
os.system("mkdir -p " + de_dir)

os.chdir(th_dir)

cuffdiff = "cuffdiff -p 8 -L {} -o {} --no-update-check {}/merged/merged.gtf"

labels = ",".join([ group.capitalize() for group in samples ])

cuffdiff = cuffdiff.format(labels, de_dir, exp_dir)

accepted_hits  = ' {}/accepted_hits.bam'

for group in samples:
    for sample in samples[group]:
        cuffdiff += accepted_hits.format(group + sample)

# os.system(cuffdiff)
print(cuffdiff)

