from __future__ import annotations

from typing import Any, Callable

from flask import request


def get_remote_address() -> str:
    """
    :return: the ip address for the current request
     (or 127.0.0.1 if none found)

    """
    if request.headers.getlist("X-Forwarded-For"):
        #return the last ip of the list as the client may add its own
        return request.headers.getlist("X-Forwarded-For")[-1]
    else:
        return request.remote_addr or "127.0.0.1"


def get_qualified_name(callable: Callable[..., Any]) -> str:
    """
    Generate the fully qualified name of a callable for use in storing
    mappings of decorated functions to rate limits

    The __qualname__ of the callable is appended in case there is a name
    clash in a module due to locally scoped functions that are decorated.

    TODO: Ideally __qualname__ should be enough, however view functions
     generated by class based views do not update that and therefore
     would not be uniquely identifiable unless __module__ & __name__
     are inspected.

    :meta private:
    """
    return f"{callable.__module__}.{callable.__name__}.{callable.__qualname__}"
