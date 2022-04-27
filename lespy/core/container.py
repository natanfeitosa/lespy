import typing as t
from lespy.core.base import Base
from lespy.core.app import App
from lespy.core.router import Route
from lespy.exceptions import AppNotFound, RouteNotFound


class Container(Base):
    _apps: t.List[App] = []
    def __init__(self, *apps):
        if apps and len(apps) > 0:
            for app in apps:
                self.add_app(app)

    def add_app(self, app: App):
        """Add an app to container of apps"""
        self._apps.append(app)
        setattr(self, f'app_{app._app_name}', app)

    def url_for(self, name: str, **params) -> str:
        app_name, path_name = name.strip().split(':')

        try:
            app: App = getattr(self, f'app_{app_name}')
        except:
            raise AppNotFound()
        return app.url_for(path_name, **params)

    def _find_rule(self, path: str, method: str) -> t.Tuple[Route, t.Dict[str, t.Any]]:
        for app in self._apps:
            try:
                return app._find_rule(path, method)
            except:
                pass
        raise RouteNotFound()
