########################################
# wrapper for rule: plink_association
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

command = "plink --bfile " + str(snakemake.input.bed).replace(".bed","") + " --assoc --out " + str(snakemake.output.association_res).replace(".assoc","") + " >> " + log_filename + " 2>&1 "
f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)

command = "touch plink.test && rm plink.*"
f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)

command = "Rscript "+os.path.abspath(os.path.dirname(__file__))+"/manhattan_plot.R "+\
           snakemake.output.association_res + " " + snakemake.output.manh_plot + " >> " + log_filename + " 2>&1 "

f = open(log_filename, 'a+')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)