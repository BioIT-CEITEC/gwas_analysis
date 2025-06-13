########################################
# wrapper for rule: plink_preprocessing
########################################
import re
import subprocess
from snakemake.shell import shell
shell.executable("/bin/bash")
log_filename = str(snakemake.log)

data = snakemake.params.config

with open(snakemake.output.sex_file, 'w') as sex_file, open(snakemake.output.phenotype, 'w') as pheno_file:
    for sample_id, sample_data in data['samples'].items():
        sample_name = sample_data['sample_name']
        sex = sample_data['sex']
        phenotype = sample_data['phenotype']
        
        sex_file.write(f"{sample_name} {sample_name} {sex}\n")
        pheno_file.write(f"{sample_name} {sample_name} {phenotype}\n")

f = open(log_filename, 'wt')
f.write("\n##\n## RULE: plink preprocessing \n##\n")
f.close()

version = str(subprocess.Popen("conda list ", shell=True, stdout=subprocess.PIPE).communicate()[0], 'utf-8')
f = open(log_filename, 'at')
f.write("## CONDA: "+version+"\n")
f.close()

command = "plink --vcf " + snakemake.input.merged_vcfs + " --split-x b37 'no-fail' --update-sex " + snakemake.output.sex_file + " --set-missing-var-ids @:#[b37]\\$1,\\$2 --make-bed --out " + str(snakemake.output.tmp_bed).replace(".bed","") + "  >> " + log_filename + " 2>&1"
f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)

command = "plink --bfile " + str(snakemake.output.tmp_bed).replace(".bed","") + " --pheno " + snakemake.output.phenotype + " --make-bed --out " + str(snakemake.output.bed).replace(".bed","") + " >> " + log_filename + " 2>&1 "
f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)

command = "plink --bfile " + str(snakemake.output.bed).replace(".bed","") + " --geno " + str(snakemake.params.geno_threshold) + " --make-bed --out " + str(snakemake.output.geno_filt).replace(".bed","") + " >> " + log_filename + " 2>&1"
f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)

command = "plink --bfile " + str(snakemake.output.geno_filt).replace(".bed","") + " --mind " + str(snakemake.params.mind_threshold) + " --make-bed --out " + str(snakemake.output.miss_filt).replace(".bed","") + " >> " + log_filename + " 2>&1"
f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)

#command = "plink --bfile " + str(snakemake.output.miss_filt).replace(".bed","") + " --check-sex " + str(snakemake.params.max_female) + " " + str(snakemake.params.min_male) + " >> " + log_filename + " 2>&1 "
#f = open(log_filename, 'at')
#f.write("## COMMAND: "+command+"\n")
#f.close()
#shell(command)
