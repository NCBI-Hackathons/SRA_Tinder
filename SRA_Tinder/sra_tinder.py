import sys
import os
import argparse
import urllib.request as ur
import re

class sra_tinder:
    _VERSION = 1.0



    def __init__(self, sra_file_name):
        self.sra_file_name = sra_file_name

    def scrape_organisms(self):
        url = "https://trace.ncbi.nlm.nih.gov/Traces/sra/?run={}".format(self.sra_file_name)
        string = ur.urlopen(url).read().decode()

        output = []

        table = str(re.findall("<h3>Strong signals<\/h3>.*?<\/table>", string, re.DOTALL))
        rows = re.findall("<tr>.*?<\/tr>", table, re.DOTALL)
        for row in rows:
            values = re.findall("<tdstyle=\"padding:.*?\">(.*?)<\/td>", str(row.replace('\n', '').replace(' ', '')),
                                re.DOTALL)
            if len(values) < 4:
                print("Error: {}".format(values))
                continue
            # if values[2] == '' or values[2] == 'species':
            #     continue
            if float(values[3]) < 2:
                continue
            output.append('\t'.join([self.sra_file_name] + values + ['\n']))
        return output

    def check_qc(self):
        qualities = {}
        with open(self.sra_file_name + '.fastq', 'r') as infile:
            quality = False
            for line in infile:
                if quality:
                    for char in line:
                        qualities[ord(char)] = qualities.get(ord(char), 0) + 1
                if line.startswith("+"):
                    quality = True
                    continue
        mean = 0
        count = 0
        for k,v in qualities.items():
            mean += k*v
            count += v

        return (mean/count) - 33

    def scrape_qc(self):

# sra_tinder('SRR3403834').scrape_organisms()

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


    line = args.input
    my_tinder = sra_tinder(line)
    i = my_tinder.check_qc()
    # ii = my_tinder.adapters()
    iii = my_tinder.scrape_organisms()
    print('\t'.join([line, str(i),  str(iii)]))