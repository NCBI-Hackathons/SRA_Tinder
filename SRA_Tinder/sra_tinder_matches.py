import sra_tinder 
import trimandcount
import subprocess
import sys
import pandas



def main(SRR_Acc_list, outfile):
    f = open(SRR_Acc_list)
    allinfo = []
    titleline = ["Accession", "mean quality score", "most abundent organism", "percent abundence", "number of organims greater than 1% abundence", "totalreads", "withadapter", "mean_readlen", "std_readlen", "readlen_trimmed", "std_readlen_trimmed"]
    for line in f:
	accession = line.strip("\n")
    	my_tinder = sra_tinder(accession)
        i = my_tinder.scrape_qc()
    	iii = my_tinder.scrape_organisms()
	fastqfile = "temp/"+accession+".fastq"
	totalreads, withadapter, mean_readlen, std_readlen, readlen_trimmed, std_readlen_trimmed = basesleftaftertriming(fastqfile)
	listofinfo = [accession, str(i), iii[0], iii[1], iii[2], totalreads, withadapter, mean_readlen, std_readlen, readlen_trimmed, std_readlen_trimmed]
    df = pandas.DataFrame.from_records(allinfo, columns=titleline)
    df.to_csv(outfile)
