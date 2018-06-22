# SRA_Tinder
![logo](/docs/logo.png)

Get a constant stream of high quality reads from the SRA matched just for you!

Have you ever been on SRA, downloaded data and then decided it just wasn't going to work? That's like going on a blind date with someone you have no interest in. Its a huge waste of your time! 

![Nope](/docs/nope.jpg)

Here we introduct SRA_tinder, the package that allows you to preview your fastq files before you date them. Go ahead, swipe left. Don't date that ugly data! Or Swipe right and find the love of your data life. 


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

python sra_tinder_matches.py tests/SRA_Acc_list.txt

To get the SRA_Acc_list.txt
GO to https://www.ncbi.nlm.nih.gov/Traces/study/ and type in a SRR number or a project number. 

#streach goals
add the ngs code instead of scraping the web
graph summerize the output table



