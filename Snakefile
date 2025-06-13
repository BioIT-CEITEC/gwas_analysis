import os
import pandas as pd
import json
from snakemake.utils import min_version

min_version("5.18.0")
configfile: "config.json"

GLOBAL_TMPD_PATH = config["globalTmpdPath"]

os.makedirs(GLOBAL_TMPD_PATH, exist_ok=True)

##### Config processing #####

sample_tab = pd.DataFrame.from_dict(config["samples"],orient="index")

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
