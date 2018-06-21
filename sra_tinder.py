import sys
import os
import argparse


class sra_tinder:
    _VERSION = 1.0

    SCORES = {
        '!': 0, '"': 1, '#': 2, '$': 3, '%': 4, '&': 5, '\'': 6, '(': 7, ')': 8,
        '*': 9, '+': 10, ',': 11, '-': 12, '.': 13, '/': 14, '0': 15, '1': 16,
        '2': 17, '3': 18, '4': 19, '5': 20, '6': 21, '7': 22, '8': 23, '9': 24,
        ':': 25, ';': 26, '<': 27, '=': 28, '>': 29, '?': 30, '@': 31, 'A': 32, 'B': 33,
        'C': 34, 'D': 35, 'E': 36, 'F': 37, 'G': 38, 'H': 39, 'I': 40, 'J': 41}

    def __init__(self, sra_file_name):
        self.sra_file_name = sra_file_name

    def scrape_organisms(self):
        url = "https://trace.ncbi.nlm.nih.gov/Traces/sra/?run={}".format(acc)
        string = ur.urlopen(url).read().decode()

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
            # if float(values[3]) < 2:
            #     continue
            outfile.write('\t'.join([acc] + values + ['\n']))

    def check_qc(self):
        qualities = {}
        with open(self.sra_file_name, 'r') as infile:
            quality = False
            for line in infile:
                if quality:
                    for char in line:
                        qualities[ord(char)] = qualities.get(ord[char], 0) + 1
                if line.startswith("+"):
                    quality = True
                    continue
        mean = 0
        count = 0
        for k,v in qualities.items()
            mean += k*v
            count += v


        print(qualities)
        print(mean, count)
sra_tinder('test.fastq').check_qc








"""
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
"""