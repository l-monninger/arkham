from typing import Protocol

class Server(Protocol):
    
    def serve(self, *, host : str, port : int)->None:
        pass