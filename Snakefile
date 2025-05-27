import os
import pandas as pd
import json
from snakemake.utils import min_version

min_version("5.18.0")
configfile: "config.json"

GLOBAL_REF_PATH = config["globalResources"]
GLOBAL_TMPD_PATH = config["globalTmpdPath"]

os.makedirs(GLOBAL_TMPD_PATH, exist_ok=True)

##### BioRoot utilities #####
module BR:
    snakefile: github("BioIT-CEITEC/bioroots_utilities", path="bioroots_utilities.smk",branch="master")
    config: config

use rule * from BR as other_*

##### Config processing #####

sample_tab = BR.load_sample()

config = BR.load_organism()

if not "format" in config:
    config["format"] = "default"
if not "not_use_merged" in config:
    config["not_use_merged"] = False
if not "min_variant_frequency" in config:
    config["min_variant_frequency"] = 0


wildcard_constraints:
    sample = "|".join(sample_tab.sample_name),


##### Target rules #####
rule all:
    input:"variant_postprocessing/final_founders_filtered.bed",
          "association_results/association_results.assoc"

##### Modules #####

include: "rules/variants_processing.smk"