fastq-dump --split-files --defline-seq '@$ac.$si.$sg/$ri' --defline-qual '+' -Z $1 | tee $1.fq | python readfq.py
fastqc $1.fq

bioawk -c fastx '{ print ">"$name; print meanqual($qual) }' $1.fq|grep -v ">"|awk '{s+=$1}END{print "ave:",s/NR}' RS=" " > $1.meanqual

