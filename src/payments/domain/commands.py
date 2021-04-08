from dataclasses import dataclass

from payments.domain.model import Items, Payer, Charge, Address


class Command:
    pass


@dataclass
class PayByCreditCard(Command):
    charge: Charge
    items: Items
    payer: Payer
    address: Address
