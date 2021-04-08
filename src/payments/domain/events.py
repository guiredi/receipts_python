from dataclasses import dataclass

from payments.domain.model import Charge, Items, Payer, Address


class Event:
    pass


@dataclass
class PayedByCreditCard(Event):
    charge: Charge
    items: Items
    payer: Payer
    address: Address
