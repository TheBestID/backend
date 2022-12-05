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
    blockchain: str


class GetUser:
    uid: str


class CompanyEmail:
    address:        str
    chainId:        int
    blockchain:     str
    company_email:  str
    company_link:   str
    githubCode:     str
    email:          str


class CompanyMsgParams:
    address:        str
    chainId:        int
    blockchain:     str
    email_token:    str
    github_token:   str