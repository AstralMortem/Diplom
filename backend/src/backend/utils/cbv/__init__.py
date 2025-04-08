import inspect
from typing import (
    Callable,
    ClassVar,
    get_type_hints,
)
from backend.utils.permission_helper import Authorization
from fastapi.routing import APIRoute
from makefun import with_signature
from .route import ControllerRoutes
from fastapi import APIRouter, Depends
from enum import Enum
from fastapi.params import Depends as DependsClass
from pydantic.v1.typing import is_classvar

ROUTE_MARKER = "__is_controller_route__"
CONTROLLER_MARKER = "__is_controller__"


class Controller(ControllerRoutes):
    prefix: ClassVar[str] = ""
    tags: ClassVar[list[str | Enum]] = []
    resource: ClassVar[str] = ""

    @classmethod
    def as_router(cls):
        router = APIRouter(prefix=cls.prefix, tags=cls.tags)

        cls.__init_dependencies()
        cls.__init_routers(router)

        return router

    @classmethod
    def __init_dependencies(cls):
        if getattr(cls, CONTROLLER_MARKER, False):
            return

        # get old init signature
        old_signature = inspect.signature(cls.__init__)
        old_params = list(old_signature.parameters.values())[1:]
        new_params = [
            x
            for x in old_params
            if x.kind
            not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
        ]

        dep_names: list[str] = []
        for name, hint in get_type_hints(cls).items():
            if is_classvar(hint):
                continue
            dep_names.append(name)
            new_params.append(
                inspect.Parameter(
                    name=name,
                    kind=inspect.Parameter.KEYWORD_ONLY,
                    annotation=hint,
                    default=getattr(cls, name, Ellipsis),
                )
            )

        new_params = [
            inspect.Parameter(
                name="self",
                kind=inspect.Parameter.POSITIONAL_ONLY,
                annotation=cls,
            )
        ] + new_params

        new_signature = old_signature.replace(parameters=new_params)

        @with_signature(new_signature)
        def new_init(self, *args, **kwargs):
            for dep_name in dep_names:
                setattr(self, dep_name, kwargs.pop(dep_name))

        setattr(cls, "__init__", new_init)
        setattr(cls, CONTROLLER_MARKER, True)

    @classmethod
    def __init_routers(cls, router: APIRouter):
        for attr_name, attr in inspect.getmembers(cls, inspect.isfunction):
            if attr_name.startswith("__") and attr_name.endswith("__"):
                continue
            if hasattr(attr, ROUTE_MARKER):
                route: APIRoute = attr(cls=cls)
                old_route_signature = inspect.signature(route.endpoint)
                old_route_params = list(old_route_signature.parameters.values())
                new_self_param = old_route_params[0].replace(default=Depends(cls))
                new_params = [new_self_param] + [
                    parameter.replace(kind=inspect.Parameter.KEYWORD_ONLY)
                    for parameter in old_route_params[1:]
                ]

                new_signature = inspect.Signature(new_params)
                route.endpoint = with_signature(new_signature)(route.endpoint)
                route.path = router.prefix + route.path
                router.routes.append(route)
        return router

    @classmethod
    def __override_permissions(cls, func: Callable):
        params = list(inspect.signature(func).parameters.values())
        for idx, param in enumerate(params):
            if isinstance(param.default, DependsClass) and isinstance(
                param.default.dependency, Authorization
            ):
                if param.default.dependency.resource is None:
                    param.default.dependency.resource = cls.resource
                    params[idx].replace(default=param.default)

        return with_signature(inspect.Signature(params))(func)

    @classmethod
    def __override_permissions_list(cls, deps: list[DependsClass]):
        for idx, dep in enumerate(deps):
            if isinstance(dep.dependency, Authorization):
                if dep.dependency.resource is None:
                    dep.dependency.resource = cls.resource
                    deps[idx] = dep
        return deps