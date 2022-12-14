from uuid import UUID


class VacancyTemplate:
    owner_uuid: UUID
    price: int
    category: str
    info: str


class Vacancy:
    address: str
    chainId: int
    blockchain: str
    price: int
    category: str
    info: str


class VacancyAdd:
    address: str
    chainId: int
    blockchain: str
    sbt_id: UUID
    txHash: str


class GetVacancy:
    address: str
    chainId: int


class VacancyEdit:
    id: int
    address: str
    chainId: int
    address: str
    price: int
    category: str
    info: str


class GetPreviews:
    value_sorted: str
    offset: int
    top_number: int
    in_asc: bool


class GetPreviewsBySTR:
    sort_type1: str
    sort_value1: str
    sort_value2: str
    offset_number: int
    top_number: int
    in_asc: bool


class GetPreviewsByID:
    id: int


class Delete:
    id: int
    address: str
    chainId: int


class Confirm:
    id: int
    address: str
    chainId: int
    hash: str
