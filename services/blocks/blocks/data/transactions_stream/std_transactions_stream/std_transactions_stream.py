from ..transactions_stream import TransactionsStream, Transaction
from blocks.util.transaction.transaction import Pricing
from typing import AsyncIterator, Awaitable
from ...transactions_meta_getter.transactions_meta_getter import TransactionsMetaGetter
from ...transactions_meta_getter.std_transaction_getter.std_transactions_meta_getter import StdTransactionsGetter
from .usd_conversion import convert_wei
from .wei import wei_to_eth
from typing import Optional


class StdTransactionsStream(TransactionsStream):
    
    meta_stream : TransactionsMetaGetter
    
    def __init__(self, *, block_id : Optional[str] = None, meta_stream : Optional[TransactionsMetaGetter] = None) -> None:
        super().__init__()
        if meta_stream is not None:
            self.meta_stream = meta_stream
        else:
            self.meta_stream = StdTransactionsGetter(block_id=block_id or "0x0")
    
    async def _get_pricing(self, *, wei : str)->Pricing:
        eth = wei_to_eth(wei=wei)
        usd = convert_wei(wei=wei)
        return Pricing(
            eth=eth,
            usd=usd
        )
    
    def __aiter__(self) -> AsyncIterator[Transaction]:
        return self
    
    async def __anext__(self) -> Awaitable[Transaction]:
        n = await self.meta_stream.__anext__()
        pricing = await self._get_pricing(wei=n.wei)
        return Transaction(
            to_addr=n.to_addr,
            from_addr=n.from_addr,
            hash=n.hash,
            wei=n.wei,
            eth=pricing.eth,
            usd=pricing.usd
        )