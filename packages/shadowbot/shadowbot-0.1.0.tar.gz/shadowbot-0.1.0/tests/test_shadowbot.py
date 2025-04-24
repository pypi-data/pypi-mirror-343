import pytest
import xbot
from .import package
from shadowbot import SBA, service_init

def test_shadow_bot():
    try:
        sba = SBA(xbot, package)
        service_init(sba, init=True)
    except Exception as e:
        pytest.fail(f"shadow_bot raised an exception: {e}")

test_shadow_bot()