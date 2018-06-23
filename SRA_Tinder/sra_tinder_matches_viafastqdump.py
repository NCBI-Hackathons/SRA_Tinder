import os
import sra_tinder 
import trimandcount
import subprocess
import sys
import pandas

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def main(SRR_Acc_list, outfile):
    f = open(SRR_Acc_list)
    allinfo = []
    titleline = [
        "Accession", "mean_quality_score", "most_abundent_organism",
        "percent_abundence", "number_of_organims_greater_than_1%_abundence",
        "total_reads_checked", "total_reads_withadapter", "mean_readlen_before_trim", "std_readlen_before_trim",
        "mean_readlen_of_trimmed_reads", "std_readlen_of_trimmed_reads"
    ]
    for line in f:
        accession = line.strip("\n")
        my_tinder = sra_tinder.sra_tinder_web(accession)
        i = my_tinder.scrape_qc()
        iii = my_tinder.scrape_organisms()
	#grab the fastq file
        dowloadfastq = envokefastqdump(accession) 
        fastqfile = "temp/"+accession+".fastq"	
        totalreads, withadapter, mean_readlen, std_readlen, readlen_trimmed, std_readlen_trimmed = trimandcount.basesleftaftertrimingonefastq(fastqfile)
        listofinfo = [accession, str(i), iii[0], iii[1], iii[2], totalreads, withadapter, mean_readlen, std_readlen, readlen_trimmed, std_readlen_trimmed]
        print (listofinfo)
        allinfo.append(listofinfo)
    df = pandas.DataFrame.from_records(allinfo, columns=titleline)
    df.to_csv(outfile)
    print (df)
        #remove the fastqfile
        #print('\t'.join([accession, str(i), iii[0], iii[1], iii[2]]))



def envokefastqdump(accession):
	#-N 10000 -X 110000 
	#fastq-dump -X 10000 -Z 20000 --outdir test/ --skip-technical --readids  --dumpbase --clip SRR3403834
	subprocess.call(['fastq-dump',"-N", "10000", "-X", "11000", "--outdir", "temp/", "--skip-technical", "--dumpbase", accession])

if __name__=="__main__":
	SRR_Acc_list = sys.argv[1]
	outfile = sys.argv[2]
	main(SRR_Acc_list, outfile)
