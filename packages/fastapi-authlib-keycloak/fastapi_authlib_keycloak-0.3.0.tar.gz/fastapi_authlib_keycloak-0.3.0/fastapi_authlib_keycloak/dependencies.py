
from fastapi import Request, Depends
from typing import Optional, List, Set

from .models import KeycloakUser
# Updated imports to include NoAuthenticatedUserError
from .errors import AuthError, AuthorizationError, MissingRolesError, MissingGroupsError, NoAuthenticatedUserError 

# --- Dependency Functions --- 

def get_current_user(request: Request, auto_error: bool = True) -> Optional[KeycloakUser]:
    """
    FastAPI dependency to get the current authenticated user from request.state.
    
    Args:
        request: The FastAPI Request object.
        auto_error: If True (default), raises NoAuthenticatedUserError if user is not found.
                    If False, returns None if user is not authenticated.
                    
    Returns:
        The KeycloakUser object if authenticated, or None if auto_error is False.
        
    Raises:
        NoAuthenticatedUserError (HTTP 401): 
            If auto_error is True and no user is found in request.state.
    """
    user: Optional[KeycloakUser] = getattr(request.state, "user", None)
    if user is None and auto_error:
        # Raise the specific error for missing user in state
        raise NoAuthenticatedUserError() 
    return user


class RoleChecker:
    """Dependency class to check for required roles."""
    def __init__(self, required_roles: List[str], require_all: bool = True):
        """
        Args:
            required_roles: A list of role names required for access.
            require_all: If True (default), user must have ALL roles. 
                         If False, user must have AT LEAST ONE of the roles.
        """
        self.required_roles = set(required_roles)
        self.require_all = require_all

    def __call__(self, user: KeycloakUser = Depends(get_current_user)) -> KeycloakUser:
        """
        Checks if the authenticated user has the required roles.
        
        Args:
            user: The authenticated KeycloakUser (injected by Depends).
            
        Returns:
            The KeycloakUser if authorization succeeds.
            
        Raises:
            MissingRolesError (HTTP 403): If the user lacks the required roles.
            NoAuthenticatedUserError (HTTP 401): If no authenticated user is found.
        """
        # get_current_user dependency already handles raising NoAuthenticatedUserError 
        # if auto_error is True (default), so the check below is redundant but safe.
        if not user: 
            raise NoAuthenticatedUserError()
            
        user_roles: Set[str] = set(getattr(user, 'roles', []))
        
        has_required_roles: bool
        if self.require_all:
            has_required_roles = self.required_roles.issubset(user_roles)
        else:
            has_required_roles = not self.required_roles.isdisjoint(user_roles) # Check for intersection
            
        if not has_required_roles:
            raise MissingRolesError(required_roles=list(self.required_roles), user_roles=list(user_roles))
            
        return user # Return user if authorized


class GroupChecker:
    """Dependency class to check for required group memberships."""
    def __init__(self, required_groups: List[str], require_all: bool = True):
        """
        Args:
            required_groups: A list of group names required for access.
            require_all: If True (default), user must belong to ALL groups. 
                         If False, user must belong to AT LEAST ONE of the groups.
        """
        self.required_groups = set(required_groups)
        self.require_all = require_all

    def __call__(self, user: KeycloakUser = Depends(get_current_user)) -> KeycloakUser:
        """
        Checks if the authenticated user belongs to the required groups.
        
        Args:
            user: The authenticated KeycloakUser (injected by Depends).
            
        Returns:
            The KeycloakUser if authorization succeeds.
            
        Raises:
            MissingGroupsError (HTTP 403): If the user lacks the required group membership.
            NoAuthenticatedUserError (HTTP 401): If no authenticated user is found.
        """
        # get_current_user dependency already handles raising NoAuthenticatedUserError
        if not user: 
             raise NoAuthenticatedUserError()

        user_groups: Set[str] = set(getattr(user, 'groups', []))
        
        has_required_groups: bool
        if self.require_all:
            has_required_groups = self.required_groups.issubset(user_groups)
        else:
            has_required_groups = not self.required_groups.isdisjoint(user_groups) # Check for intersection
            
        if not has_required_groups:
             raise MissingGroupsError(required_groups=list(self.required_groups), user_groups=list(user_groups))
             
        return user # Return user if authorized


# Convenience functions for common use cases

def require_roles(roles: List[str], require_all: bool = True) -> RoleChecker:
    """
    FastAPI Dependency factory to require specific roles.
    
    Example:
        @app.get("/admin", dependencies=[Depends(require_roles(["admin"]))])
        async def admin_route(...):
            ...
            
        @app.get("/editor", dependencies=[Depends(require_roles(["editor", "publisher"], require_all=False))])
        async def editor_route(...):
            ...
    """
    return RoleChecker(required_roles=roles, require_all=require_all)
    
def require_groups(groups: List[str], require_all: bool = True) -> GroupChecker:
    """
    FastAPI Dependency factory to require specific group membership.
    
    Example:
        @app.get("/finance", dependencies=[Depends(require_groups(["/finance/reporting"]))])
        async def finance_route(...):
            ...
    """
    return GroupChecker(required_groups=groups, require_all=require_all)

