import inspect
from backend.utils.cbv import Controller
from fastapi import APIRouter
from fastapi.routing import APIRoute
from fastapi import Depends


def test_controller_route_set():
    class TestController(Controller):
        prefix = "/test"

        @Controller.get(path="/")
        async def get(self):
            return "Hello, World!"

    router: APIRouter = TestController.as_router()
    assert len(router.routes) == 1
    assert isinstance(router.routes[0], APIRoute)
    assert router.routes[0].path == "/test/"


def test_controller_dependencies():
    def test_dependency():
        return "test"

    class TestController(Controller):
        prefix = "/test"

        dependency: str = Depends(test_dependency)

        @Controller.get(path="/")
        async def get(self):
            return self.dependency

    router: APIRouter = TestController.as_router()
    assert len(router.routes) == 1
    assert isinstance(router.routes[0], APIRoute)
