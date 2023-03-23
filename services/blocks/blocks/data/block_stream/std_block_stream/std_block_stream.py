from ..block_stream import BlockStream, Block
from blocks.data.block_meta_stream.block_meta_stream import BlockMetaStream
from blocks.data.block_meta_stream.std_block_meta_stream.std_block_meta_stream import StdBlockMetaStream
from blocks.data.transactions_stream.transactions_stream import TransactionsStream
from blocks.data.transactions_stream.std_transactions_stream.std_transactions_stream import StdTransactionsStream
from typing import AsyncIterator, Awaitable

class StdBlockStream(BlockStream):
    
    block_meta_stream : BlockMetaStream
    tx_stream : type[TransactionsStream]
    
    def __init__(self, *, block_meta_stream : BlockMetaStream = StdBlockMetaStream(), tx_stream : type[TransactionsStream] = StdTransactionsStream) -> None:
        super().__init__()
        self.block_meta_stream = block_meta_stream
        self.tx_stream = tx_stream
        
    def __aiter__(self) -> AsyncIterator[Block]:
        return self
        
    async def __anext__(self) -> Awaitable[Awaitable]:
        n = await self.block_meta_stream.__anext__()
        tx_stream = self.tx_stream(block_id=n.id)
        txs = []
        async for tx in tx_stream:
            txs.append(tx)
        return Block(
            id=n.id,
            txs=txs # we may be able to lazify this more, but I'm not sure how pydantic handles async iterator to sequence conversion
        )