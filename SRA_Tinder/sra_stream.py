import asyncio
import os
import aiofiles



class SRA_Stream():

    def __init__(self):
        pass

    async def pipe_reads(self,pipe):
        async with aiofiles.open(pipe,mode='w') as pipe:
            for i in range(10):
                await pipe.write(str(i))
                await asyncio.sleep(1)
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
        tasks = []
        for run in runs:
            try:
                os.unlink(run)
            except Exception as e:
                pass
            os.mkfifo(run)
            tasks.append(self.pipe_reads(run))
        results = asyncio.gather(*tasks)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(results)
        return results
