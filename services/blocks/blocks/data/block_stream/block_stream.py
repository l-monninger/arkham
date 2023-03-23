from typing import Protocol, AsyncIterator
from blocks.util.block.block import Block


class BlockStream(AsyncIterator[Block]):
    pass