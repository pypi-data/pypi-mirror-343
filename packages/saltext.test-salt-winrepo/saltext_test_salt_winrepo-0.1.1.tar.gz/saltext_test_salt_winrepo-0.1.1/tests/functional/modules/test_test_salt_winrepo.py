import pytest

pytestmark = [
    pytest.mark.requires_salt_modules("test_salt_winrepo.example_function"),
]


@pytest.fixture
def test_salt_winrepo(modules):
    return modules.test_salt_winrepo


def test_replace_this_this_with_something_meaningful(test_salt_winrepo):
    echo_str = "Echoed!"
    res = test_salt_winrepo.example_function(echo_str)
    assert res == echo_str
