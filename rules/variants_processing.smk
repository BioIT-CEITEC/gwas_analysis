rule merge_vcfs:
    input:
        vcfs = expand("germline_varcalls/{sample}/haplotypecaller/haplotypecaller.vcf.gz", sample=sample_tab.sample_name)
    output:
        merged_vcfs = "variant_postprocessing/merged.vcf.gz"
    log:
        "logs/merge_vcfs.log"
    conda: "../wrappers/merge_vcfs/env.yaml"
    shell:
        """
        mkdir -p variant_postprocessing
        bcftools merge {input.vcfs} -Oz -o {output.merged_vcfs} >> {log} 2>&1
        tabix -p vcf {output.merged_vcfs} >> {log} 2>&1
        """
rule plink_ped_creation:
    input:
        merged_vcfs = "variant_postprocessing/merged.vcf.gz"
    output:
        ped = "variant_postprocessing/all_samples.ped",
        bim = "variant_postprocessing/all_samples.bim",
        fam = "variant_postprocessing/all_samples.fam"
    log:
        "logs/plink_ped_creation.log"
    conda: "../wrappers/plink_ped_creation/env.yaml"
    shell:
        """
        plink --vcf {input.merged_vcfs} --make-bed --out variant_postprocessing/all_sampless >> {log} 2>&1
        """