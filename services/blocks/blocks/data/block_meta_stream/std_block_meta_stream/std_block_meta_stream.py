from ..block_meta_stream import BlockMetaStream, BlockMeta
from typing import Awaitable, Optional, AsyncIterator
import requests
from websockets import client
from asyncio import get_event_loop
import json
from uuid import uuid4
import asyncio
import nest_asyncio
from pydantic import BaseModel, ValidationError

class AlchemyBlockResult(BaseModel):
    baseFeePerGas: str
    difficulty: str
    extraData: str
    gasLimit: str
    gasUsed: str
    hash: str
    logsBloom: str
    miner: str
    mixHash: str
    nonce: str
    number: str
    parentHash: str
    receiptsRoot: str
    sha3Uncles: str
    size: str
    stateRoot: str
    timestamp: str
    transactionsRoot: str


class AlchemyBlockParams(BaseModel):
    result: AlchemyBlockResult
    subscription: str


class AlchemyBlockMeta(BaseModel):
    jsonrpc: str
    method: str
    params: AlchemyBlockParams

nest_asyncio.apply()

ALCHEMY_WS_URL = "wss://eth-mainnet.alchemyapi.io/v2/GNauZOAEhjOc34zQQqQuXorOlmC6wJ6W"
WS_PAYLOAD = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "eth_subscribe",
    "params" : ["newHeads", True]
}

def mk_ws_payload(uuid : str = uuid4().hex):
    return {
        "id": uuid,
        "jsonrpc": "2.0",
        "method": "eth_subscribe",
        "params" : ["newHeads"]
    }

class StdBlockMetaStream(BlockMetaStream):
    
    
    ws : Optional[client.WebSocketClientProtocol]
    started : bool
    uuid : str
    
    def __init__(self) -> None:
        super().__init__()
        self.ws = None
        self.started = False
        self.uuid = uuid4().hex
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self._connect())
        
    async def _connect(self)->None:
        self.ws = await client.connect(ALCHEMY_WS_URL).__aenter__()
        
    async def start(self)->None:
        if not self.started:
            await self.ws.send(json.dumps(mk_ws_payload(self.uuid)))
        self.started = True
        
    def __aiter__(self) -> AsyncIterator[BlockMeta]:
        self.loop.run_until_complete(self.start())
        return self
    
    
    async def __anext__(self) -> Awaitable[BlockMeta]:
        
        await self.start()
        while True:
            try:
                d = json.loads(await self.ws.__aiter__().__anext__())
                Alchemy_block = AlchemyBlockMeta.parse_obj(d)
                return BlockMeta(id=Alchemy_block.params.result.number)
            except ValidationError as e:
                continue
            
    async def __aenter__(self):
        return self      
    
    async def __aexit__(self, __exc_type: type[BaseException] | None, __exc_value: BaseException | None, __traceback: None) -> bool | None:
        return await self.ws.close()