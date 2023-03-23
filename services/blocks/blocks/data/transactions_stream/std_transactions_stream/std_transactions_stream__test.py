from blocks.util.runtime.deasync import deasync
import unittest
from blocks.data.transactions_meta_getter.std_transaction_getter.std_transactions_meta_getter import StdTransactionsGetter
from .std_transactions_stream import StdTransactionsStream

class StdTransactionsGetterTest(unittest.TestCase):
    
    @deasync
    async def test_iterates_stream(self):
        meta_stream = StdTransactionsGetter(block_id="0x1019e47")
        txs = StdTransactionsStream(meta_stream=meta_stream)
        async for tx in txs:
            print(tx)