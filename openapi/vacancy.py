from uuid import UUID

class VacancyTemplate:
    owner_uuid: UUID
    price: int
    category: str
    info: str   

class VacancyAdd:
    address: str
    chainId: int
    owner_uuid: UUID
    price: int
    category: str
    info: str   

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


class GetPreviewsBySTR:
    sort_type1: str
    sort_value1: str
    sort_value2: str
    offset_number: int
    top_number: int
    

class GetPreviewsByID:
    id: int


class Delete:
    id: int
    address: str
    chainId: int