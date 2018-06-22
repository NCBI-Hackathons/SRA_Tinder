import sys
import os
import argparse
import urllib.request as ur
import re

VERSION = 1.0


class sra_tinder:


    def __init__(self, sra_file_name):
        self.sra_file_name = sra_file_name

    def scrape_organisms(self):
        """
        Scrapes the taxonomic information for a run accession.
        :return: a list representing [most_abundant_organism, its_%_abundance, #_organisms_>_1%_abundance]
        """
        url = "https://trace.ncbi.nlm.nih.gov/Traces/sra/?run={}".format(self.sra_file_name)
        string = ur.urlopen(url).read().decode()
        output = []
        count_organisms = 0
        table = str(re.findall("<h3>Strong signals<\/h3>.*?<\/table>", string, re.DOTALL))
        rows = re.findall("<tr>.*?<\/tr>", table, re.DOTALL)
        for row in rows:
            values = re.findall("<tdstyle=\"padding:.*?\">(.*?)<\/td>", str(row.replace('\n', '').replace(' ', '')),
                                re.DOTALL)
            if len(values) < 4:
                # print("Error: {}".format(values))
                continue
            count_organisms += 1
            if len(output) == 0 or float(values[3]) > output[1]:
                output += [values[1], float(values[3])]
        output += [count_organisms]
        return [str(x) for x in output]


    def scrape_qc(self):
        """
        Scrapes the URL metadata page for the run accession
        :return: a float rounded to two decimal places representing the average quality score of a SRA run
        """
        url = "https://trace.ncbi.nlm.nih.gov/Traces/sra/?run={}".format(self.sra_file_name)
        string = ur.urlopen(url).read().decode()
        table = re.findall('<table class="zebra run-metatable">.*?<div class="center">Phred quality score<\/div>', string, re.DOTALL)
        table = str(table)
        entries = re.findall('<span title="(.*?) : (.*?)" style=', table, re.DOTALL)
        d = {}
        for score in entries:
            d[int(score[0])] = int(score[1].replace(',', ''))
        total = 0
        count = 0
        for k, v in d.items():
            total += k * v
            count += v
        return round(total/count, 2)

#testing cases, please ignore
# x = sra_tinder('SRR3403834').scrape_organisms()
# print(x)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='Input File', required=True)
    parser.add_argument('-n', help='Some Number', type=int)
    parser.add_argument('-v', help='Verbose', action='store_true')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)


    accession = args.input
    my_tinder = sra_tinder(accession)
    i = my_tinder.scrape_qc()
    # ii = my_tinder.adapters()
    iii = my_tinder.scrape_organisms()
    print('\t'.join([accession, str(i), iii[0], iii[1], iii[2]]))