########################################
# wrapper for rule: plink_qc_control
########################################
import re
import os
import subprocess
from snakemake.shell import shell
shell.executable("/bin/bash")
log_filename = str(snakemake.log)

f = open(log_filename, 'wt')
f.write("\n##\n## RULE: plink preprocessing \n##\n")
f.close()

version = str(subprocess.Popen("conda list ", shell=True, stdout=subprocess.PIPE).communicate()[0], 'utf-8')
f = open(log_filename, 'at')
f.write("## CONDA: "+version+"\n")
f.close()

command = "plink --bfile " + str(snakemake.input.bed).replace(".bed","") + " --impute-sex " + str(snakemake.params.max_female) + " " + str(snakemake.params.min_male) + " --make-bed --out " + str(snakemake.output.imp_sex).replace(".bed","") + " >> " + log_filename + " 2>&1 " 
f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)

command = "awk '{{ if ($1 >= 1 && $1 <= 22 ) print $2 }}' " + str(snakemake.input.bed).replace("bed","bim") + " > " + snakemake.output.text + " 2>> " + log_filename + " 2>&1"
f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)

command = "plink --bfile " + str(snakemake.output.imp_sex).replace(".bed","") + " --extract " + snakemake.output.text + " --make-bed --out " + str(snakemake.output.ext).replace(".bed","") + " >> " + log_filename + " 2>&1 "
f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)

command = "plink -bfile " + str(snakemake.output.ext).replace(".bed","") + " --freq --out " + str(snakemake.output.freq).replace(".frq","") + " >> " + log_filename + " 2>&1 "
f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)

command = "plink --bfile " + str(snakemake.output.ext).replace(".bed","") + " --maf " + str(snakemake.params.maf) + " --make-bed --out " + str(snakemake.output.filtered).replace(".bed","") + " >> " + log_filename + " 2>&1 "
f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)

command = "plink --bfile " + str(snakemake.output.filtered).replace(".bed","") + " --hardy  >> " + log_filename + " 2>&1 "
f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)

command = "plink --bfile " + str(snakemake.output.filtered).replace(".bed","") + " --hwe 1e-6 --make-bed --out " + str(snakemake.output.hw_f1).replace(".bed","")+ " >> " + log_filename + " 2>&1 "
f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)

command = "plink --bfile " + str(snakemake.output.hw_f1).replace(".bed","") + " --hwe 1e-10 --make-bed --out " + str(snakemake.output.hw_filtered).replace(".bed","")+ " >> " + log_filename + " 2>&1 "
f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)

command = "plink --bfile "+ str(snakemake.output.hw_filtered).replace(".bed","")+" --indep-pairwise 50 5 0.2 --out " + str(snakemake.output.prunesnp).replace(".prune.in","") + " >> " + log_filename + " 2>&1 "
f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)

command = "plink --bfile " + str(snakemake.output.hw_filtered).replace(".bed","") + " --extract " + snakemake.output.prunesnp + " --het --out " + str(snakemake.output.pruned).replace(".het","") + " >> " + log_filename + " 2>&1 "
f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)

command = "plink --bfile " + str(snakemake.output.hw_filtered).replace(".bed","") + " --filter-founders --make-bed --out " + str(snakemake.output.founders_filt).replace(".bed","")+ " >> " + log_filename + " 2>&1 "
f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)

command = "plink --bfile " + str(snakemake.output.founders_filt).replace(".bed","") + " --extract " + snakemake.output.prunesnp + " --genome --min 0.2 --out " + str(snakemake.output.founders_txt).replace(".genome","") + " >> " + log_filename + " 2>&1 " 
f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)

command = "plink --bfile " + str(snakemake.output.founders_filt).replace(".bed","") + " --read-genome " + str(snakemake.output.founders_txt) + " --cluster --mds-plot 10 --out " +  str(snakemake.output.founders_mds).replace(".mds","") + " >> " + log_filename + " 2>&1 "
f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)

command = "awk '{{print$1, $2, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13}}' " + str(snakemake.output.founders_mds) + " > " + snakemake.output.founders_covar + " >> " + log_filename + " 2>&1 "
f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)