from pydantic import BaseModel


class UserItemDtoSchema(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    last_login: str
    avatar_full_url: str
