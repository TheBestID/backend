from uuid import UUID


class Achievement:
    from_address: str
    to_address: str
    chainId: int
    data: {}


class GetAchievement:
    address: str
    chainId: int


class AchievementAdd:
    address: str
    chainId: int
    sbt_id: UUID
    txHash: str
