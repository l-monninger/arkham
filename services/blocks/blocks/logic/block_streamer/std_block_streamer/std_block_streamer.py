from ..block_streamer import BlockStreamer, Block
from typing import Callable, Awaitable, Any, List
import weakref
from blocks.data.block_stream.block_stream import BlockStream
from blocks.data.block_stream.std_block_stream.std_block_stream import StdBlockStream
import asyncio

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
            try:
                await on_block(block)
            except Exception as e:
                print(e)
        
    async def unsubscribe(self, *, id: Any):
        del self.callbacks[id]
        
    async def handle_callbacks(self, *, block : Block):
        crs = []
        for listener_key in self.callbacks:
            crs.append(self.callbacks[listener_key](block))
        await asyncio.gather(*crs)
            
    def update_buff(self, *, block : Block):
        if len(self.buff) > self.buff_size:
             self.buff = self.buff[1:self.buff_size]
        self.buff.append(block)
        
    async def stream(self):
        async for block in self.blocks_stream:
            print("RECEIVED BLOCK")
            self.update_buff(block=block)
            await self.handle_callbacks(block=block)