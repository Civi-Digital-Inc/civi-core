import enum


class IdentityRole(enum.Enum):
    ADMIN = 'ADMIN'


class EnvType(enum.Enum):
    PRODUCTION = 'PRODUCTION'
    LOCAL = 'LOCAL'
