import enum


class IdentityRole(enum.Enum):
    DEFAULT = 'DEFAULT'
    ADMIN = 'ADMIN'


class EnvType(enum.Enum):
    PRODUCTION = 'PRODUCTION'
    LOCAL = 'LOCAL'
