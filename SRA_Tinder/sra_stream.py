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

    def stream_reads(self, acc, splitNum=1, splitNo=1):
        '''
        This is a blocking task, it needs to be run in an executor
        '''

        # open requested accession using SRA implementation of the API
        pipe_path = self.get_pipe(acc)
        pipe = open(pipe_path, 'w')        
        with NGS.openReadCollection(acc) as run:
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
        os.unlink(pipe_path)
        return None

    def _create_pipe(self,acc):
        '''
        Create a named pipe based on an SRA Accession
        '''
        acc = self.get_pipe(acc)
        try:
            os.unlink(acc)
        except FileNotFoundError as e:
            pass
        os.mkfifo(acc)

    def get_pipe(self,acc):
        '''
        Get a pipe name based off the accession
        name. 

        NOTE: This does not open the pipe
        '''
        # Generate a generic filename
        if not acc.endswith('.fastq'):
            acc = acc + '.fastq'
        return acc

    def stream(self,acc, pool=None):
        '''
        Stream SRA files into named pipes 

        Parameters
        ----------
        accs: an iterable of Run (str) names

        Returns
        ------
        A future containing s
        '''
        print(f'Streaming {acc}', file=sys.stderr)
        if pool is None:
            pool = concurrent.futures.ProcessPoolExecutor()
        self._create_pipe(acc)
        loop = asyncio.get_event_loop()
        future = loop.run_in_executor(pool, self.stream_reads, acc)
        return future


if __name__ == '__main__':
    x = SRA_Stream()
    test_sets = [
        'SRR1105736',
        'SRR1105737',
        'SRR1105738',
        'SRR1105739',
        'SRR1105740',
        'SRR1105741',
        'SRR1224573',
        'SRR1224574'
    ]
    x.run(test_sets)
