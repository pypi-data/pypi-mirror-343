from pathlib import Path
from importlib.metadata import version


def setup(app):
    __version__ = version("grafica")

    app.add_html_theme("grafica", Path(__file__).resolve().parent)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
