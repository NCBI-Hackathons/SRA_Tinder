from Bio import SeqIO
import sys
import glob
import os


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
    total, withadapter, trimmedbases, totalbases = 0, 0, 0, 0
    for record in records:
        len_record = len(record)
        totalbases = totalbases+len_record
        total = total+1
        index = record.seq.find(adaptor[0:min_match])
        if index == -1:
            trimmedbases = trimmedbases+len_record
        else:
            withadapter=withadapter+1
            trimmedbases = trimmedbases+index
    return total, withadapter, totalbases, trimmedbases

def loopadapters(fastqfile):
	l, a, tb, trb = [], [], [], []
	#need to add current path
	for adapterfile in glob.iglob('adapters/*.fa'):
		adapters = SeqIO.parse(adapterfile, "fasta")
		for adapter_record in adapters:
			original_reads = SeqIO.parse(fastqfile, "fastq")
			total_reads, trimmed_reads, totalbases, trimmedbases = trim_adaptors_check(original_reads, str(adapter_record.seq))
			#print (len(trimmed_reads))
			#count = SeqIO.write(trimmed_reads, "trimmed.fastq", "fastq")
			l.append(trimmed_reads)
			a.append(str(adapter_record.seq))
			tb.append(totalbases)
			trb.append(trimmedbases)
			#print (count, str(adapter_record.seq))
	bestadapter = [(count, adapter, totalnts, trimednts) for count, adapter,totalnts, trimednts in zip(l, a, tb, trb) if count==max(l)]
	return bestadapter


def outputtrimedadapterfastqfile(fastqfile, outfastqfile):
	m = loopadapters(fastqfile)
	original_reads = SeqIO.parse(fastqfile, "fastq")
	countreadswithadapter, adapter, totalntsinfastq, trimedntsinfastq = m[0]
	trimmed_reads = trim_adaptors_drop(original_reads, adpater, 0)
	count = SeqIO.write(trimmed_reads, outfastqfile, "fastq")
	

def basesleftaftertriming(fastqfile):
	m = loopadapters(fastqfile)
	countreadswithadapter, adapter, totalntsinfastq, trimedntsinfastq = m[0]	
	return countreadswithadapter, adapter, totalntsinfastq, trimedntsinfastq

if __name__=="__main__":
	fastqfile = sys.argv[1]
	countreadswithadapter, adapter, totalntsinfastq, trimedntsinfastq = basesleftaftertriming(fastqfile)
	print (countreadswithadapter, adapter, totalntsinfastq, trimedntsinfastq)
	#if you want to output a trimmed file run outputtrimedadapterfastqfile
