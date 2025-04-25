from pydantic import BaseModel
from sqlalchemy import Boolean, Column,Integer,String
from sqlalchemy.orm import validates

class MetaAuthorization:
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(50),unique=True)
    normalizedName=Column(String(50),unique=True)
    description=Column(String(255),nullable=False)
    is_active=Column(Boolean,default=True)


    @validates('name')
    def validate_name(self,key,value):
        self.normalizedName = value.upper().strip() if value else None
        return value

class MetaAuthorizationBaseModel(BaseModel):
    id:int
    normalizedName:str
    is_active: bool

class MetaAuthorizationPydanticModel(MetaAuthorizationBaseModel):
    name: str

class MetaUserPrivilegeModel(BaseModel):
    privilege:MetaAuthorizationBaseModel
    is_active:bool


class MetaUserRoleModel(BaseModel):
    role:MetaAuthorizationBaseModel
    is_active:bool


