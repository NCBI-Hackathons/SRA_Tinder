import sys
import os
import argparse
import urllib.request as ur
import re

VERSION = 1.0


class sra_tinder_web:


    def __init__(self, sra_file_name):
        self.sra_file_name = sra_file_name




    def scrape_run(self, essential=True):
        """
        Scrapes the URL metadata page for the run accession
        :return: a float rounded to two decimal places representing the average quality score of a SRA run
        """
        url = "https://trace.ncbi.nlm.nih.gov/Traces/sra/?run={}".format(self.sra_file_name)
        string = ur.urlopen(url).read().decode()
        ret = {}

        #Get organism information from the reads
        count_organisms = 0
        output = []
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

        ret['top_org'] = output[0]
        ret['top_org_%'] = output[1]
        ret['#_1%_orgs'] = output[2]

        #scrape and count qc data for reads
        table = re.findall('<table class="zebra run-metatable">.*?<div class="center">Phred quality score<\/div>', string, re.DOTALL)
        table = str(table)
        entries = re.findall('<span title="(.*?) : (.*?)" style=', table, re.DOTALL)
        d = {}
        for score in entries:
            d[int(score[0])] = int(score[1].replace(',', ''))
        total_qual = 0
        count = 0
        q30_plus_count = 0

        for k, v in d.items():
            total_qual += k * v
            count += v
            if k >= 30:
                q30_plus_count += v

        ret['mean_qual'] = round(total_qual/count, 2)
        ret['%q30'] = round(q30_plus_count/count, 2) * 100

        #Scrape the project that contains this run
        study = re.findall("<a href=\"\?study=(.*?)\">", string, re.DOTALL)
        ret['study'] = study[0]

        #Scrape the source, strategy, layout, and selection
        experiment_table = re.findall('<table class=\"zebra\">(.*?)<\/tr>(.*?)<\/table>', string, re.DOTALL)
        headers = re.findall('<th>(.*?)</th>', experiment_table[0][0], re.DOTALL)
        values = re.findall('<td>(.*?)</td>', experiment_table[0][1], re.DOTALL)

        headers = headers[1:]
        ret['source'] = values[3]
        ret['strategy'] = values[2]
        ret['selection'] = values[4]
        ret['layout'] = values[5]

        #scraping bioproject and pubmed links
        project = re.findall('<a href=\"https://www.ncbi.nlm.nih.gov/bioproject/(.*?)\">', string, re.DOTALL)
        project = project[0]
        project_string = ur.urlopen("https://www.ncbi.nlm.nih.gov/bioproject/{}".format(project)).read().decode()
        taxonomy_id = re.findall('<td class="CTtitle">Organism</td><td class="CTcontent"><a href=".*?" class="RegularLinkB" title=\"(.*?)\"', project_string, re.DOTALL)
        try:
            publications = re.findall('<td class="CTtitle">Publications</td><td class="CTcontent">(.*?)Publications</td></tr><tr><td>', project_string, re.DOTALL)
            pmids = re.findall('href=\"/pubmed/(.*?)\"', publications[0], re.DOTALL)
            pmids = ['https://www.ncbi.nlm.nih.gov/pubmed/?term={}'.format(x) for x in pmids]

            ret['pmids'] = pmids
            ret['taxon_id'] = taxonomy_id[0]
        except Exception as e:
            # sys.stderr.write("Error reading PMIDS for {}\n Error is: {}\n".format(self.sra_file_name, str(e)))
            ret['pmids'] = 'None'
            ret['taxon_id'] = 'None'

        return ret



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='Input File', required=True)
    parser.add_argument('-e', '--essential', help='Run with only the essential fields (accession, average_qual_Score, pass/fail, top_organism, top_organism%, #_organisms >1%, USER_SUBMITTED_Type', action='store_true')



    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)

    with open(args.input, 'r') as infile:
        if args.essential:
            titleline = [
                "Accession", "Percent_Quality_Scores_above_30", "Pass_or_Fail_70%_Q30", "most_abundent_organism",
                "percent_abundence", "number_of_organims_greater_than_1%_abundence",
                "USER_LABELED_data_type(may_be_incorrect)"]
        else:
            titleline = [
                "Run Accession", "Study", "Percent Quality Scores above 30", "Pass or Fail 70% Q30",
                "mean_quality_score", "most_abundent_organism",
                "percent_abundence", "number_of_organims_greater_than_1%_abundence", "Taxon_Orgs", "*Source",
                "*Strategy", "*Selection", "*Layout", "URL", "PUBMED"]
        sys.stdout.write('\t'.join(titleline + ['\n']))
        for line in infile:
            line = line.strip()
            my_tinder = sra_tinder_web(line)
            run_info = my_tinder.scrape_run()
            m = {True: 'Pass', False: 'Fail'}
            final_output_line = []
            url = "https://trace.ncbi.nlm.nih.gov/Traces/sra/?run={}".format(line)

            if not args.essential:


                final_output_line += [line, run_info['study'], run_info['%q30'], m[(run_info['%q30'] > 70)],
                                      run_info['mean_qual'], run_info['top_org'], run_info['top_org_%'],
                                      run_info['#_1%_orgs'], run_info['taxon_id'], run_info['source'],
                                      run_info['strategy'], run_info['selection'], run_info['layout'], url,
                                      run_info['pmids']]
            else:

                final_output_line += [line, run_info['%q30'], m[(run_info['%q30'] > 70)], run_info['top_org'],
                                      run_info['top_org_%'], run_info['#_1%_orgs'], run_info['source']]
            final_output_line = [str(x) for x in final_output_line] + ['\n']
            sys.stdout.write('\t'.join(final_output_line))

