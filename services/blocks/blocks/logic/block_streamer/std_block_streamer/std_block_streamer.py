from ..block_streamer import BlockStreamer, Block
from typing import Callable, Awaitable, Any, List
import weakref
from blocks.data.block_stream.block_stream import BlockStream
from blocks.data.block_stream.std_block_stream.std_block_stream import StdBlockStream

class StdBlockStreamer(BlockStreamer):
    
    callbacks : weakref.WeakKeyDictionary
    blocks_stream : BlockStream
    buff : List[Block]
    buff_size : int
    
    def __init__(self, *, blocks_stream : BlockStream = StdBlockStream(), buff_size : int = 5) -> None:
        self.callbacks = weakref.WeakKeyDictionary()
        self.blocks_stream = blocks_stream
        self.buff_size = buff_size
        self.buff = []
    
    async def subscribe(self, *, id: Any, on_block: Callable[[Block], Awaitable[None]]):
        self.callbacks[id] = on_block
        for block in self.buff:
            await on_block(block)
        
    async def unsubscribe(self, *, id: Any):
        del self.callbacks[id]
        
    async def handle_callbacks(self, *, block : Block):
        for listener_key in self.callbacks:
            await self.callbacks[listener_key](block)
            
    def update_buff(self, *, block : Block):
        self.buff = [*self.buff[0:self.buff_size - 1], block]
        
    async def stream(self):
        async for block in self.blocks_stream:
            print("RECEIVED BLOCK")
            self.update_buff(block=block)
            await self.handle_callbacks(block=block)