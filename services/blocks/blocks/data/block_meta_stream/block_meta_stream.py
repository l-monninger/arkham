from typing import Protocol, AsyncIterator, ContextManager, AsyncContextManager
from blocks.util.block.block import BlockMeta

class BlockMetaStream(AsyncIterator[BlockMeta], AsyncContextManager):
    pass