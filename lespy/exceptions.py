"""Exceptions module"""


class RouteNotFound(Exception):
    """The route could not be found or does not exist"""


class DisallowedHost(Exception):
    """Disallowed host
    
    Set this host in `ALLOWED_HOSTS` with `set_config`
    """


class RouteAlreadyExists(Exception):
    """This exact route already exists or another one with the same name or path"""


class AppNotFound(Exception):
    """The app with this name does not exists"""
