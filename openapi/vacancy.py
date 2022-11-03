from uuid import UUID

class VacancyTemplate:
    id: str
    owner_uuid: UUID
    price: int
    category: str
    timestamp: str
    info: str   