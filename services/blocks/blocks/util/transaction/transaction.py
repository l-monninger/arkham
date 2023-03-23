from pydantic import BaseModel

class TransactionMeta(BaseModel):
    
    from_addr : str
    to_addr : str
    hash : str
    wei : str

class Pricing(BaseModel):
    eth : float
    usd : float

class Transaction(TransactionMeta, Pricing):
   pass