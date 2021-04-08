import abc

from payments.app import db
from payments.domain import model
from payments.domain.model import Transaction


class TransactionRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, product: model.Transaction):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, sku) -> model.Transaction:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *, uuid: str, transaction: Transaction) -> model.Transaction:
        raise NotImplementedError


class SqlAlchemyTransactionRepository(TransactionRepository):
    def add(self, transaction: Transaction) -> model.Transaction:
        db.session.add(transaction)
        db.session.commit()
        return transaction

    def get(self, *, uuid: str) -> model.Transaction:
        return db.session.query(model.Transaction).filter(uuid=uuid).first()

    def update(self, *, uuid: str, transaction: Transaction) -> model.Transaction:
        return db.session.query(model.Transaction).filter(uuid=uuid).update(transaction)
