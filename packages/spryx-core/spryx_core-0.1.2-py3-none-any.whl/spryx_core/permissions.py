from enum import StrEnum, unique


@unique
class Permission(StrEnum):
    READ_USERS = "users:read"
    WRITE_USERS = "users:write"
    READ_ORDERS = "orders:read"
