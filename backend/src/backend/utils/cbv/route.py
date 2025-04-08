from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from fastapi.utils import generate_unique_id
from fastapi.datastructures import Default

ROUTE_MARKER = "__is_controller_route__"


def get_wrapped_route(func, path, method, **route_kwargs):
    def wrapper(*args, **kwargs):
        current_class: type = kwargs.get("cls")
        if deps:=route_kwargs.get('dependencies', []):
            route_kwargs["dependencies"] = current_class._Controller__override_permissions_list(deps)
        return APIRoute(
            path=path,
            methods=[method],
            endpoint=func,
            response_model=route_kwargs.get("response_model"),
            status_code=route_kwargs.get("status_code"),
            tags=route_kwargs.get("tags", current_class.tags),
            dependencies=route_kwargs.get("dependencies"),
            summary=route_kwargs.get("summary"),
            description=route_kwargs.get("description"),
            response_description=route_kwargs.get(
                "response_description", "Successful response"
            ),
            responses=route_kwargs.get("responses"),
            deprecated=route_kwargs.get("deprecated"),
            name=route_kwargs.get("name", f"{current_class.__name__}.{func.__name__}"),
            operation_id=route_kwargs.get("operation_id"),
            response_model_include=route_kwargs.get("response_model_include"),
            response_model_exclude=route_kwargs.get("response_model_exclude"),
            response_model_by_alias=route_kwargs.get("response_model_by_alias", True),
            response_model_exclude_unset=route_kwargs.get(
                "response_model_exclude_unset", False
            ),
            response_model_exclude_defaults=route_kwargs.get(
                "response_model_exclude_defaults", False
            ),
            response_model_exclude_none=route_kwargs.get(
                "response_model_exclude_none", False
            ),
            include_in_schema=route_kwargs.get("include_in_schema", True),
            response_class=route_kwargs.get("response_class", Default(JSONResponse)),
            dependency_overrides_provider=route_kwargs.get(
                "dependency_overrides_provider"
            ),
            callbacks=route_kwargs.get("callbacks"),
            openapi_extra=route_kwargs.get("openapi_extra"),
            generate_unique_id_function=route_kwargs.get(
                "generate_unique_id_function", Default(generate_unique_id)
            ),
        )

    setattr(wrapper, ROUTE_MARKER, True)
    return wrapper


class ControllerRoutes:
    @classmethod
    def get(cls, path, **kwargs):
        def decorator(func):
            func = cls._Controller__override_permissions(func)
            return get_wrapped_route(func, path, "GET", **kwargs)

        return decorator

    @classmethod
    def post(cls, path, **kwargs):
        def decorator(func):
            func = cls._Controller__override_permissions(func)
            return get_wrapped_route(func, path, "POST", **kwargs)

        return decorator

    @classmethod
    def put(cls, path, **kwargs):
        def decorator(func):
            func = cls._Controller__override_permissions(func)
            return get_wrapped_route(func, path, "PUT", **kwargs)

        return decorator

    @classmethod
    def patch(cls, path, **kwargs):
        def decorator(func):
            func = cls._Controller__override_permissions(func)
            return get_wrapped_route(func, path, "PATCH", **kwargs)

        return decorator

    @classmethod
    def delete(cls, path, **kwargs):
        def decorator(func):
            func = cls._Controller__override_permissions(func)
            return get_wrapped_route(func, path, "DELETE", **kwargs)

        return decorator
