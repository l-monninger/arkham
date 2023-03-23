from ..server import Server
from fastapi import FastAPI, WebSocket
from blocks.logic.block_streamer.block_streamer import BlockStreamer
from blocks.logic.block_streamer.std_block_streamer.std_block_streamer import StdBlockStreamer
from blocks.util.block.block import Block
import uvicorn
from typing import Optional
import asyncio
import concurrent.futures
import nest_asyncio
from time import sleep
import sys
nest_asyncio.apply()

class StdServer(Server):
    
    app : FastAPI
    block_streamer : BlockStreamer
    stream_pool : concurrent.futures.ThreadPoolExecutor
    server_pool : concurrent.futures.ThreadPoolExecutor
    
    def __init__(self, *, block_streamer : Optional[BlockStreamer] = StdBlockStreamer()) -> None:
        
        self.app = FastAPI()
        self.block_streamer = block_streamer
        self.loop = asyncio.get_event_loop()
        self.stream_pool = concurrent.futures.ThreadPoolExecutor()
        self.server_pool = concurrent.futures.ThreadPoolExecutor()
    
    def build_app(self)->None:
        
        @self.app.get("/_health")
        async def check_health():
            return True
        
        @self.app.websocket("/blocks")
        async def stream_blocks(websocket : WebSocket):
            await websocket.accept()
            
            async def send_to_client(block : Block):
                await websocket.send_json(block.dict())
                
            await self.block_streamer.subscribe(id=websocket, on_block=send_to_client)
            
            try:
                while True:
                    await websocket.receive()
            except Exception as e:
                await self.block_streamer.unsubscribe(id=websocket)
        
           
         
    async def run_server(self, *, host : str, port : int):
       uvicorn.run(app=self.app, host=host, port=port)
        
    
    def serve(self) -> None:
        self.build_app()
        self.loop.run_until_complete(asyncio.gather(
            self.block_streamer.stream(),
            self.run_server()
        ))
      