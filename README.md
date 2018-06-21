# EZData

A package to onboard data from disparate datasets into common pipelines without file transfer

## Installation
Installation is a three step process:
### Step 1:
```
# Clone the repo
$ git clone https://github.com/NCBI-Hackathons/EZData
```
### Step 2:
```
# Install the included SRA SDK
$ cd deps/ngs-sdk.2.9.0-linux/ngs-python
$ python setup.py install
```
### Step 3:
```
# move back to base directory
$ cd ../../..
$ python setup.py install
```


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
