# pyright: reportUnusedFunction=false
from typing import TYPE_CHECKING, cast

import jinja2
import markdown
from jinja2.utils import markupsafe  # type: ignore
from klein import Klein
from klein.resource import KleinResource
from twisted.logger import Logger
from twisted.python.filepath import FilePath
from twisted.web import resource, static
from twisted.web.server import Request

from adlermanager.AdlerManagerTokenResource import AdlerManagerTokenResource
from adlermanager.Config import Config

if TYPE_CHECKING:
    from adlermanager.SitesManager import SiteManager, SitesManager

log = Logger()


def get_jinja_env(support_dir: str) -> jinja2.Environment:
    """
    Return a L{jinja2.Environment} with templates loaded from:
      - Package
      - Support dir

    @param support_dir: Full path to support dir.
      See L{authapiv02.DefaultConfig.Config}
    @type support_dir: L{str}
    """
    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.toc",
            "markdown.extensions.tables",
        ]
    )
    templates = jinja2.Environment(
        extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols"],
        loader=jinja2.ChoiceLoader(
            [
                jinja2.FileSystemLoader(support_dir),
                jinja2.PackageLoader("adlermanager", "templates"),
            ]
        ),
        autoescape=True,
    )

    def md_filter(txt: str) -> markupsafe.Markup:
        return markupsafe.Markup(md.convert(txt))

    templates.filters["markdown"] = md_filter  # type: ignore
    return templates


def web_root(sites_manager: "SitesManager") -> KleinResource:
    app = Klein()

    @app.route("/")
    def index(request: Request):  # type: ignore
        try:
            host = cast(str, request.getRequestHostname().decode("utf-8"))
        except Exception:
            return resource.ErrorPage(400, "Bad cat", '<a href="http://http.cat/400">http://http.cat/400</a>')
        if host not in sites_manager.site_managers:
            return resource.ErrorPage(404, "Gone cat", '<a href="http://http.cat/404">http://http.cat/404</a>')
        site: SiteManager
        try:
            site = sites_manager.site_managers[host]
        except Exception:
            log.failure("sad cat")
            return resource.ErrorPage(500, "Sad cat", '<a href="http://http.cat/500">http://http.cat/500</a>')

        site_path = cast(  # type: ignore
            str, FilePath(Config.data_dir).child("sites").child(host).path
        )
        templates = get_jinja_env(site_path)
        template = templates.get_template("template.j2")

        return template.render(site=site)

    @app.route("/api/v2/alerts", methods=["POST"])
    def alert_handler(request: Request):  # type: ignore  # noqa: ARG001
        return AdlerManagerTokenResource(sites_manager)

    @app.route("/static", branch=True)
    def static_files(request: Request):  # type: ignore  # noqa: ARG001
        return static.File(Config.web_static_dir)

    @app.route("/vendor", branch=True)
    def vendor_files(request: Request):  # type: ignore  # noqa: ARG001
        return static.File(FilePath(__file__).parent().child("vendor").path)

    return app.resource()
