from collections.abc import Callable
from typing import Any

from django.http import HttpRequest, HttpResponseBase
from django.urls.resolvers import URLPattern

ViewFunc = Callable[[HttpRequest], HttpResponseBase]

def static(prefix: str, view: ViewFunc = ..., **kwargs: Any) -> list[URLPattern]: ...
