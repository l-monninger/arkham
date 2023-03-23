from blocks.util.runtime.deasync import deasync
import unittest
from .std_transactions_meta_getter import StdTransactionsGetter

class StdTransactionsGetterTest(unittest.TestCase):
    
    @deasync
    async def test_iterates_stream(self):
        txs = StdTransactionsGetter(block_id="0x1019e47")
        async for tx in txs:
            self.assertIsNotNone(tx)
            self.assertIsNotNone(tx.to_addr)
            self.assertIsNotNone(tx.from_addr)
            self.assertIsNotNone(tx.hash)