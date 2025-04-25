import pytest
import salt.modules.test as testmod

import saltext.test_salt_winrepo.modules.test_salt_winrepo_mod as test_salt_winrepo_module


@pytest.fixture
def configure_loader_modules():
    module_globals = {
        "__salt__": {"test.echo": testmod.echo},
    }
    return {
        test_salt_winrepo_module: module_globals,
    }


def test_read_value_exists_and_returns_vdata_none():
    assert callable(test_salt_winrepo_module.read_value)
    assert test_salt_winrepo_module.read_value("Hive", "Key", "VName")["vdata"] is None
