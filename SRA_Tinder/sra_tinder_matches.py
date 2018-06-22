import sra_tinder 
import trimandcount




def main(SRR_Acc_list):
    f = open(SRR_Acc_list)
    titleline = ["Accession", "mean quality score", "most abundent organism", "percent abundence", "number of organims greater than 1% abundence", "totalreads", "withadapter", "mean_readlen", "std_readlen", "readlen_trimmed", "std_readlen_trimmed"]
    for line in f:
	accession = line.strip("\n")
    	my_tinder = sra_tinder(accession)
        i = my_tinder.scrape_qc()
    	iii = my_tinder.scrape_organisms()
	listofinfo = [accession, str(i), iii[0], iii[1], iii[2]]
	#grab the fastq file
	fastqfile = "temp/"+accession+".fastq"

	totalreads, withadapter, mean_readlen, std_readlen, readlen_trimmed, std_readlen_trimmed = basesleftaftertriming(fastqfile)
	#remove the fastqfile
	#print('\t'.join([accession, str(i), iii[0], iii[1], iii[2]]))
