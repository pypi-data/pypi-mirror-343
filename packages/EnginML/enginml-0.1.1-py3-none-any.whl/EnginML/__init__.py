"""Public API surface."""
from importlib import metadata as _meta

from .core import fit_regression, fit_classification, fit_clustering, load_csv_or_excel
from .report import save_report

__all__ = [
    "fit_regression",
    "fit_classification",
    "fit_clustering",
    "load_csv_or_excel",
    "save_report",
]

try:
    __version__ = _meta.version("EnginML")
except _meta.PackageNotFoundError:
    __version__ = "0.1.0"