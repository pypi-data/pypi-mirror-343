from enum import Enum
from typing import NamedTuple,List

class PermissionAction(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"


class PermissionModule(str, Enum):
    USER = "users"
    ROLE = "roles"
    PERMISSION = "permissions"
    ROLE_PERMISSION = "role_permissions"  # assign permissions to roles
    USER_ROLE = "user_roles"  # assign roles to users
    PRODUCT = "products"
    SELLER = "sellers"
    FEATURE_REQUEST = "feature_requests"
    SUPPORT_CASE = "support_cases"
    EXPORT = "export"  # for data export functionality


class PermissionData(NamedTuple):
    name: str
    description: str
    resource: str
    action: str


class PermissionConstants:
    # User Permissions
    USER_CREATE = PermissionData(
        name="Create User",
        description="Can create users",
        resource=PermissionModule.USER,
        action=PermissionAction.CREATE,
    )
    USER_READ = PermissionData(
        name="Read User",
        description="Can read user data",
        resource=PermissionModule.USER,
        action=PermissionAction.READ,
    )
    USER_UPDATE = PermissionData(
        name="Update User",
        description="Can update user data",
        resource=PermissionModule.USER,
        action=PermissionAction.UPDATE,
    )

    USER_DELETE = PermissionData(
        name="Delete User",
        description="Can delete users",
        resource=PermissionModule.USER,
        action=PermissionAction.DELETE,
    )
    # seller permissions
    SELLER_CREATE = PermissionData(
        name="Create Seller",
        description="Can create sellers",
        resource=PermissionModule.SELLER,
        action=PermissionAction.CREATE,
    )
    SELLER_READ = PermissionData(
        name="Read Seller",
        description="Can read seller data",
        resource=PermissionModule.SELLER,
        action=PermissionAction.READ,
    )
    SELLER_UPDATE = PermissionData(
        name="Update Seller",
        description="Can update seller data",
        resource=PermissionModule.SELLER,
        action=PermissionAction.UPDATE,
    )

    SELLER_DELETE = PermissionData(
        name="Delete Seller",
        description="Can delete sellers",
        resource=PermissionModule.SELLER,
        action=PermissionAction.DELETE,
    )

    # product permissions
    PRODUCT_CREATE = PermissionData(
        name="Create Product",
        description="Can create products",
        resource=PermissionModule.PRODUCT,
        action=PermissionAction.CREATE,
    )
    PRODUCT_READ = PermissionData(
        name="Read Product",
        description="Can read product data",
        resource=PermissionModule.PRODUCT,
        action=PermissionAction.READ,
    )
    PRODUCT_UPDATE = PermissionData(
        name="Update Product",
        description="Can update product data",
        resource=PermissionModule.PRODUCT,
        action=PermissionAction.UPDATE,
    )
    PRODUCT_DELETE = PermissionData(
        name="Delete Product",
        description="Can delete products",
        resource=PermissionModule.PRODUCT,
        action=PermissionAction.DELETE,
    )

    # role
    ROLE_CREATE = PermissionData(
        name="Create Role",
        description="Can create roles",
        resource=PermissionModule.ROLE,
        action=PermissionAction.CREATE,
    )
    ROLE_READ = PermissionData(
        name="Read Role",
        description="Can read role data",
        resource=PermissionModule.ROLE,
        action=PermissionAction.READ,
    )
    ROLE_UPDATE = PermissionData(
        name="Update Role",
        description="Can update role data",
        resource=PermissionModule.ROLE,
        action=PermissionAction.UPDATE,
    )
    ROLE_DELETE = PermissionData(
        name="Delete Role",
        description="Can delete roles",
        resource=PermissionModule.ROLE,
        action=PermissionAction.DELETE,
    )

    # permission
    PERMISSION_READ = PermissionData(
        name="Read Permission",
        description="Can read permission data",
        resource=PermissionModule.PERMISSION,
        action=PermissionAction.READ,
    )

    # user_role
    ASSIGN_ROLE_TO_USER = PermissionData(
        name="Assign Role to User",
        description="Can assign roles to users",
        resource=PermissionModule.USER_ROLE,
        action=PermissionAction.UPDATE,
    )
    REMOVE_ROLE_FROM_USER = PermissionData(
        name="Remove Role from User",
        description="Can remove roles from users",
        resource=PermissionModule.USER_ROLE,
        action=PermissionAction.DELETE,
    )
    READ_USER_ROLE = PermissionData(
        name="Read User Role",
        description="Can read user role data",
        resource=PermissionModule.USER_ROLE,
        action=PermissionAction.READ,
    )
    # role_permission
    ASSIGN_PERMISSION_TO_ROLE = PermissionData(
        name="Assign Permission to Role",
        description="Can assign permissions to roles",
        resource=PermissionModule.ROLE_PERMISSION,
        action=PermissionAction.UPDATE,
    )
    REMOVE_PERMISSION_FROM_ROLE = PermissionData(
        name="Remove Permission from Role",
        description="Can remove permissions from roles",
        resource=PermissionModule.ROLE_PERMISSION,
        action=PermissionAction.DELETE,
    )

    # feature_request
    FEATURE_REQUEST_CREATE = PermissionData(
        name="Create Feature Request",
        description="Can create feature requests",
        resource=PermissionModule.FEATURE_REQUEST,
        action=PermissionAction.CREATE,
    )
    FEATURE_REQUEST_READ = PermissionData(
        name="Read Feature Request",
        description="Can read feature request data",
        resource=PermissionModule.FEATURE_REQUEST,
        action=PermissionAction.READ,
    )
    FEATURE_REQUEST_UPDATE = PermissionData(
        name="Update Feature Request",
        description="Can update feature request data",
        resource=PermissionModule.FEATURE_REQUEST,
        action=PermissionAction.UPDATE,
    )
    FEATURE_REQUEST_DELETE = PermissionData(
        name="Delete Feature Request",
        description="Can delete feature requests",
        resource=PermissionModule.FEATURE_REQUEST,
        action=PermissionAction.DELETE,
    )

    # support_case
    SUPPORT_CASE_CREATE = PermissionData(
        name="Create Support Case",
        description="Can create support cases",
        resource=PermissionModule.SUPPORT_CASE,
        action=PermissionAction.CREATE,
    )
    SUPPORT_CASE_READ = PermissionData(
        name="Read Support Case",
        description="Can read support case data",
        resource=PermissionModule.SUPPORT_CASE,
        action=PermissionAction.READ,
    )

    SUPPORT_CASE_UPDATE = PermissionData(
        name="Update Support Case",
        description="Can update support case data",
        resource=PermissionModule.SUPPORT_CASE,
        action=PermissionAction.UPDATE,
    )

    SUPPORT_CASE_DELETE = PermissionData(
        name="Delete Support Case",
        description="Can delete support cases",
        resource=PermissionModule.SUPPORT_CASE,
        action=PermissionAction.DELETE,
    )

    # export permissions
    EXPORT_READ = PermissionData(
        name="Export Data",
        description="Can export data from the system",
        resource=PermissionModule.EXPORT,
        action=PermissionAction.READ,
    )

    @classmethod
    def get_all_permissions(cls) -> List[PermissionData]:
        """Get all defined permissions"""
        return [
            value
            for name, value in cls.__dict__.items()
            if isinstance(value, PermissionData)
        ]

