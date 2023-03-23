from blocks.util.transaction.transaction import Transaction
from typing import AsyncIterator, Optional
from ..transactions_meta_getter.transactions_meta_getter import TransactionsMetaGetter

class TransactionsStream(AsyncIterator[Transaction]):
    def __init__(self, *, block_id : Optional[str] = None, meta_stream : Optional[TransactionsMetaGetter] = None) -> None:
        super().__init__()