# SRA_Tinder
*Find hot data sets in your area (of research)!*
![logo](/docs/logo.png)


Have you ever spent weeks working SRA data and then decided it just wasn't going to work? That's like going on a blind date with someone you have no interest in. It's a huge waste of your time!

![Nope](/docs/nope.jpg)

Here we introduct SRA_Tinder, the package that allows you to preview your fastq files before you date them. Go ahead, swipe left. Don't date that ugly data! Or Swipe right and find the love of your data life.
Our goal is to show you only the most essential information about your SRA data sets, and let you decide which ones are right for you.


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


Input is a SRRnumber list from runselector, output is a tab delemted table.

python sra_tinder_matches.py SRA_Acc_list.txt

For example you can test the code using this
### Step 3:
```
$ python sra_tinder_matches.py tests/SRA_Acc_list.txt
```
To get your own SRA_Acc_list.txt go to https://www.ncbi.nlm.nih.gov/Traces/study/ and type in a SRR number or a SRNA project number and click Accession List. 


#streach goals
add the ngs code instead of scraping the web. This means we don't break when SRA changers there webstie, and we could easily take in fastq files instead of SRA accesssions.
graph summerize the output table
add in the search SRA and get a massive accesion list auto lookup




