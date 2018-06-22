from Bio import SeqIO
import numpy 
import sys
import glob
import os

#pip install biopython
#pip install numpy

def trim_adaptors_drop(records, adaptor, min_len):
    """Trims perfect adaptor sequences, checks read length.

    This is a generator function, the records argument should
    be a list or iterator returning SeqRecord objects.
    """
    len_adaptor = len(adaptor) #cache this for later
    for record in records:
        len_record = len(record) #cache this for later
        if len(record) < min_len:
           #Too short to keep
           continue
        index = record.seq.find(adaptor)
        if index == -1:
            #adaptor not found, so won't trim
            yield record
        elif len_record - index - len_adaptor >= min_len:
            #after trimming this will still be long enough
            yield record[index+len_adaptor:]


def trim_adaptors_check(records, adaptor, min_match=6):
    """Trims perfect adaptor sequences.

    This is a generator function, the records argument should
    be a list or iterator returning SeqRecord objects.
    http://biopython.org/DIST/docs/tutorial/Tutorial.html#htoc289
    """
    len_adaptor = len(adaptor) #cache this for later
    withadapter  = 0
    trimmedbases, totalbases = [], []
    for record in records:
        print (record)
        len_record = len(record)
        totalbases.append(len_record)
        index = record.seq.find(adaptor[0:min_match])
        if not index == -1:
            withadapter=withadapter+1
            trimmedbases.append(index)
    mean_readlen = numpy.mean(totalbases) 
    std_readlen = numpy.std(totalbases)
    readlen_trimmed = numpy.mean(trimmedbases)
    std_readlen_trimmed =numpy.std(trimmedbases)
    totalreads = len(totalbases)
    return totalreads, withadapter, mean_readlen, std_readlen, readlen_trimmed, std_readlen_trimmed

def loopadapters(fastqfile):
	alladapters, readswithadapters = [], []
	#need to add current path
	for adapterfile in glob.iglob('adapters/*.fa'):
		adapters = SeqIO.parse(adapterfile, "fasta")
		for adapter_record in adapters:
			original_reads = SeqIO.parse(fastqfile, "fastq")
			totalreads, withadapter, mean_readlen, std_readlen, readlen_trimmed, std_readlen_trimmed = trim_adaptors_check(original_reads, str(adapter_record.seq))
			#print (len(trimmed_reads))
			#count = SeqIO.write(trimmed_reads, "trimmed.fastq", "fastq")
			readswithadapters.append(withadapter)
			alladapters.append([totalreads, withadapter, mean_readlen, std_readlen, readlen_trimmed, std_readlen_trimmed])
			#print (count, str(adapter_record.seq))
	bestadapters = [(totalreads,withadapter, mean_readlen, std_readlen, readlen_trimmed, std_readlen_trimmed) for totalreads, withadapter, mean_readlen, std_readlen, readlen_trimmed, std_readlen_trimmed in alladapters if withadapter==max(readswithadapters)] 
	return bestadapters


def outputtrimedadapterfastqfile(fastqfile, outfastqfile, adpater):
	original_reads = SeqIO.parse(fastqfile, "fastq")
	trimmed_reads = trim_adaptors_drop(original_reads, adpater, 0)
	#if you want to write the trimed reads used this
	#count = SeqIO.write(trimmed_reads, outfastqfile, "fastq")
	return trimmed_reads

def basesleftaftertriming(fastqfile):
    with open(fastqfile) as IN:
        i = 0
        for line in IN:
            i+=1
        print(i)
    return
    m = loopadapters(fastqfile)
    print(m)
    totalreads, withadapter, mean_readlen, std_readlen, readlen_trimmed, std_readlen_trimmed = m[0]	
    return totalreads, withadapter, mean_readlen, std_readlen, readlen_trimmed, std_readlen_trimmed

if __name__=="__main__":
	fastqfile = sys.argv[1]
	totalreads, withadapter, mean_readlen, std_readlen, readlen_trimmed, std_readlen_trimmed = basesleftaftertriming(fastqfile)
	print ("totalreads", "withadapter", "mean_readlen", "std_readlen", "readlen_trimmed", "std_readlen_trimmed")
	print (totalreads, withadapter, mean_readlen, std_readlen, readlen_trimmed, std_readlen_trimmed)
	#if you want to output a trimmed file run outputtrimedadapterfastqfile
