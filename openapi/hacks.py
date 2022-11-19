class AddHack:
    address: str
    chainId: int
    theme: str
    base_color: str
    font_head: str
    font_par: str
    hackathon_name: str
    description: str
    back_url: str
    logo_url: str
    price: int
    pool: str
    descr_price: str
    sbt_url: str
    task_descr: str
    social_link: str
    category: str


class CreateTable:
    drop: bool


class SortByInt:
    sort_value: str
    offset_number: int
    top_number: int
    in_asc: bool


class SortByStr:
    sort_type: str
    sort_value: str
    sort_value_int: str
    offset_number: int
    top_number: int
    in_asc: bool


class GetById:
    id: int
