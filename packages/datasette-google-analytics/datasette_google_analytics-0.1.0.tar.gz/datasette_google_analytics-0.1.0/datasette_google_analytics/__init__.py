from datasette import hookimpl
import os
import jinja2

__version__ = "0.1.0"


@hookimpl
def prepare_jinja2_environment(env, datasette):
    """
    Add template directory to the Jinja2 environment.
    """
    template_directory = os.path.join(os.path.dirname(__file__), "templates")
    env.loader = jinja2.ChoiceLoader(
        [env.loader, jinja2.FileSystemLoader(template_directory)]
    )


@hookimpl
def extra_template_vars(datasette):
    """
    Add Google Analytics tracking ID to template variables.
    """

    async def inner():
        plugin_config = datasette.plugin_config("datasette-google-analytics") or {}
        tracking_id = plugin_config.get("tracking_id")

        return {"ga_tracking_id": tracking_id}

    return inner
