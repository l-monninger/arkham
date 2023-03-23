from blocks.util.runtime.deasync import deasync
import unittest
from .std_block_meta_stream import StdBlockMetaStream

class StdBlockMetaStreamTest(unittest.TestCase):
    
    @deasync
    async def test_iterates_stream(self):
        stream = StdBlockMetaStream()
        async for entry in stream:
            print("ENTRY: ", entry)
            self.assertIsNotNone(entry)