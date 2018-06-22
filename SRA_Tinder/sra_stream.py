import asyncio
import os
import concurrent.futures

import sys
import traceback

from ngs import NGS
from ngs.ErrorMsg import ErrorMsg
from ngs.ReadCollection import ReadCollection
from ngs.Read import Read
from ngs.ReadIterator import ReadIterator

class SRA_Stream():

    def __init__(self):
        pass

    def stream_reads(self, foo, splitNum=1, splitNo=1):
        '''
        This is a blocking task, it needs to be run in an executor
        '''

        # open requested accession using SRA implementation of the API
        pipe = open(foo, 'w')        
        with NGS.openReadCollection(foo) as run:
            run_name = run.getName()

            # compute window to iterate through
            MAX_ROW = run.getReadCount()
            chunk = MAX_ROW/splitNum
            first = int(round(chunk*(splitNo-1)))
            next_first = int(round(chunk*(splitNo)))
            if next_first > MAX_ROW:
                next_first = MAX_ROW

            # start iterator on reads
            with run.getReadRange(first+1, next_first-first, Read.all) as it:
                i = 0
                while it.nextRead():
                    i += 1
                    if i > 20000: 
                        break
                    while it.nextFragment():
                        bases = it.getFragmentBases()
                        qualities=it.getFragmentQualities()
                        ids=it.getFragmentId()
                        if bases:
                            read = f'@{ids}\n{bases}\n+\n{qualities}'
                            print(read,file=pipe)
        os.unlink(foo)

    def run(self,accs):
        '''
        Stream SRA files into named pipes 

        Parameters
        ----------
        accs: an iterable of Run (str) names

        Output
        ------
        Opens a named pipe
        '''
        loop = asyncio.get_event_loop()
        tasks = []
        pool = concurrent.futures.ProcessPoolExecutor(max_workers=4)
        for acc in accs:
            print(f'Streaming {acc}', file=sys.stderr)
            try:
                os.unlink(acc)
            except FileNotFoundError as e:
                pass
            os.mkfifo(acc)
            future = loop.run_in_executor(pool, self.stream_reads, acc)
            tasks.append(future)
        results = asyncio.gather(*tasks)
        loop.run_until_complete(results)
        return results


if __name__ == '__main__':
    x = SRA_Stream()
    test_sets = ['SRR1105736',
        'SRR1105737',
        'SRR1105738',
        'SRR1105739',
        'SRR1105740',
        'SRR1105741',
        'SRR1224573',
        'SRR1224574'
    ]
    x.run(test_sets)
