from uuid import UUID


class UserAddress:
    address: str


class UserAdd:
    address: str
    uid: UUID
    thHash: str


class UserAddressR200:
    uid: int


class UserEmail:
    email: str
    address: str


class UserEmailR200:
    sbt: str


class UserCheck:
    address: str
    chainId: int

