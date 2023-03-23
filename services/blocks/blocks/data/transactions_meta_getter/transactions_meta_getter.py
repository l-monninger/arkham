from typing import Protocol, AsyncIterator
from blocks.util.transaction.transaction import TransactionMeta

class TransactionsMetaGetter(AsyncIterator[TransactionMeta]):
    pass