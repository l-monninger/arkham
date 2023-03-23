from blocks.util.transaction.transaction import Transaction
from pydantic import BaseModel
from typing import Sequence

class BlockMeta(BaseModel):
    id : str

class Block(BlockMeta):
    
    txs : Sequence[Transaction] # though we expect to use Iterables, we need this to be consumed before being transmitted