from blocks.util.runtime.deasync import deasync
import unittest
from .std_block_stream import StdBlockStream
from blocks.data.block_meta_stream.std_block_meta_stream.std_block_meta_stream import StdBlockMetaStream

class StdBlockStreamTest(unittest.TestCase):
    
    @deasync
    async def test_iterates_stream(self):
        stream = StdBlockStream(block_meta_stream=StdBlockMetaStream())
        async for entry in stream:
            print(entry)
            self.assertIsNotNone(entry)