class RbacError(Exception):
    """Base exception for all RBAC domain errors."""


class PermissionNotFoundError(RbacError):
    """Permission with the given identifier was not found."""


class PermissionAlreadyExistsError(RbacError):
    """Permission with the given name already exists."""


class RoleNotFoundError(RbacError):
    """Role with the given identifier was not found."""


class RoleAlreadyExistsError(RbacError):
    """Role with the given name already exists."""


class PermissionDeniedError(RbacError):
    """User does not have the required permission."""


class RoleAlreadyAssignedError(RbacError):
    """Role is already assigned to the user."""


class RoleNotAssignedError(RbacError):
    """Role is not assigned to the user."""


class PermissionAlreadyAssignedError(RbacError):
    """Permission is already assigned to the role."""


class PermissionNotAssignedError(RbacError):
    """Permission is not assigned to the role."""


RBAC_EXCEPTIONS: dict[type[RbacError], tuple[str, int]] = {
    PermissionNotFoundError: ("PERMISSION_NOT_FOUND", 404),
    PermissionAlreadyExistsError: ("PERMISSION_ALREADY_EXISTS", 409),
    RoleNotFoundError: ("ROLE_NOT_FOUND", 404),
    RoleAlreadyExistsError: ("ROLE_ALREADY_EXISTS", 409),
    PermissionDeniedError: ("PERMISSION_DENIED", 403),
    RoleAlreadyAssignedError: ("ROLE_ALREADY_ASSIGNED", 409),
    RoleNotAssignedError: ("ROLE_NOT_ASSIGNED", 400),
    PermissionAlreadyAssignedError: ("PERMISSION_ALREADY_ASSIGNED", 409),
    PermissionNotAssignedError: ("PERMISSION_NOT_ASSIGNED", 400),
}
