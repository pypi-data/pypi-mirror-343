"""
Salt execution module
"""

import logging

log = logging.getLogger(__name__)

__virtualname__ = "test_salt_winrepo"


def __virtual__():
    # To force a module not to load return something like:
    #   return (False, "The test_salt_winrepo execution module is not implemented yet")
    return __virtualname__


def read_value(_hive, _key, _vname=None):
    r"""
    This is a dummy function

    Returns:
        None: Always returns ``None``

    CLI Example:

    .. code-block:: bash

        salt '*' test_salt_winrepo.read_value HKEY_LOCAL_MACHINE 'SOFTWARE\Salt' 'version'
    """
    return {"vdata": None}
