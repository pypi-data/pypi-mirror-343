"""Module for primary check function."""

from typing import List
from os import PathLike

from .checksuite import CheckSuite
from .rasmodel import RasModel
from .result import RasqcResult
from .registry import CHECKSUITES


def check(
    ras_model: str | PathLike | RasModel, check_suite: str | CheckSuite
) -> List[RasqcResult]:
    """Run all checks on the provided HEC-RAS model.

    Parameters
    ----------
        ras_model: The HEC-RAS model to check.

    Returns
    -------
        List[RasqcResult]: List of results from all checks.
    """
    if isinstance(check_suite, str):
        check_suite: CheckSuite = CHECKSUITES[check_suite]
    return check_suite.run_checks(ras_model)
