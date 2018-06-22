import asyncio
import os
import aiofiles

import sys
import traceback

from ngs import NGS
from ngs.ErrorMsg import ErrorMsg
from ngs.ReadCollection import ReadCollection
from ngs.Read import Read
from ngs.ReadIterator import ReadIterator

def run(acc, splitNum=1, splitNo=1):
    '''
    This is a blocking task, it needs to be run in an executor
    '''
    # open requested accession using SRA implementation of the API
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
                        read = f'@{ids}\n{bases}\n+\n{qualities}\n'
                        return read
                        #print ("\t{} - {}".format(bases, "aligned" if it.isAligned() else "unaligned"))
                        #print ('@'+ids) 
                        #print (bases)
                        #print ('+'+ids)
                        #print (qualities)
                        #print ("\n")
            #print ("Read {} spots for {}".format(i,  run_name))

class SRA_Stream():

    def __init__(self):
        pass

    async def pipe_reads(self,acc,loop):
        #loop = asyncio.get_event_loop()
        async with aiofiles.open(acc,mode='w') as pipe:
            future = loop.run_in_executor(None, run, acc)
            data = await future 
            await pipe.write(str(data))
        return None

    def run(self,runs):
        '''
        Stream SRA files into named pipes 

        Parameters
        ----------
        runs: an iterable of Run (str) names

        Output
        ------
        Opens a named pipe
        '''
        loop = asyncio.get_event_loop()
        tasks = []
        for run in runs:
            try:
                os.unlink(run)
            except FileNotFoundError as e:
                pass
            os.mkfifo(run)
            tasks.append(self.pipe_reads(run,loop))
        results = asyncio.gather(*tasks)
        loop.run_until_complete(results)
        return results


if __name__ == '__main__':
    x = SRA_Stream()
    x.run(['SRR020192'])
