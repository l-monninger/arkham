from ..transactions_meta_getter import TransactionsMetaGetter, TransactionMeta
from typing import AsyncIterator, Awaitable, List, Optional, Iterator
from pydantic import BaseModel, Field
import asyncio
import nest_asyncio
import json
from uuid import uuid1
nest_asyncio.apply()

# 0x1019e47
import requests

url = "https://eth-mainnet.alchemyapi.io/v2/GNauZOAEhjOc34zQQqQuXorOlmC6wJ6W"

headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

def mk_block_payload(*, uuid : str, block_id : str):
    return {
        "id": uuid,
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [block_id, True]
    }

class AlchemyTransaction(BaseModel):
    blockHash: str
    blockNumber: str
    hash: str
    accessList: Optional[List] = None
    chainId: Optional[str]
    from_: str = Field(..., alias='from')
    gas: str
    gasPrice: str
    input: str
    maxFeePerGas: Optional[str] = None
    maxPriorityFeePerGas: Optional[str] = None
    nonce: str
    r: str
    s: str
    to: Optional[str] = None
    transactionIndex: str
    type: str
    v: str
    value: str


class AlchemyResult(BaseModel):
    number: str
    hash: str
    transactions: List[AlchemyTransaction]
    difficulty: str
    extraData: str
    gasLimit: str
    gasUsed: str
    logsBloom: str
    miner: str
    mixHash: str
    nonce: str
    parentHash: str
    receiptsRoot: str
    sha3Uncles: str
    size: str
    stateRoot: str
    timestamp: str
    totalDifficulty: str
    transactionsRoot: str
    uncles: List
    baseFeePerGas: str


class AlchemyBlock(BaseModel):
    jsonrpc: str
    id: str
    result: AlchemyResult

class StdTransactionsGetter(TransactionsMetaGetter):
    
    block_id : str
    block : Optional[AlchemyBlock]
    txs_iterator : Optional[Iterator[AlchemyTransaction]]
    uuid : str
    
    def __init__(self, *, block_id : str) -> None:
        self.block_id = block_id
        self.uuid = uuid1().hex
        self.loop = asyncio.get_running_loop()
        self.loop.run_until_complete(self._get_block())
        
    async def _get_block(self):
        d = json.loads(requests.post(
            url, 
            json=mk_block_payload(uuid=self.uuid, block_id=self.block_id), 
            headers=headers).text
        )
        self.block = AlchemyBlock.parse_obj(d)
        self.txs_iterator = self.block.result.transactions.__iter__()
        
    def __aiter__(self) -> AsyncIterator[TransactionMeta]:
        return self
        
    async def __anext__(self) -> Awaitable[TransactionMeta]:
        
        try:
            n = self.txs_iterator.__next__()
            while n.to is None or n.from_ is None:
                # pending or incomplete tx, skip it
                n = self.txs_iterator.__next__()
            return TransactionMeta(from_addr=n.from_, to_addr=n.to, hash=n.hash, wei=n.value)
        except StopIteration as e:
            raise StopAsyncIteration()