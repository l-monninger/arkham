from typing import Protocol, Callable, Dict, Any, Awaitable
from blocks.util.block.block import Block

class BlockStreamer(Protocol):
    
    async def subscribe(self, *, id : Any, on_block : Callable[[Block], Awaitable[None]]):
        pass
    
    async def unsubscribe(self, *, id : Any):
        pass
    
    async def stream(self):
        pass