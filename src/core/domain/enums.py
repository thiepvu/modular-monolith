import enum


class ExtendedEnum(enum.Enum):
    @classmethod
    def list(cls):
        """Returns a list of all enum values."""
        return [c.value for c in cls]

    @classmethod
    def choices(cls):
        """Returns a list of tuples (value, name) for Django choices."""
        return [(c.value, c.name) for c in cls]


class UserStatusEnum(ExtendedEnum):
    Active = "active"
    Inactive = "inactive"


class DbEntityEnum(ExtendedEnum):
    Workspace = "workspace"
    Dataset = "dataset"
    Project = "project"
    Comment = "comment"


class UserRoleEnum(ExtendedEnum):
    Admin = "SYS_ADMIN"
