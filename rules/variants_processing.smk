rule create_tbi_index:
    input:
        vcf = "/germline_varcalls/{sample}.g.vcf.gz"
    output:
        tbi = "/germline_varcalls/{sample}.g.vcf.gz.tbi"
    log:
        "logs/{sample}/create_tbi_index.log"
    threads: 10
    conda: "../wrappers/merge_vcfs/env.yaml"
    shell:
        """
        tabix -p vcf {input.vcf} >> {log} 2>&1
        """

rule merge_vcfs:
    input:
        vcfs = expand("/germline_varcalls/{sample}.g.vcf.gz", sample=sample_tab.sample_name),
        tbi = expand("/germline_varcalls/{sample}.g.vcf.gz.tbi", sample=sample_tab.sample_name)
    output:
        merged_vcfs = "variant_postprocessing/merged_variants.g.vcf.gz",
        annotated_vcfs = "variant_postprocessing/merged_annotated_variants.g.vcf.gz"
    log:
        "logs/merge_vcfs.log"
    threads: 10
    conda: "../wrappers/merge_vcfs/env.yaml"
    shell:
        """
        mkdir -p variant_postprocessing
        bcftools merge {input.vcfs} --threads {threads} -Oz -o {output.merged_vcfs} >> {log} 2>&1
        bcftools annotate --set-id '%CHROM\_%POS\_%REF\_%ALT' -O z -o {output.annotated_vcfs} {output.merged_vcfs}
        tabix -p vcf {output.merged_vcfs} >> {log} 2>&1
        """

rule plink_ped_creation:
    input:
        merged_vcfs = "variant_postprocessing/merged_annotated_variants.g.vcf.gz"
    output:
        tmp_bed = "variant_postprocessing/temp/all_samples_tmp.bed",
        bed = "variant_postprocessing/temp/all_samples.bed",
        geno_filt = "variant_postprocessing/temp/all_samples_geno_filt.bed",
        miss_filt = "variant_postprocessing/temp/all_samples_miss_filt.bed",
        sex_file = "variant_postprocessing/sex_information.txt",
        phenotype = "variant_postprocessing/pheno_information.txt"
    log:
        "logs/plink_ped_creation.log"
    params:
        geno_threshold = config["plink_geno_threshold"],
        mind_threshold = config["plink_mind_threshold"],
        max_female = config["plink_max_female"],
        min_male = config["plink_min_male"],
        config = config
    conda: "../wrappers/plink/env.yaml"
    script: "../wrappers/plink/ped_creation.py"

rule plink_qc_control:
    input:
        bed = "variant_postprocessing/temp/all_samples_miss_filt.bed"
    output:
        imp_sex = "variant_postprocessing/temp/all_samples_imputed_sex.bed",
        ext = "variant_postprocessing/temp/all_samples_autosomal.bed",
        freq = "variant_postprocessing/temp/all_samples_freq.frq",
        filtered = "variant_postprocessing/temp/all_samples_filt_freq.bed",
        hw_f1 = "variant_postprocessing/temp/all_samples_hw_f1.bed",
        hw_filtered = "variant_postprocessing/temp/all_samples_fw_filtered.bed",
        text = "variant_postprocessing/temp/autosomal_chromosomes_only.txt",
        prunesnp = "variant_postprocessing/indepSNP.prune.in",
        pruned = "variant_postprocessing/all_samples_pruned.het",
        founders_filt = "variant_postprocessing/final_founders_filtered.bed",
        founders_txt = "variant_postprocessing/final_founders_effect.genome",
        founders_mds = "variant_postprocessing/final_founders_filtered_mds.mds"
    log:
        "logs/plink_qc_control.log"
    params:
        maf = config["plink_maf"],
        max_female = config["plink_max_female"],
        min_male = config["plink_min_male"]
    conda: "../wrappers/plink/env.yaml"
    script: "../wrappers/plink/qc_ctrl.py"

rule association_studies:
  input:
    bed = "variant_postprocessing/final_founders_filtered.bed"
  output:
    association_res = "association_results/association_results.assoc",
    manh_plot = "association_results/manhattan_plot.pdf"
  log: "logs/association_analysis.log"
  conda: "../wrappers/plink/env.yaml"
  script: "../wrappers/plink/association.py"
