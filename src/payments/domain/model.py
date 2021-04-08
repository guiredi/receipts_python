from dataclasses import dataclass


@dataclass
class Charge:
    token: str
    customer_id: str
    email: str
    installments: str
    keep_dunning = False


@dataclass
class Items:
    description: str
    qty: int
    price_cents: int


@dataclass
class Payer:
    cpf_cnpj: str
    name: str
    phone_prefix: int
    phone: str
    email: str


@dataclass
class Address:
    street: str
    number: int
    district: str
    city: str
    state: str
    zip_code: str
    complement: str


class Transaction:
    def __init__(self, payment_method: str, gateway: str, value: int):
        self.payment_method = payment_method
        self.gateway = gateway
        self.value = value
