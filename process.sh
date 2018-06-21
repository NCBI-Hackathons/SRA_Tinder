#!/usr/bin/env bash

NREADS=${2:-4000}

fastq-dump --split-files --defline-seq '@$ac.$si.$sg/$ri' --defline-qual '+' -Z $1 | head -n $NREADS > $1.fq

#cat $1 > python readfq.py
fastqc $1.fq

qual=$(bioawk -c fastx '{ print ">"$name; print meanqual($qual) }' $1.fq|grep -v ">"|awk '{s+=$1}END{print "",s/NR}' RS=" ")
echo $1 $'\t' $qual  >> table.txt

