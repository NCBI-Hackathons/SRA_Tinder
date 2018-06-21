# EZData

A package to onboard data from disparate datasets into common pipelines without file transfer


## Example usage

    ./process.sh ERR612477


Example usage for bulk processing


    while read i; do ./process.sh  $i; done < SraAccessionsTest.txt > table.txt

This will then create the bulk processing of the first 1000 reads of all runs listed in SraAccessionsTest.txt and output summary stats to table.txt of mean base quality score over all bases


## Note

Uses readfq.py from https://github.com/lh3/readfq

## Prerequisites

Install sra-toolkit and make sure fastq-dump is in your $PATH https://github.com/ncbi/sra-tools

Also install fastqc to the command line (if you have homebrew, use `brew install fastqc`)
