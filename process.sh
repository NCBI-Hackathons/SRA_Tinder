fastq-dump --split-files --defline-seq '@$ac.$si.$sg/$ri' --defline-qual '+' -Z $1 | tee $1.fq | python readfq.py
fastqc $1.fq

