from blocks.util.runtime.deasync import deasync
import unittest
from .std_block_streamer import StdBlockStreamer
from blocks.data.block_stream.std_block_stream.std_block_stream import StdBlockStream

class StdBlockStreamerTest(unittest.TestCase):
    
    @deasync
    async def test_iterates_stream(self):
        streamer = StdBlockStreamer(blocks_stream=StdBlockStream())
        async def do(block):
            print(block)
        await streamer.subscribe(id=self, on_block=do)
        await streamer.stream()