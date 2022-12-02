from uuid import UUID

from sanic_openapi.openapi3.types import Byte, Object, Binary

Achievement = {
    'schema': {
        "type": "object",
        "properties": {
            "from_address": {
                "type": "string"
            },
            "to_address": {
                "type": "string"
            },
            "blockchain": {
                "type": "string"
            },
            "chainId": {
                "type": "integer"
            },
            "data": {
                "type": "object"
            },
            "image": {
                "type": "string",
                "format": "binary"
            }
        }
    }
}


class GetAchievement:
    address: str
    chainId: int


class AchievementAdd:
    address: str
    chainId: int
    blockchain: str
    sbt_id: UUID
    txHash: str
