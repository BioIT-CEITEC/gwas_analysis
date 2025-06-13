library(qqman)

manhattan_plot <- function(args) {
  assoc_file <- args[1]
  manhattan_plot <- args[2]
  
  results_as <- read.table(assoc_file, head = TRUE)
  
  pdf(file = manhattan_plot, width = 20, height = 14)
  
  manhattan(results_as, chr="CHR", bp="BP", p="P", snp="SNP",
            main="Manhattan plot",
            ylim = c(0, 12)
            )
  dev.off()
  
}

#run as Rscript
args <- commandArgs(trailingOnly = TRUE)
manhattan_plot(args)