from typing import Optional, List

from pydantic import BaseModel, EmailStr


#  
#  User Schema
# 

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    user_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    pass


# Properties to receive via API on update
class UserUpdate(UserBase):
    auth_uid: Optional[int] = None


class UserInDBBase(UserBase):
    uid: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    pass


#  
#  Auth Schema
# 


# Shared properties
class AuthBase(BaseModel):
    user_name: Optional[str] = None
    password: Optional[str] = None
    login_retry: Optional[int] = 0
    is_blocked: Optional[bool] = False
    user_type: Optional[str] = None


# Properties to receive via API on creation
class AuthCreate(AuthBase):
    user_name: str
    password: str
    login_retry: int = 0
    is_blocked: bool = False


# Properties to receive via API on update
class AuthUpdate(AuthBase):
    pass


class AuthInDBBase(AuthBase):
    uid: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Auth(AuthInDBBase):
    pass


# Additional properties stored in DB
class AuthInDB(AuthInDBBase):
    hashed_password: str


#
#  Permission Schema
#

# Shared properties
class PermissionBase(BaseModel):
    action: Optional[str] = None
    target: Optional[str] = None
    active: bool = False


# Properties to receive via API on creation
class PermissionCreate(PermissionBase):
    pass


# Properties to receive via API on update
class PermissionUpdate(PermissionBase):
    uid: Optional[int] = None


class PermissionInDBBase(PermissionBase):
    uid: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Permission(PermissionInDBBase):
    pass


# Additional properties stored in DB
class PermissionInDB(PermissionInDBBase):
    pass


#
#  Group Schema
#

# Shared properties
class GroupBase(BaseModel):
    name: Optional[str] = None
    keyword: Optional[str] = None
    members: Optional[List[User]] = None
    permissions: Optional[List[Permission]] = None
    active: bool = False


# Properties to receive via API on creation
class GroupCreate(GroupBase):
    pass


# Properties to receive via API on update
class GroupUpdate(GroupBase):
    uid: Optional[int] = None


class GroupInDBBase(GroupBase):
    uid: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Group(GroupInDBBase):
    pass


# Additional properties stored in DB
class GroupInDB(GroupInDBBase):
    pass
